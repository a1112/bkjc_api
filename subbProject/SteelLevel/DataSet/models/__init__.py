# 定义一个模型类
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class SteelLevel(Base):
    #  钢板等级信息表
    __tablename__ = 'SteelLevel'
    id = Column(Integer, primary_key=True)
    plant_classification = Column(String)
    productionLine_classification = Column(String)
    steelName = Column(String)
    packageName = Column(String)
    seqNo = Column(Integer)
    steelID = Column(Integer)
    steelType = Column(String)
    length = Column(Float)
    width = Column(Float)
    thick = Column(Float)
    upDefectNum = Column(Integer)  # 不同缺陷等级的数量
    downDefectNum = Column(Integer)  # 不同缺陷等级的数量
    detectTime = Column(DateTime)
    level = Column(Integer)
    levelInfo = Column(String)
    grade = Column(Integer)
    msg = Column(String)

    level_up = Column(Integer)
    levelInfo_up = Column(String)
    grade_up = Column(Integer)
    msg_up = Column(String)

    level_under = Column(Integer)
    levelInfo_under = Column(String)
    grade_under = Column(Integer)
    msg_under = Column(String)


class DefectLevel(Base):
    #  缺陷等级信息表
    __tablename__ = 'DefectLevel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    defectNo = Column(Integer)
    defectID = Column(Integer)
    defectName = Column(String)
    steelName = Column(String)
    bmIndex = Column(Integer)
    seqNo = Column(Integer)
    packageName = Column(String)
    classId = Column(Integer)
    cameraId = Column(Integer)
    ImageIndex = Column(Integer)

    imageX = Column(Integer)
    imageY = Column(Integer)
    imageW = Column(Integer)
    imageH = Column(Integer)

    steelX = Column(Integer)
    steelY = Column(Integer)
    steelW = Column(Integer)
    steelH = Column(Integer)

    level = Column(Integer)
    levelMsg = Column(String)
    msg = Column(String)


class UserData(Base):
    __tablename__ = 'UserSteelLevelData'
    id = Column(Integer, primary_key=True, autoincrement=True)  # id
    fileName = Column(String)  # 插入的文件名称
    steelName = Column(String)
    plant_classification = Column(String)
    productionLine_classification = Column(String)
    productionTime = Column(DateTime)
    steelType = Column(String)
    steelLevel = Column(Integer)
    steelLevelCode = Column(String)
    residualReasonCode = Column(String)
    defectCode = Column(String)
    scrapReasonCode = Column(String)
    downgradeNote = Column(String)
    BusNumber = Column(String)