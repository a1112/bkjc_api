# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Index, Integer, LargeBinary, Table, Unicode
from sqlalchemy.dialects.mssql import BIT, UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class MessageQueue(Base):
    __tablename__ = 'MessageQueue'
    __table_args__ = (
        Index('IX_ActiveMessages', 'QueueName', 'IsActive', 'Priority', 'DateActive', 'Sequence', 'MessageId', unique=True),
    )

    MessageId = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False)
    QueueName = Column(Unicode(255), primary_key=True, nullable=False)
    Priority = Column(Integer, nullable=False)
    DateActive = Column(DateTime, nullable=False)
    IsActive = Column(BIT, nullable=False)
    MessageBody = Column(LargeBinary, nullable=False)
    DateCreated = Column(DateTime, nullable=False)
    Sequence = Column(BigInteger, nullable=False)
    RequestId = Column(UNIQUEIDENTIFIER)
    DateRequestExpires = Column(DateTime)
    CorrelationId = Column(UNIQUEIDENTIFIER)
    LookupField1 = Column(Unicode(255), index=True)
    LookupField2 = Column(Unicode(255), index=True)
    LookupField3 = Column(Unicode(255), index=True)


t_TransactionState = Table(
    'TransactionState', metadata,
    Column('OperationId', UNIQUEIDENTIFIER, nullable=False, unique=True),
    Column('TransactionId', UNIQUEIDENTIFIER, nullable=False),
    Column('State', Integer, nullable=False),
    Column('DateCreated', DateTime, nullable=False)
)
