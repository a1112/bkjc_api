# coding: utf-8
from sqlalchemy import BigInteger, Column, Integer, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Defect(Base):
    __tablename__ = 'defect'

    ID = Column(BigInteger, primary_key=True, comment='')
    defectNo = Column(BigInteger, nullable=False, comment='')
    steelID = Column("SteelID",VARCHAR(64), index=True)
    steelintop = Column(Integer, comment='')
    steelinleft = Column(Integer, comment='')
    steelinright = Column(Integer, comment='')
    classno = Column(Integer, comment='')
    Top = Column(Integer, comment='')
    defectLen = Column(Integer, comment='')
    defectwidth = Column(Integer, comment='')
    imageNo = Column(Integer, comment='')
