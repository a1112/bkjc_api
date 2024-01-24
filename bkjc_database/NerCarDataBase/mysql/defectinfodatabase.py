from bkjc_database.NerCarDataBase.BaseImport import *
from bkjc_database.NerCarDataBase.SqlBase import init
from bkjc_database.NerCarDataBase.core import beforeInit

from bkjc_database.NerCarDataBase.mysql import Ncdhotstrip
from bkjc_database.NerCarDataBase.mysql import Ncdhotstripdefect

databaseName = "defectinfodatabase"

engine: Engine
Base: automap_base
Session: sessionmaker
session: Session
inspector: Inspector
table_names: list


def appendDefect(defect,steel):
    defect: Ncdhotstripdefect.Camdefect1
    steel: Ncdhotstrip.Steelrecord
    session.add(Defect(defectNo=defect.defectID,steelID=steel.steelID,
                       steelintop=defect.topInObj,steelinleft=defect.leftToEdge,
                       steelinright=defect.rightToEdge,classno=defect.camNo,
                       Top=int(defect.camNo == 1),defectLen=defect.bottomInObj-defect.topInObj,
                       defectwidth=defect.rightInObj-defect.leftInObj,imageNo=defect.imgIndex))


def getLastDefect(isTop):
    return session.query(Defect).where(isTop == Defect.Top)[0]


def getLastDefectId(isTop):
    try:
        return session.query(Defect).where(isTop == Defect.Top)[0].defectNo
    except:
        return 0

def dbInit():
    global engine, Base, Session, session, inspector, table_names
    engine, Base, Session, session, inspector = init(databaseName)
    table_names = inspector.get_table_names()


if beforeInit:
    dbInit()
