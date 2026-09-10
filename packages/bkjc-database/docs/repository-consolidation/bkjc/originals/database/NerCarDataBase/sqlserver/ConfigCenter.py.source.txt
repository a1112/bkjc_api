#  encoding=utf-8
"""
自动映射 Classifier 数据库
"""
from typing import List
from bkjc_database.NerCarDataBase.BaseImport import *
from bkjc_database.NerCarDataBase.SqlBase import init
from bkjc_database.NerCarDataBase.core import beforeInit
from bkjc_database.NerCarDataBase.sqlserver.models.ConfigCenter import CamInfo, DefectClass

databaseName = "ConfigCenter"

engine: Engine
Base: automap_base
Session: sessionmaker
session: Session
inspector: Inspector
table_names: list


def dbInit():
    global engine, Base, Session, session, inspector, table_names
    engine, Base, Session, session, inspector = init(databaseName)
    table_names = inspector.get_table_names()


def getCameraNumber():
    return session.query(CamInfo).count()  # 相机总数


def getUpCameraIdList() -> List[int]:
    """获取上表相机ID"""
    return [res[0] for res in session.query(CamInfo.ID).filter(CamInfo.Surface == 1).all()]


def getUnderCameraIdList() -> List[int]:
    """获取下表相机ID"""
    return [res[0] for res in session.query(CamInfo.ID).filter(CamInfo.Surface == 0)[:]]


if beforeInit:
    dbInit()
    cameraNumber = getCameraNumber()
    upCameraIdList = getUpCameraIdList()
    underCameraIdList = getUnderCameraIdList()
    defectDict = dict(session.query(DefectClass.Class, DefectClass.Name).all())  # 缺陷键值对
