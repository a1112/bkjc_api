# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, Unicode, text, Identity, Table
from sqlalchemy.dialects.mssql import IMAGE, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Defect(Base):
    __tablename__ = 'Defect'

    ID = Column(Integer, primary_key=True)
    DefectNo = Column(Integer, nullable=False)
    SteelNo = Column(Integer, nullable=False)
    CameraNo = Column(SmallInteger, nullable=False)
    ImageIndex = Column(SmallInteger, nullable=False)
    Class = Column(SmallInteger, nullable=False)
    Grade = Column(SmallInteger, nullable=False)
    LeftInImg = Column(SmallInteger, nullable=False)
    RightInImg = Column(SmallInteger, nullable=False)
    TopInImg = Column(SmallInteger, nullable=False)
    BottomInImg = Column(SmallInteger, nullable=False)
    LeftInSteel = Column(SmallInteger, nullable=False)
    RightInSteel = Column(SmallInteger, nullable=False)
    TopInSteel = Column(Integer, nullable=False)
    BottomInSteel = Column(Integer, nullable=False)
    Area = Column(Integer, nullable=False)
    Cycle = Column(SmallInteger, nullable=False)
    Class2 = Column(SmallInteger, nullable=False)
    Grade2 = Column(SmallInteger)
    LeftInImg2 = Column(SmallInteger)
    RightInImg2 = Column(SmallInteger)
    TopInImg2 = Column(SmallInteger)
    BottomInImg2 = Column(SmallInteger)
    LeftInSteel2 = Column(SmallInteger)
    RightInSteel2 = Column(SmallInteger)
    TopInSteel2 = Column(Integer)
    BottomInSteel2 = Column(Integer)
    Area2 = Column(Integer)
    Cycle2 = Column(SmallInteger)
    UpdateTime = Column(DateTime)
    ImgData = Column(IMAGE)


class SteelGrade(Base):
    __tablename__ = 'SteelGrade'

    ID = Column(Integer, primary_key=True)
    SequeceNo = Column(Integer, nullable=False)
    Grade = Column(TINYINT, nullable=False)
    Warn = Column(TINYINT, server_default=text("((0))"))
    ConfirmWarn = Column(Integer)
    Dsc = Column(Unicode(250))


class SteelID(Base):
    __tablename__ = 'SteelID'

    No = Column(Integer, primary_key=True)
    ID = Column(String(50, 'Chinese_PRC_CI_AS'))
    Width = Column(SmallInteger)
    Thick = Column(SmallInteger)
    Length = Column(Integer)
    Used = Column(TINYINT)
    AddTime = Column(DateTime)
    SteelStatus = Column(Integer)
    SteelType = Column(Unicode(50))


class SteelWidth(Base):
    __tablename__ = 'SteelWidth'

    ID = Column(Integer, primary_key=True)
    SequeceNo = Column(Integer, nullable=False)
    LeftPos = Column(SmallInteger)
    RightPos = Column(SmallInteger)
    Length = Column(Integer)
    ImgIndex = Column(Integer)


# t_SteelGrade = Table(
#     'SteelGrade', metadata,
#     Column('ID', Integer, Identity(start=1, increment=1), nullable=False),
#     Column('SequeceNo', Integer, nullable=False),
#     Column('Grade', TINYINT, nullable=False),
#     Column('Warn', TINYINT, server_default=text('((0))')),
#     Column('ConfirmWarn', Integer),
#     Column('Dsc', Unicode(250))
# )


class SteelGradeInfo(Base):
    __tablename__ = 'SteelGradeInfo'
    ID = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    SequeceNo = Column(Integer, nullable=False, unique=True)
    SteelName = Column(String(50, 'Chinese_PRC_CI_AS'), nullable=False)
    DetectTime = Column(DateTime, nullable=False)
    SteelUse = Column(String(50, 'Chinese_PRC_CI_AS'), nullable=False)
    SteelType = Column(String(50, 'Chinese_PRC_CI_AS'), nullable=False)
    Grade = Column(TINYINT, nullable=False)
    Quality = Column(String(10, 'Chinese_PRC_CI_AS'), nullable=False)
    DscTop = Column(Unicode)
    DscBot = Column(Unicode)

class Steel(Base):
    __tablename__ = 'steel'

    ID = Column(Integer, primary_key=True)
    SequeceNo = Column(Integer, nullable=False)
    ImageNo = Column(Integer)
    SteelID = Column(String(50, 'Chinese_PRC_CI_AS'))
    TopImageError = Column(SmallInteger)
    TopLen = Column(Integer)
    TopWidth = Column(SmallInteger)
    TopDefectNum = Column(SmallInteger)
    TopDetectTime = Column(DateTime)
    BottomImageError = Column(SmallInteger)
    BottomLen = Column(Integer)
    BottomWidth = Column(SmallInteger)
    BottomDefectNum = Column(SmallInteger)
    BottomDetectTime = Column(DateTime)
    Grade = Column(SmallInteger)
    Class = Column(String(64, 'Chinese_PRC_CI_AS'))
    Thick = Column(Integer)
    SteelType = Column(String(64, 'Chinese_PRC_CI_AS'))
    DetectStatus = Column(Integer, server_default=text("((0))"))
