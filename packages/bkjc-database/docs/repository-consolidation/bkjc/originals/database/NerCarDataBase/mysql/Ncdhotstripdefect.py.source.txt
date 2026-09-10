from bkjc_database.NerCarDataBase.BaseImport import *
from bkjc_database.NerCarDataBase.SqlBase import init
from bkjc_database.NerCarDataBase.core import beforeInit
from config import database_type

if database_type == "ncdhotstrip":
    databaseName = "ncdhotstripdefect"
else:
    databaseName = "Ncdplatedefect"


engine: Engine
Base: automap_base
Session: sessionmaker
session: Session
inspector: Inspector
table_names: list


def getLastDefect(cameraId):
    if cameraId == 1:
        return session.query(Camdefect1)[-1]
    else:
        return session.query(Camdefect2)[-1]


def getDefectByDefectId(cameraId,defectId):
    if cameraId == 1:
        return session.query(Camdefect1).where(Camdefect1.defectID > defectId)
    else:
        return session.query(Camdefect2).where(Camdefect2.defectID > defectId)

def dbInit():
    global engine, Base, Session, session, inspector, table_names
    engine, Base, Session, session, inspector = init(databaseName)
    table_names = inspector.get_table_names()


if beforeInit:
    dbInit()
