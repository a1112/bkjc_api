#  静态调用
import datetime
import os
from os import path

from bkjc_database import core

modelPath = path.join(path.dirname(__file__), "sqlserver/models\\")


def getSize(session):
    """获取数据库的占用情况
    https://docs.microsoft.com/zh-cn/sql/relational-databases/system-stored-procedures/sp-spaceused-transact-sql?view=sql-server-ver15
    """
    return session.execute("EXEC sp_spaceused")  # sql server


def create_model_file(databaseName: str, baseUrl=None, out_file=None):
    """
    使用 sqlacodegen 工具 自动 生成映射
    """
    if not out_file:
        out_file = path.join(modelPath, databaseName + ".py")
    if not baseUrl:
        baseUrl = core.baseUrl
    code = "sqlacodegen  --noinflect {}>{}".format(baseUrl.format(databaseName), out_file)
    print("创建 {} 映射 \n  执行 {}， {}".format(databaseName, code, os.system(code)))
    #sqlacodegen mssql+pymssql://sa:519223@127.0.0.1:1433/SteelRecord?charset=utf8>SteelRecord.py

def create_all_model(baseUrl=None, cover=False, out_dir=None):
    """
    对数据库生成模型
    """
    if not baseUrl:
        baseUrl = core.baseUrl
    if not out_dir:
        out_dir = modelPath
    from bkjc_database.NerCarDataBase.sqlserver.master import database_names
    for database_name in database_names:
        out_file = path.join(out_dir, database_name + '.py')
        if (not cover and path.exists(out_file)) or database_name in core.systemDatabase:
            continue
        create_model_file(database_name, baseUrl, out_file)


def getDateInfo(dateTime):
    """
    将时间戳，datetime，转换成 字典
    :param dateTime:
    :return:
    """
    if isinstance(dateTime, datetime.datetime):
        return {"year": dateTime.year,
                "month": dateTime.month,
                "weekday": dateTime.weekday(),
                "day": dateTime.day,
                "hour": dateTime.hour,
                "minute": dateTime.minute,
                "second": dateTime.second,
                }
    if isinstance(dateTime, (float, int)):
        return getDateInfo(datetime.datetime.fromtimestamp(dateTime))
    if isinstance(dateTime, datetime.timedelta):
        return {"day": dateTime.days,
                "hour": int(dateTime.seconds / 3600),
                "minute": int(dateTime.seconds / 60) % 60,
                "second": dateTime.seconds % 60
                }


def to_dict(obj, up_Data: dict = None):
    """
    转换成可序列化的字典
    """
    if hasattr(obj, "__dict__") and "_sa_instance_state" in obj.__dict__:
        if not up_Data:
            up_Data = {}
        if len(obj.__dict__) <= 1:
            rd = {key: to_dict(getattr(obj, key)) for key in obj.__dir__() if not key.startswith('_')
                  and key not in ["metadata"] and key not in up_Data}
        else:
            rd = {key: to_dict(getattr(obj, key)) for key in obj.__dict__ if
                  key not in ["_sa_instance_state"] and key not in up_Data}
        rd.update(up_Data)
        return rd
    elif isinstance(obj, datetime.datetime):
        return getDateInfo(obj)
    else:
        return obj
