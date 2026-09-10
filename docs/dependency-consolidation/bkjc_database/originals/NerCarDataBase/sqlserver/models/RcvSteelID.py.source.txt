# coding: utf-8
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class RcvSteelID(Base):
    __tablename__ = 'RcvSteelID'

    No = Column(Integer, primary_key=True)
    SLAB_ID = Column(String(50, 'Chinese_PRC_CI_AS'))
    SLAB_STATE = Column(String(25, 'Chinese_PRC_CI_AS'))
    PLATEID = Column(String(50, 'Chinese_PRC_CI_AS'))
    SIZE = Column(String(50, 'Chinese_PRC_CI_AS'))
