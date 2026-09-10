# coding: utf-8
from sqlalchemy import Column, Integer, NCHAR, SmallInteger, Table, Unicode
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_Info = Table(
    'Info', metadata,
    Column('ID', SmallInteger, nullable=False),
    Column('Name', Unicode(50), nullable=False),
    Column('Comment', NCHAR(250))
)


class Parameter(Base):
    __tablename__ = 'Parameter'

    ID = Column(Integer, primary_key=True)
    Type = Column(TINYINT, nullable=False)
    Classifier = Column(SmallInteger, nullable=False)
    Name = Column(NCHAR(32), nullable=False)
    Value = Column(Unicode(64), nullable=False)
