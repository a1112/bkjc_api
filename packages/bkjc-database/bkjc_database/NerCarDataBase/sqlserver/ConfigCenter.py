#  encoding=utf-8
"""
自动映射 Classifier 数据库
"""
from typing import List
from bkjc_database.NerCarDataBase.sqlserver.models.ConfigCenter import CamInfo, DefectClass
from bkjc_database.property.DataBaseInterFace import DbItem

databaseName = "ConfigCenter"


class ConfigCenterDb(DbItem):
    def __init__(self):
        super().__init__(databaseName)

    def getCameraInfo(self, cameraId: int):
        """获取相机信息"""
        with self.Session() as session:
            try:
                return session.query(CamInfo).filter(CamInfo.ID == cameraId).first()
            except:
                session.rollback()

    def getCameraInfoList(self):
        """获取相机信息列表"""
        with self.Session() as session:
            try:
                return session.query(CamInfo).all()
            except:
                session.rollback()

    def getDefectClass(self, defectClass: int):
        """获取缺陷类别"""
        with self.Session() as session:
            try:
                return session.query(DefectClass).filter(DefectClass.Class == defectClass).first()
            except:
                session.rollback()

    def getDefectClassList(self):
        """获取缺陷类别列表"""
        with self.Session() as session:
            try:
                return session.query(DefectClass).all()
            except:
                session.rollback()

    @property
    def defectDict(self):
        """缺陷键值对"""
        with self.Session() as session:
            try:
                return dict(session.query(DefectClass.Class, DefectClass.Name).all())
            except:
                session.rollback()

    @property
    def cameraNumber(self):
        """相机总数"""
        with self.Session() as session:
            try:
                return session.query(CamInfo).count()
            except:
                session.rollback()

    @property
    def upCameraIdList(self):
        """上表相机ID"""
        with self.Session() as session:
            try:
                return [res[0] for res in session.query(CamInfo.ID).filter(CamInfo.Surface == 1).all()]
            except:
                session.rollback()

    @property
    def underCameraIdList(self):
        """下表相机ID"""
        with self.Session() as session:
            try:
                return [res[0] for res in session.query(CamInfo.ID).filter(CamInfo.Surface == 0)[:]]
            except:
                session.rollback()


cameraNumber = ConfigCenterDb().cameraNumber
upCameraIdList = ConfigCenterDb().upCameraIdList
underCameraIdList = ConfigCenterDb().underCameraIdList
defectDict = ConfigCenterDb().defectDict  # 缺陷键值对
Session = ConfigCenterDb().Session
