# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import IMAGE, TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_ClassDefectNum = Table(
    'ClassDefectNum', metadata,
    Column('ID', Integer, nullable=False),
    Column('SubSteelID', Unicode(50), nullable=False),
    Column('Class', Unicode(50)),
    Column('DefectNum', Integer),
    Column('DefectArea', Integer),
    Column('IsTop', Integer)
)


class DTclassTJ(Base):
    __tablename__ = 'DTclassTJ'

    ID = Column(Integer, primary_key=True)
    SequeceNo = Column(Integer, nullable=False)
    Class = Column(TINYINT)
    TopDefectNum = Column(SmallInteger)
    BottomDefectNum = Column(SmallInteger)
    TopDefectNum1 = Column(SmallInteger)
    BottomDefectNum1 = Column(SmallInteger)


t_Defect = Table(
    'Defect', metadata,
    Column('No', Integer, nullable=False),
    Column('SequeceNo', Integer),
    Column('DefectNo', Integer),
    Column('Class', TINYINT),
    Column('Class2', TINYINT),
    Column('ClassIdentify', TINYINT),
    Column('CameraNo', SmallInteger),
    Column('Width', SmallInteger),
    Column('Height', SmallInteger),
    Column('Area', Integer, nullable=False),
    Column('PosInLen', Integer),
    Column('PosInWidth', Integer),
    Column('ImgData', IMAGE),
    Column('DefectGrade', TINYINT),
    Column('IsTop', TINYINT),
    Column('Cycle', SmallInteger)
)


t_DefectClass = Table(
    'DefectClass', metadata,
    Column('Class', TINYINT),
    Column('Name', String(32, 'Chinese_PRC_CI_AS')),
    Column('Grade', TINYINT),
    Column('Dsc', String(64, 'Chinese_PRC_CI_AS'))
)


t_SteelID = Table(
    'SteelID', metadata,
    Column('No', Integer, nullable=False),
    Column('ID', String(50, 'Chinese_PRC_CI_AS')),
    Column('AddTime', DateTime)
)


t_SteelWarn = Table(
    'SteelWarn', metadata,
    Column('ID', Integer, nullable=False),
    Column('SirenNo', TINYINT, nullable=False),
    Column('Info', String(260, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('Type', Integer, nullable=False, server_default=text("((0))")),
    Column('Process', TINYINT, server_default=text("((0))")),
    Column('Sender', String(50, 'Chinese_PRC_CI_AS'))
)


t_SubSteel = Table(
    'SubSteel', metadata,
    Column('ID', Integer, nullable=False),
    Column('SubSteelID', String(50, 'Chinese_PRC_CI_AS'), nullable=False),
    Column('SteelID', Unicode(50)),
    Column('Length', Integer),
    Column('ParentLength', Integer),
    Column('Cut', Integer),
    Column('Type', Unicode(50))
)


t_WarnDefine = Table(
    'WarnDefine', metadata,
    Column('TypeID', Integer, nullable=False),
    Column('WarnType', TINYINT, nullable=False),
    Column('Descrip', String(200, 'Chinese_PRC_CI_AS'), nullable=False)
)


t_steel = Table(
    'steel', metadata,
    Column('ID', Integer, nullable=False),
    Column('SequeceNo', Integer, nullable=False),
    Column('SteelID', String(50, 'Chinese_PRC_CI_AS')),
    Column('Length', Integer),
    Column('Grade', TINYINT),
    Column('Grade1', TINYINT),
    Column('TopDefectNum', SmallInteger),
    Column('BottomDefectNum', SmallInteger),
    Column('DetectTime', DateTime),
    Column('UpdateTime', DateTime),
    Column('Dsc', String(256, 'Chinese_PRC_CI_AS'))
)
