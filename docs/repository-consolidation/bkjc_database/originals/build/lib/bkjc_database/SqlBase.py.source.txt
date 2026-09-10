#  encoding = utf-8


import logging
from typing import List
from collections import defaultdict
from os import path

from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.engine.base import Engine
from sqlalchemy.engine.reflection import Inspector
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool

# import sqlacodegen  # 生成映射

from bkjc_database import core, CONFIG

modelPath = path.join(path.dirname(__file__), "sqlserver/models\\")
connectDicts = defaultdict(dict)


def get_engine(databaseName, baseUrl: str = None) -> Engine:
    """通过url 获取 engine """
    echo=False
    if not baseUrl:
        baseUrl = CONFIG.globDbConfig.baseUrl
        echo = CONFIG.globDbConfig.echo
    return create_engine(baseUrl.format(databaseName), poolclass=QueuePool, pool_size=100, max_overflow=20, pool_recycle=100, pool_pre_ping=True,
                         echo=echo)


def get_inspector(engine) -> Inspector:
    """通过 Engine 获取描述"""
    return inspect(engine)


def init(databaseName: str, baseUrl=None, flush=False) -> (Engine, automap_base, sessionmaker, Inspector):
    """必要初始化"""
    connect = connectDicts[databaseName]

    engine = get_engine(databaseName, baseUrl)
    tryConnect(engine)
    Base = automap_base()
    Base.prepare(engine, reflect=False)
    Session_ = sessionmaker(bind=engine, expire_on_commit=True)
    inspector = get_inspector(engine)
    tables = getAllTableName(inspector)
    connect["engine"], connect["Base"], connect["Session"], connect["inspector"], \
    connect["tables"] = engine, Base, Session_,inspector, tables
    return engine, Base, Session_,inspector


def tryConnect(engine: Engine):
    """处理连接的错误情况"""
    try:
        engine.connect()
    except OperationalError as e:
        print("致命错误，无法完成连接 {}".format(engine.url))
        logging.critical("连接 {} 失败，可能原因有 密码过期，数据库不存在... ...".format(engine.url))
        raise e


def getConnectDict(databaseName: str):
    """
    no doc
    """
    if databaseName not in connectDicts:
        init(databaseName)
    return connectDicts[databaseName]


def getAllTableName(inspector) -> List[str]:
    """获取所有表格名称"""
    return inspector.get_table_names()


def try_get_table(base, table_name: str):
    """获取表的映射"""
    try:
        re = getattr(base.classes, table_name)
        logging.debug("完成 {} 的自动映射".format(table_name))
        return re
    except (AttributeError,):
        logging.error("无法自动映射 {} 表。请检查该表是否存在主键".format(table_name))
        return None


def getSize(session):
    """获取数据库的占用情况
    https://docs.microsoft.com/zh-cn/sql/relational-databases/system-stored-procedures/sp-spaceused-transact-sql?view=sql-server-ver15
    """
    return session.execute("EXEC sp_spaceused")


def getAutoMap(base, tableList: List[str]):
    """
    尝试自动完成映射，如果无法自动完成映射，说明表
    """
