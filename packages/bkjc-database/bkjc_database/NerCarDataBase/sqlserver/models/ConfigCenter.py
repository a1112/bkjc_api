# coding: utf-8
from sqlalchemy import Column, Float, Integer, NCHAR, SmallInteger, Unicode, text
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class CamDefectImg(Base):
    __tablename__ = 'CamDefectImg'

    CamNo = Column(TINYINT, primary_key=True)
    Server = Column(NCHAR(16))
    Path = Column(NCHAR(128))


class CamInfo(Base):
    __tablename__ = 'CamInfo'

    ID = Column(TINYINT, primary_key=True)
    ImageSrcIndex = Column(TINYINT, nullable=False)
    Surface = Column(TINYINT, nullable=False)
    Descript = Column(Unicode(50))
    Temper = Column(TINYINT)
    TemperGate = Column(TINYINT)
    FrameRate = Column(Float(53))


class Cooler(Base):
    __tablename__ = 'Cooler'

    ID = Column(TINYINT, primary_key=True)
    Temper = Column(TINYINT)
    TemperGate = Column(TINYINT)
    Intense = Column(TINYINT)
    Status = Column(TINYINT)
    Descript = Column(Unicode(50))


class DefectClass(Base):
    __tablename__ = 'DefectClass'

    ID = Column(TINYINT, primary_key=True)
    Name = Column(Unicode(50), nullable=False)
    Grade = Column(TINYINT, nullable=False, server_default=text("((0))"))
    Class = Column(TINYINT, nullable=False)
    Red = Column(TINYINT, nullable=False)
    Green = Column(TINYINT, nullable=False)
    Blue = Column(TINYINT, nullable=False)


class ImageSource(Base):
    __tablename__ = 'ImageSource'

    ID = Column(TINYINT, primary_key=True)
    CamNum = Column(TINYINT, nullable=False)
    IP = Column(Unicode(20), nullable=False)
    Port = Column(SmallInteger, nullable=False)
    SrcImageIndexPath = Column(Unicode(64), nullable=False)
    DetectImageIndexPath = Column(Unicode(64), nullable=False)
    Descript = Column(Unicode(50))


class Light(Base):
    __tablename__ = 'Light'

    ID = Column(TINYINT, primary_key=True)
    Temper = Column(TINYINT)
    TemperGate = Column(TINYINT)
    Intense = Column(SmallInteger)
    Status = Column(TINYINT)
    Surface = Column(TINYINT)


class Services(Base):
    __tablename__ = 'Services'

    ID = Column(Integer, primary_key=True)
    Name = Column(Unicode(50), nullable=False)
    IP = Column(Unicode(16), nullable=False)
    Port = Column(SmallInteger, nullable=False)
    Descrip = Column(Unicode(50))
    RunStatus = Column(TINYINT)


class Sync(Base):
    __tablename__ = 'Sync'

    ID = Column(TINYINT, primary_key=True)
    Status = Column(TINYINT)
    Surface = Column(TINYINT)
    Dsc = Column(Unicode(50))


class UserFunc(Base):
    __tablename__ = 'UserFunc'

    ID = Column(Integer, primary_key=True)
    Name = Column(NCHAR(32))
    FuncType = Column(SmallInteger, nullable=False)
    Grade = Column(TINYINT, nullable=False, server_default=text("((0))"))
    Descript = Column(Unicode(64))


class UserGroup(Base):
    __tablename__ = 'UserGroup'

    ID = Column(Integer, primary_key=True)
    GroupID = Column(SmallInteger)
    Name = Column(NCHAR(32))
    Grade = Column(TINYINT)
    Descript = Column(Unicode(50))


class UserInfo(Base):
    __tablename__ = 'UserInfo'

    ID = Column(Integer, primary_key=True)
    Name = Column(Unicode(32))
    Passwd = Column(Unicode(50))
    GroupID = Column(SmallInteger)
