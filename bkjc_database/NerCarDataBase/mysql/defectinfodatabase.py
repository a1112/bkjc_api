from bkjc_database.NerCarDataBase.mysql.models.defectinfodatabase import Defect

from bkjc_database.property.DataBaseInterFace import DbItem

from bkjc_database.BaseImport import *
from bkjc_database.SqlBase import init
from bkjc_database.CONFIG import beforeInit

from bkjc_database.NerCarDataBase.mysql import Ncdhotstrip
from bkjc_database.NerCarDataBase.mysql import Ncdhotstripdefect

databaseName = "defectinfodatabase"

engine: Engine
Base: automap_base
Session: sessionmaker
session: Session
inspector: Inspector
table_names: list


class DefectInfoDb(DbItem):
    def appendDefect(self,defect,steel):
        defect: Ncdhotstripdefect.Camdefect1
        steel: Ncdhotstrip.Steelrecord
        session.add(Defect(defectNo=defect.defectID,steelID=steel.steelID,
                           steelintop=defect.topInObj,steelinleft=defect.leftToEdge,
                           steelinright=defect.rightToEdge,classno=defect.camNo,
                           Top=int(defect.camNo == 1),defectLen=defect.bottomInObj-defect.topInObj,
                           defectwidth=defect.rightInObj-defect.leftInObj,imageNo=defect.imgIndex))

    def getLastDefect(self,isTop):
        return session.query(Defect).where(isTop == Defect.Top)[0]


    def getLastDefectId(self,isTop):
        try:
            return session.query(Defect).where(isTop == Defect.Top)[0].defectNo
        except:
            return 0

    def dbInit(self):
        global engine, Base, Session, session, inspector, table_names
        engine, Base, Session, session, inspector = init(databaseName)
        table_names = inspector.get_table_names()

