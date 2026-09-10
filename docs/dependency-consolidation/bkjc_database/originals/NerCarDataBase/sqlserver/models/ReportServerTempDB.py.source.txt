# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, ForeignKey, Index, Integer, LargeBinary, SmallInteger, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import BIT, IMAGE, NTEXT, TINYINT, UNIQUEIDENTIFIER
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class ChunkData(Base):
    __tablename__ = 'ChunkData'
    __table_args__ = (
        Index('IX_ChunkData', 'SnapshotDataID', 'ChunkName', 'ChunkType', unique=True),
    )

    ChunkID = Column(UNIQUEIDENTIFIER, primary_key=True)
    SnapshotDataID = Column(UNIQUEIDENTIFIER, nullable=False)
    ChunkFlags = Column(TINYINT)
    ChunkName = Column(Unicode(260))
    ChunkType = Column(Integer)
    Version = Column(SmallInteger)
    MimeType = Column(Unicode(260))
    Content = Column(IMAGE)


class ChunkSegmentMapping(Base):
    __tablename__ = 'ChunkSegmentMapping'
    __table_args__ = (
        Index('UNIQ_ChunkId_StartByte', 'ChunkId', 'StartByte', 'ActualByteCount', 'LogicalByteCount', unique=True),
    )

    ChunkId = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False)
    SegmentId = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False, index=True)
    StartByte = Column(BigInteger, nullable=False)
    LogicalByteCount = Column(Integer, nullable=False)
    ActualByteCount = Column(Integer, nullable=False)


class DBUpgradeHistory(Base):
    __tablename__ = 'DBUpgradeHistory'

    UpgradeID = Column(BigInteger, primary_key=True)
    DbVersion = Column(Unicode(25))
    User = Column(Unicode(128), server_default=text("(suser_sname())"))
    DateTime = Column(DateTime, server_default=text("(getdate())"))


class ExecutionCache(Base):
    __tablename__ = 'ExecutionCache'
    __table_args__ = (
        Index('IX_ExecutionCache', 'ReportID', 'AbsoluteExpiration', 'SnapshotDataID', unique=True),
        Index('IX_CacheLookup', 'ReportID', 'ParamsHash', 'AbsoluteExpiration', 'SnapshotDataID')
    )

    ExecutionCacheID = Column(UNIQUEIDENTIFIER, primary_key=True)
    ReportID = Column(UNIQUEIDENTIFIER, nullable=False)
    ExpirationFlags = Column(Integer, nullable=False)
    AbsoluteExpiration = Column(DateTime)
    RelativeExpiration = Column(Integer)
    SnapshotDataID = Column(UNIQUEIDENTIFIER, nullable=False, index=True)
    LastUsedTime = Column(DateTime, nullable=False, server_default=text("(getdate())"))
    ParamsHash = Column(Integer, nullable=False, server_default=text("((0))"))


class PersistedStream(Base):
    __tablename__ = 'PersistedStream'

    SessionID = Column(String(32, 'Latin1_General_CI_AS_KS_WS'), primary_key=True, nullable=False)
    Index = Column(Integer, primary_key=True, nullable=False)
    Content = Column(IMAGE)
    Name = Column(Unicode(260))
    MimeType = Column(Unicode(260))
    Extension = Column(Unicode(260))
    Encoding = Column(Unicode(260))
    Error = Column(Unicode(512))
    RefCount = Column(Integer, nullable=False)
    ExpirationDate = Column(DateTime, nullable=False)


class Segment(Base):
    __tablename__ = 'Segment'

    SegmentId = Column(UNIQUEIDENTIFIER, primary_key=True, unique=True, server_default=text("(newsequentialid())"))
    Content = Column(LargeBinary)


class SegmentedChunk(Base):
    __tablename__ = 'SegmentedChunk'
    __table_args__ = (
        Index('UNIQ_SnapshotChunkMapping', 'SnapshotDataId', 'ChunkType', 'ChunkName', 'ChunkFlags', 'ChunkId', unique=True),
        Index('IX_ChunkId_SnapshotDataId', 'ChunkId', 'SnapshotDataId')
    )

    ChunkId = Column(UNIQUEIDENTIFIER, nullable=False, server_default=text("(newsequentialid())"))
    SnapshotDataId = Column(UNIQUEIDENTIFIER, nullable=False)
    ChunkFlags = Column(TINYINT, nullable=False)
    ChunkName = Column(Unicode(260), nullable=False)
    ChunkType = Column(Integer, nullable=False)
    Version = Column(SmallInteger, nullable=False)
    MimeType = Column(Unicode(260))
    Machine = Column(Unicode(512), nullable=False)
    SegmentedChunkId = Column(BigInteger, primary_key=True)


