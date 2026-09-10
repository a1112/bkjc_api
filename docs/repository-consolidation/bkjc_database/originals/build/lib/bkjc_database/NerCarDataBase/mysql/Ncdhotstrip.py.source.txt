from bkjc_database.property.DataBaseInterFace import DbItem

from bkjc_database.CONFIG import globDbConfig

if globDbConfig.database_type == "ncdhotstrip":
    databaseName = "Ncdhotstrip"
    from bkjc_database.NerCarDataBase.mysql.models.ncdhotstrip import *
else:
    from bkjc_database.NerCarDataBase.mysql.models.ncdplate import *
    databaseName = "Ncdplate"


class SteelDb(DbItem):
    def __init__(self):
        super().__init__(databaseName)

    def getSteelBySeqNo(self, seqNo):
        with self.Session() as session:
            try:
                return session.query(Steelrecord).where(Steelrecord.seqNo == seqNo)[0]
            except:
                session.rollback()
                return None

    @property
    def upCameraIdList(self):
        return [1]

    @property
    def underCameraIdList(self):
        return [2]

    @property
    def allCamera(self):
        return self.upCameraIdList + self.underCameraIdList

    @property
    def cameraNumber(self):
        return 4

steelDb = SteelDb()
underCameraIdList = steelDb.underCameraIdList
upCameraIdList = steelDb.upCameraIdList
allCamera = steelDb.allCamera
Session = steelDb.Session

steelDb.createDatabase(Base.metadata)