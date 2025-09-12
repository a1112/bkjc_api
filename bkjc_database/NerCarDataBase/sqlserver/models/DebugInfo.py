# coding: utf-8
from sqlalchemy import Column, DateTime, Integer, LargeBinary, SmallInteger, Table, Unicode, text
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Info(Base):
    __tablename__ = 'Info'

    ID = Column(Integer, primary_key=True)
    FromObj = Column(Unicode(50), nullable=False)
    Type = Column(TINYINT, nullable=False)
    InfoContent = Column(Unicode(256), nullable=False)
    InfoID = Column(SmallInteger, nullable=False)
    Time = Column(DateTime, nullable=False)


class InfoDesc(Base):
    __tablename__ = 'InfoDesc'

    ID = Column(Integer, primary_key=True)
    FromObj = Column(Unicode(50), nullable=False)
    InfoID = Column(SmallInteger, nullable=False)
    Descript = Column(Unicode(100))


class TypeInfo(Base):
    __tablename__ = 'TypeInfo'

    ID = Column(Integer, primary_key=True)
    Type = Column(TINYINT)
    Descript = Column(Unicode(50))
    Grade = Column(TINYINT)


t_WarnLog = Table(
    'WarnLog', metadata,
    Column('ID', Integer, nullable=False),
    Column('InfoID', SmallInteger, nullable=False),
    Column('SteelNo', Integer),
    Column('IsProcess', TINYINT, server_default=text("((0))")),
    Column('Dsc', LargeBinary(200)),
    Column('Operator', Unicode(50)),
    Column('WarnTime', DateTime, nullable=False)
)
