"""Destination defect store; callers own each transaction explicitly."""
from sqlalchemy import func
from bkjc_database.NerCarDataBase.mysql.models.defectinfodatabase import Defect
from bkjc_database.property.DataBaseInterFace import DbItem


class DefectInfoDb(DbItem):
    def __init__(self):
        super().__init__("defectinfodatabase")

    def appendDefect(self, defect, steel, session):
        if steel is None:
            raise ValueError("Missing steel record; refusing to advance the defect cursor")
        row = Defect(defectNo=defect.defectID, steelID=steel.steelID,
            steelintop=defect.topInObj, steelinleft=defect.leftToEdge,
            steelinright=defect.rightToEdge, classno=defect.camNo,
            Top=int(defect.camNo == 1), defectLen=defect.bottomInObj-defect.topInObj,
            defectwidth=defect.rightInObj-defect.leftInObj, imageNo=defect.imgIndex)
        session.add(row)
        return row

    def getLastDefect(self, isTop, session):
        return session.query(Defect).filter(Defect.Top == isTop).order_by(Defect.defectNo.desc()).first()

    def getLastDefectId(self, isTop, session):
        return session.query(func.max(Defect.defectNo)).filter(Defect.Top == isTop).scalar() or 0


defectInfoDb = DefectInfoDb()
