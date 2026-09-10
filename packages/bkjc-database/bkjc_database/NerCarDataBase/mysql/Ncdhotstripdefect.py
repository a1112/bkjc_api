from bkjc_database.CONFIG import globDbConfig
if globDbConfig is None:
    raise RuntimeError("Configure database before importing MySQL models")
if globDbConfig.database_type == "ncdhotstrip":
    from bkjc_database.NerCarDataBase.mysql.models.ncdhotstripdefect import *
else:
    from bkjc_database.NerCarDataBase.mysql.models.ncdplatedefect import *
from bkjc_database.property.DataBaseInterFace import DbItem


class DefectDb(DbItem):
    def __init__(self):
        if globDbConfig.database_type == "ncdhotstrip":
            self.databaseName = "ncdhotstripdefect"
        else:
            self.databaseName = "Ncdplatedefect"
        super().__init__(self.databaseName)

    def getDefectByDefectId(self, cameraId, defectId):
        with self.Session() as session:
            try:
                if cameraId == 1:
                    return session.query(Camdefect1).where(Camdefect1.defectID == defectId)[0]
                else:
                    return session.query(Camdefect2).where(Camdefect2.defectID == defectId)[0]
            except:
                session.rollback()
                return None

    def getDefectsAfter(self, cameraId, defectId, limit=500):
        """Return a bounded, ascending batch strictly after the committed cursor."""
        if cameraId not in (1, 2) or not 1 <= limit <= 10000:
            raise ValueError("Invalid camera or batch size")
        model = Camdefect1 if cameraId == 1 else Camdefect2
        with self.Session() as session:
            return session.query(model).filter(model.defectID > defectId).order_by(model.defectID.asc()).limit(limit).all()

    def getLastDefect(self, cameraId):
        with self.Session() as session:
            try:
                if cameraId == 1:
                    return session.query(Camdefect1)[-1]
                else:
                    return session.query(Camdefect2)[-1]
            except:
                session.rollback()
                return None

defectDb = DefectDb()
Session = defectDb.Session
