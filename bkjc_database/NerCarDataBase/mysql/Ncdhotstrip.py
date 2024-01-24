from typing import List
from bkjc_database.NerCarDataBase.BaseImport import *
from bkjc_database.NerCarDataBase.SqlBase import init
from bkjc_database.NerCarDataBase.core import beforeInit
from config import database_type

if database_type=="ncdhotstrip":
    databaseName = "Ncdhotstrip"
else:
    from bkjc_database.NerCarDataBase.mysql.models.ncdplate import *
    databaseName = "Ncdplate"

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
    return 4


def getUpCameraIdList() -> List[int]:
    """获取上表相机ID"""
    return [1]


def getUnderCameraIdList() -> List[int]:
    """获取下表相机ID"""
    return [2]


def getSteelBySeqNo(seqNo):
    return session.query(Steelrecord).where(Steelrecord.seqNo == seqNo)[0]


upCameraIdList = [1]
underCameraIdList = [2]
allCamera=upCameraIdList+underCameraIdList
if beforeInit:
    dbInit()
    cameraNumber = getCameraNumber()
    upCameraIdList = getUpCameraIdList()
    underCameraIdList = getUnderCameraIdList()
    allCamera = upCameraIdList + underCameraIdList