t_SessionData = Table(
    'SessionData', metadata,
    Column('SessionID', String(32, 'Latin1_General_CI_AS_KS_WS'), nullable=False, unique=True),
    Column('CompiledDefinition', UNIQUEIDENTIFIER),
    Column('SnapshotDataID', UNIQUEIDENTIFIER, index=True),
    Column('IsPermanentSnapshot', BIT),
    Column('ReportPath', Unicode(464)),
    Column('Timeout', Integer, nullable=False),
    Column('AutoRefreshSeconds', Integer),
    Column('Expiration', DateTime, nullable=False, index=True),
    Column('ShowHideInfo', IMAGE),
    Column('DataSourceInfo', IMAGE),
    Column('OwnerID', UNIQUEIDENTIFIER, nullable=False),
    Column('EffectiveParams', NTEXT(1073741823)),
    Column('CreationTime', DateTime, nullable=False),
    Column('HasInteractivity', BIT),
    Column('SnapshotExpirationDate', DateTime),
    Column('HistoryDate', DateTime),
    Column('PageHeight', Float(53)),
    Column('PageWidth', Float(53)),
    Column('TopMargin', Float(53)),
    Column('BottomMargin', Float(53)),
    Column('LeftMargin', Float(53)),
    Column('RightMargin', Float(53)),
    Column('AwaitingFirstExecution', BIT),
    Column('EditSessionID', String(32, 'Latin1_General_CI_AS_KS_WS'), index=True),
    Column('DataSetInfo', LargeBinary),
    Column('SitePath', Unicode(440)),
    Column('SiteZone', Integer, nullable=False, server_default=text("((0))")),
    Column('ReportDefinitionPath', Unicode(464))
)


t_SessionLock = Table(
    'SessionLock', metadata,
    Column('SessionID', String(32, 'Latin1_General_CI_AS_KS_WS'), nullable=False, unique=True),
    Column('LockVersion', Integer, nullable=False, server_default=text("((0))"))
)


t_SnapshotData = Table(
    'SnapshotData', metadata,
    Column('SnapshotDataID', UNIQUEIDENTIFIER, nullable=False),
    Column('CreatedDate', DateTime, nullable=False),
    Column('ParamsHash', Integer),
    Column('QueryParams', NTEXT(1073741823)),
    Column('EffectiveParams', NTEXT(1073741823)),
    Column('Description', Unicode(512)),
    Column('DependsOnUser', BIT),
    Column('PermanentRefcount', Integer, nullable=False),
    Column('TransientRefcount', Integer, nullable=False),
    Column('ExpirationDate', DateTime, nullable=False),
    Column('PageCount', Integer),
    Column('HasDocMap', BIT),
    Column('Machine', Unicode(512), nullable=False),
    Column('PaginationMode', SmallInteger),
    Column('ProcessingFlags', Integer),
    Column('IsCached', BIT, server_default=text("((0))")),
    Index('IX_SnapshotCleaning', 'PermanentRefcount', 'TransientRefcount', 'Machine'),
    Index('IX_SnapshotData', 'SnapshotDataID', 'ParamsHash'),
    Index('IS_SnapshotExpiration', 'PermanentRefcount', 'ExpirationDate')
)


class TempCatalog(Base):
    __tablename__ = 'TempCatalog'

    EditSessionID = Column(String(32, 'Latin1_General_CI_AS_KS_WS'), primary_key=True, nullable=False)
    TempCatalogID = Column(UNIQUEIDENTIFIER, nullable=False, unique=True)
    ContextPath = Column(Unicode(425), primary_key=True, nullable=False)
    Name = Column(Unicode(425), nullable=False)
    Content = Column(LargeBinary)
    Description = Column(Unicode)
    Intermediate = Column(UNIQUEIDENTIFIER)
    IntermediateIsPermanent = Column(BIT, nullable=False, server_default=text("((0))"))
    Property = Column(Unicode)
    Parameter = Column(Unicode)
    OwnerID = Column(UNIQUEIDENTIFIER, nullable=False)
    CreationTime = Column(DateTime, nullable=False)
    ExpirationTime = Column(DateTime, nullable=False, index=True)
    DataCacheHash = Column(LargeBinary(64))


class TempDataSets(Base):
    __tablename__ = 'TempDataSets'
    __table_args__ = (
        Index('IX_TempDataSet_ItemID_Name', 'ItemID', 'Name'),
    )

    ID = Column(UNIQUEIDENTIFIER, primary_key=True)
    ItemID = Column(ForeignKey('TempCatalog.TempCatalogID'), nullable=False)
    LinkID = Column(UNIQUEIDENTIFIER, index=True)
    Name = Column(Unicode(260), nullable=False)

    TempCatalog = relationship('TempCatalog')


class TempDataSources(Base):
    __tablename__ = 'TempDataSources'

    DSID = Column(UNIQUEIDENTIFIER, primary_key=True)
    ItemID = Column(ForeignKey('TempCatalog.TempCatalogID'), nullable=False, index=True)
    Name = Column(Unicode(260))
    Extension = Column(Unicode(260))
    Link = Column(UNIQUEIDENTIFIER)
    CredentialRetrieval = Column(Integer)
    Prompt = Column(NTEXT(1073741823))
    ConnectionString = Column(IMAGE)
    OriginalConnectionString = Column(IMAGE)
    OriginalConnectStringExpressionBased = Column(BIT)
    UserName = Column(IMAGE)
    Password = Column(IMAGE)
    Flags = Column(Integer)
    Version = Column(Integer, nullable=False)

    TempCatalog = relationship('TempCatalog')
