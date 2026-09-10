# coding: utf-8
from sqlalchemy import Column, Integer, SmallInteger, Table
from sqlalchemy.dialects.mssql import IMAGE, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_CycleDefect = Table(
    'CycleDefect', metadata,
    Column('ID', Integer, nullable=False),
    Column('DefectNo', Integer, nullable=False),
    Column('SteelNo', Integer, nullable=False),
    Column('CameraNo', SmallInteger, nullable=False),
    Column('ImageIndex', SmallInteger, nullable=False),
    Column('Class', SmallInteger, nullable=False),
    Column('Grade', SmallInteger, nullable=False),
    Column('LeftInImg', SmallInteger, nullable=False),
    Column('RightInImg', SmallInteger, nullable=False),
    Column('TopInImg', SmallInteger, nullable=False),
    Column('BottomInImg', SmallInteger, nullable=False),
    Column('LeftInSteel', SmallInteger, nullable=False),
    Column('RightInSteel', SmallInteger, nullable=False),
    Column('TopInSteel', Integer, nullable=False),
    Column('BottomInSteel', Integer, nullable=False),
    Column('Area', Integer, nullable=False),
    Column('Cycle', SmallInteger, nullable=False),
    Column('ImgData', IMAGE)
)


class Defect(Base):
    __tablename__ = 'Defect'

    ID = Column(Integer, nullable=False)
    DefectNo = Column(Integer, primary_key=True, nullable=False)
    SteelNo = Column(Integer, nullable=False)
    CameraNo = Column(SmallInteger, primary_key=True, nullable=False)
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
    ImgData = Column(IMAGE)


class Defect1(Base):
    __tablename__ = 'Defect1'

    ID = Column(Integer, nullable=False)
    DefectNo = Column(Integer, primary_key=True, nullable=False)
    SteelNo = Column(Integer, nullable=False)
    CameraNo = Column(SmallInteger, primary_key=True, nullable=False)
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
    ImgData = Column(IMAGE)


t_DefectTJ = Table(
    'DefectTJ', metadata,
    Column('ID', Integer, nullable=False),
    Column('SteelNo', Integer, nullable=False),
    Column('Class', TINYINT, nullable=False),
    Column('DefectNum', SmallInteger),
    Column('DefectArea', Integer),
    Column('CycleLen', Integer),
    Column('MaxDefectSize', Integer),
    Column('MaxDefectLen', Integer),
    Column('MaxDefectWidth', Integer)
)


t_DefectTempClassified = Table(
    'DefectTempClassified', metadata,
    Column('ID', Integer, nullable=False),
    Column('DefectNo', Integer, nullable=False),
    Column('SteelNo', Integer, nullable=False),
    Column('CameraNo', SmallInteger, nullable=False),
    Column('ImageIndex', SmallInteger, nullable=False),
    Column('Class', SmallInteger, nullable=False),
    Column('Grade', SmallInteger, nullable=False),
    Column('LeftInImg', SmallInteger, nullable=False),
    Column('RightInImg', SmallInteger, nullable=False),
    Column('TopInImg', SmallInteger, nullable=False),
    Column('BottomInImg', SmallInteger, nullable=False),
    Column('LeftInSteel', SmallInteger, nullable=False),
    Column('RightInSteel', SmallInteger, nullable=False),
    Column('TopInSteel', Integer, nullable=False),
    Column('BottomInSteel', Integer, nullable=False),
    Column('Area', Integer, nullable=False),
    Column('Cycle', SmallInteger, nullable=False),
    Column('ImgData', IMAGE)
)
