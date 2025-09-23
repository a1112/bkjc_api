# 定义一个模型类
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime,Text
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


class SteelLevel(Base):
    #  钢板等级信息表
    __tablename__ = 'SteelLevel'
    id = Column(Integer, primary_key=True)
    plant_classification = Column(String(50))
    productionLine_classification = Column(String(50))
    steelName = Column(String(50))
    packageName = Column(String(50))
    seqNo = Column(Integer)
    steelID = Column(Integer)
    steelType = Column(String(30))
    length = Column(Float)
    width = Column(Float)
    thick = Column(Float)
    upDefectNum = Column(Integer)  # 不同缺陷等级的数量
    downDefectNum = Column(Integer)  # 不同缺陷等级的数量
    detectTime = Column(DateTime)
    level = Column(Integer)
    levelInfo = Column(Text())
    grade = Column(Integer)
    msg = Column(Text())

    level_up = Column(Integer)
    levelInfo_up = Column(String(10))
    grade_up = Column(Integer)
    msg_up = Column(Text())

    level_under = Column(Integer)
    levelInfo_under = Column(String(10))
    grade_under = Column(Integer)
    msg_under = Column(Text())


class DefectLevel(Base):
    #  缺陷等级信息表
    __tablename__ = 'DefectLevel'
    id = Column(Integer, primary_key=True, autoincrement=True)
    defectNo = Column(Integer)
    defectID = Column(Integer)
    defectName = Column(String(20))
    steelName = Column(String(20))
    bmIndex = Column(Integer)
    seqNo = Column(Integer)
    packageName = Column(String(30))
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
    levelMsg = Column(Text())
    msg = Column(Text())


class UserData(Base):
    __tablename__ = 'UserSteelLevelData'
    id = Column(Integer, primary_key=True, autoincrement=True)  # id
    fileName = Column(String(256))  # 插入的文件名称
    steelName = Column(String(30))
    plant_classification = Column(String(50))
    productionLine_classification = Column(String(50))
    productionTime = Column(DateTime)
    steelType = Column(String(30))
    steelLevel = Column(Integer)
    steelLevelCode = Column(String(5))
    residualReasonCode = Column(String(5))
    defectCode = Column(String(5))
    scrapReasonCode = Column(String(5))
    downgradeNote = Column(String(5))
    busNumber = Column(String(10))