# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, ForeignKey, Index, Integer, LargeBinary, SmallInteger, String, Table, Unicode, text
from sqlalchemy.dialects.mssql import BIT, IMAGE, NTEXT, TINYINT, UNIQUEIDENTIFIER, XML
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_Batch = Table(
    'Batch', metadata,
    Column('BatchID', UNIQUEIDENTIFIER, nullable=False),
    Column('AddedOn', DateTime, nullable=False, index=True),
    Column('Action', String(32, 'Latin1_General_CI_AS_KS_WS'), nullable=False),
    Column('Item', Unicode(425)),
    Column('Parent', Unicode(425)),
    Column('Param', Unicode(425)),
    Column('BoolParam', BIT),
    Column('Content', IMAGE),
    Column('Properties', NTEXT(1073741823)),
    Index('IX_Batch', 'BatchID', 'AddedOn')
)


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


class ConfigurationInfo(Base):
    __tablename__ = 'ConfigurationInfo'

    ConfigInfoID = Column(UNIQUEIDENTIFIER, primary_key=True)
    Name = Column(Unicode(260), nullable=False, unique=True)
    Value = Column(NTEXT(1073741823), nullable=False)


class DBUpgradeHistory(Base):
    __tablename__ = 'DBUpgradeHistory'

    UpgradeID = Column(BigInteger, primary_key=True)
    DbVersion = Column(Unicode(25))
    User = Column(Unicode(128), server_default=text("(suser_sname())"))
    DateTime = Column(DateTime, server_default=text("(getdate())"))


class Event(Base):
    __tablename__ = 'Event'

    EventID = Column(UNIQUEIDENTIFIER, primary_key=True)
    EventType = Column(Unicode(260), nullable=False)
    EventData = Column(Unicode(260))
    TimeEntered = Column(DateTime, nullable=False, index=True)
    ProcessStart = Column(DateTime, index=True)
    ProcessHeartbeat = Column(DateTime)
    BatchID = Column(UNIQUEIDENTIFIER)


t_ExecutionLog = Table(
    'ExecutionLog', metadata,
    Column('InstanceName', Unicode(38), nullable=False),
    Column('ReportID', UNIQUEIDENTIFIER),
    Column('UserName', Unicode(260)),
    Column('RequestType', BIT),
    Column('Format', Unicode(26)),
    Column('Parameters', NTEXT(1073741823)),
    Column('TimeStart', DateTime, nullable=False),
    Column('TimeEnd', DateTime, nullable=False),
    Column('TimeDataRetrieval', Integer, nullable=False),
    Column('TimeProcessing', Integer, nullable=False),
    Column('TimeRendering', Integer, nullable=False),
    Column('Source', Integer, nullable=False),
    Column('Status', Unicode(40), nullable=False),
    Column('ByteCount', BigInteger, nullable=False),
    Column('RowCount', BigInteger, nullable=False)
)


t_ExecutionLog2 = Table(
    'ExecutionLog2', metadata,
    Column('InstanceName', Unicode(38), nullable=False),
    Column('ReportPath', Unicode(425)),
    Column('UserName', Unicode(260)),
    Column('ExecutionId', Unicode(64)),
    Column('RequestType', String(12, 'Latin1_General_CI_AS_KS_WS'), nullable=False),
    Column('Format', Unicode(26)),
    Column('Parameters', NTEXT(1073741823)),
    Column('ReportAction', String(21, 'Latin1_General_CI_AS_KS_WS'), nullable=False),
    Column('TimeStart', DateTime, nullable=False),
    Column('TimeEnd', DateTime, nullable=False),
    Column('TimeDataRetrieval', Integer, nullable=False),
    Column('TimeProcessing', Integer, nullable=False),
    Column('TimeRendering', Integer, nullable=False),
    Column('Source', String(8, 'Latin1_General_CI_AS_KS_WS'), nullable=False),
    Column('Status', Unicode(40), nullable=False),
    Column('ByteCount', BigInteger, nullable=False),
    Column('RowCount', BigInteger, nullable=False),
    Column('AdditionalInfo', XML)
)


t_ExecutionLog3 = Table(
    'ExecutionLog3', metadata,
    Column('InstanceName', Unicode(38), nullable=False),
    Column('ItemPath', Unicode(425)),
    Column('UserName', Unicode(260)),
    Column('ExecutionId', Unicode(64)),
    Column('RequestType', String(13, 'Latin1_General_CI_AS_KS_WS'), nullable=False),
    Column('Format', Unicode(26)),
    Column('Parameters', NTEXT(1073741823)),
    Column('ItemAction', String(21, 'Latin1_General_CI_AS_KS_WS'), nullable=False),
    Column('TimeStart', DateTime, nullable=False),
    Column('TimeEnd', DateTime, nullable=False),
    Column('TimeDataRetrieval', Integer, nullable=False),
    Column('TimeProcessing', Integer, nullable=False),
    Column('TimeRendering', Integer, nullable=False),
    Column('Source', String(8, 'Latin1_General_CI_AS_KS_WS'), nullable=False),
    Column('Status', Unicode(40), nullable=False),
    Column('ByteCount', BigInteger, nullable=False),
    Column('RowCount', BigInteger, nullable=False),
    Column('AdditionalInfo', XML)
)


class ExecutionLogStorage(Base):
    __tablename__ = 'ExecutionLogStorage'
    __table_args__ = (
        Index('IX_ExecutionLog', 'TimeStart', 'LogEntryId'),
    )

    LogEntryId = Column(BigInteger, primary_key=True)
    InstanceName = Column(Unicode(38), nullable=False)
    ReportID = Column(UNIQUEIDENTIFIER)
    UserName = Column(Unicode(260))
    ExecutionId = Column(Unicode(64))
    RequestType = Column(TINYINT, nullable=False)
    Format = Column(Unicode(26))
    Parameters = Column(NTEXT(1073741823))
    ReportAction = Column(TINYINT)
    TimeStart = Column(DateTime, nullable=False)
    TimeEnd = Column(DateTime, nullable=False)
    TimeDataRetrieval = Column(Integer, nullable=False)
    TimeProcessing = Column(Integer, nullable=False)
    TimeRendering = Column(Integer, nullable=False)
    Source = Column(TINYINT, nullable=False)
    Status = Column(Unicode(40), nullable=False)
    ByteCount = Column(BigInteger, nullable=False)
    RowCount = Column(BigInteger, nullable=False)
    AdditionalInfo = Column(XML)


t_ExtendedDataSets = Table(
    'ExtendedDataSets', metadata,
    Column('ID', UNIQUEIDENTIFIER, nullable=False),
    Column('LinkID', UNIQUEIDENTIFIER),
    Column('Name', Unicode(260), nullable=False),
    Column('ItemID', UNIQUEIDENTIFIER, nullable=False)
)


t_ExtendedDataSources = Table(
    'ExtendedDataSources', metadata,
    Column('DSID', UNIQUEIDENTIFIER, nullable=False),
    Column('ItemID', UNIQUEIDENTIFIER),
    Column('SubscriptionID', UNIQUEIDENTIFIER),
    Column('Name', Unicode(260)),
    Column('Extension', Unicode(260)),
    Column('Link', UNIQUEIDENTIFIER),
    Column('CredentialRetrieval', Integer),
    Column('Prompt', NTEXT(1073741823)),
    Column('ConnectionString', IMAGE),
    Column('OriginalConnectionString', IMAGE),
    Column('OriginalConnectStringExpressionBased', BIT),
    Column('UserName', IMAGE),
    Column('Password', IMAGE),
    Column('Flags', Integer),
    Column('Version', Integer, nullable=False)
)


class History(Base):
    __tablename__ = 'History'
    __table_args__ = (
        Index('IX_History', 'ReportID', 'SnapshotDate', unique=True),
    )

    HistoryID = Column(UNIQUEIDENTIFIER, primary_key=True)
    ReportID = Column(UNIQUEIDENTIFIER, nullable=False)
    SnapshotDataID = Column(UNIQUEIDENTIFIER, nullable=False, index=True)
    SnapshotDate = Column(DateTime, nullable=False)


class Keys(Base):
    __tablename__ = 'Keys'

    MachineName = Column(Unicode(256))
    InstallationID = Column(UNIQUEIDENTIFIER, primary_key=True, nullable=False)
    InstanceName = Column(Unicode(32))
    Client = Column(Integer, primary_key=True, nullable=False)
    PublicKey = Column(IMAGE)
    SymmetricKey = Column(IMAGE)


class Policies(Base):
    __tablename__ = 'Policies'

    PolicyID = Column(UNIQUEIDENTIFIER, primary_key=True)
    PolicyFlag = Column(TINYINT)


class Roles(Base):
    __tablename__ = 'Roles'

    RoleID = Column(UNIQUEIDENTIFIER, primary_key=True)
    RoleName = Column(Unicode(260), nullable=False, unique=True)
    Description = Column(Unicode(512))
    TaskMask = Column(Unicode(32), nullable=False)
    RoleFlags = Column(TINYINT, nullable=False)


class RunningJobs(Base):
    __tablename__ = 'RunningJobs'
    __table_args__ = (
        Index('IX_RunningJobsStatus', 'ComputerName', 'JobType'),
    )

    JobID = Column(Unicode(32), primary_key=True)
    StartDate = Column(DateTime, nullable=False)
    ComputerName = Column(Unicode(32), nullable=False)
    RequestName = Column(Unicode(425), nullable=False)
    RequestPath = Column(Unicode(425), nullable=False)
    UserId = Column(UNIQUEIDENTIFIER, nullable=False)
    Description = Column(NTEXT(1073741823))
    Timeout = Column(Integer, nullable=False)
    JobAction = Column(SmallInteger, nullable=False)
    JobType = Column(SmallInteger, nullable=False)
    JobStatus = Column(SmallInteger, nullable=False)


class Segment(Base):
    __tablename__ = 'Segment'

    SegmentId = Column(UNIQUEIDENTIFIER, primary_key=True, unique=True, server_default=text("(newsequentialid())"))
    Content = Column(LargeBinary)


class SegmentedChunk(Base):
    __tablename__ = 'SegmentedChunk'
    __table_args__ = (
        Index('IX_ChunkId_SnapshotDataId', 'ChunkId', 'SnapshotDataId'),
        Index('UNIQ_SnapshotChunkMapping', 'SnapshotDataId', 'ChunkType', 'ChunkName', 'ChunkFlags', 'ChunkId', unique=True)
    )

    ChunkId = Column(UNIQUEIDENTIFIER, nullable=False, server_default=text("(newsequentialid())"))
    SnapshotDataId = Column(UNIQUEIDENTIFIER, nullable=False)
    ChunkFlags = Column(TINYINT, nullable=False)
    ChunkName = Column(Unicode(260), nullable=False)
    ChunkType = Column(Integer, nullable=False)
    Version = Column(SmallInteger, nullable=False)
    MimeType = Column(Unicode(260))
    SegmentedChunkId = Column(BigInteger, primary_key=True)


class ServerParametersInstance(Base):
    __tablename__ = 'ServerParametersInstance'

    ServerParametersID = Column(Unicode(32), primary_key=True)
    ParentID = Column(Unicode(32))
    Path = Column(Unicode(425), nullable=False)
    CreateDate = Column(DateTime, nullable=False)
    ModifiedDate = Column(DateTime, nullable=False)
    Timeout = Column(Integer, nullable=False)
    Expiration = Column(DateTime, nullable=False, index=True)
    ParametersValues = Column(IMAGE, nullable=False)


class ServerUpgradeHistory(Base):
    __tablename__ = 'ServerUpgradeHistory'

    UpgradeID = Column(BigInteger, primary_key=True)
    ServerVersion = Column(Unicode(25))
    User = Column(Unicode(128), server_default=text("(suser_sname())"))
    DateTime = Column(DateTime, server_default=text("(getdate())"))


class SnapshotData(Base):
    __tablename__ = 'SnapshotData'

    SnapshotDataID = Column(UNIQUEIDENTIFIER, primary_key=True)
    CreatedDate = Column(DateTime, nullable=False)
    ParamsHash = Column(Integer)
    QueryParams = Column(NTEXT(1073741823))
    EffectiveParams = Column(NTEXT(1073741823))
    Description = Column(Unicode(512))
    DependsOnUser = Column(BIT)
    PermanentRefcount = Column(Integer, nullable=False, index=True)
    TransientRefcount = Column(Integer, nullable=False)
    ExpirationDate = Column(DateTime, nullable=False)
    PageCount = Column(Integer)
    HasDocMap = Column(BIT)
    PaginationMode = Column(SmallInteger)
    ProcessingFlags = Column(Integer)


class SubscriptionsBeingDeleted(Base):
    __tablename__ = 'SubscriptionsBeingDeleted'

    SubscriptionID = Column(UNIQUEIDENTIFIER, primary_key=True)
    CreationDate = Column(DateTime, nullable=False)


class UpgradeInfo(Base):
    __tablename__ = 'UpgradeInfo'

    Item = Column(Unicode(260), primary_key=True)
    Status = Column(Unicode(512))


class Users(Base):
    __tablename__ = 'Users'
    __table_args__ = (
        Index('IX_Users', 'Sid', 'AuthType', 'UserName', unique=True),
    )

    UserID = Column(UNIQUEIDENTIFIER, primary_key=True)
    Sid = Column(LargeBinary(85))
    UserType = Column(Integer, nullable=False)
    AuthType = Column(Integer, nullable=False)
    UserName = Column(Unicode(260))


class Catalog(Base):
    __tablename__ = 'Catalog'
    __table_args__ = (
        Index('IX_ComponentLookup', 'Type', 'ComponentID'),
    )

    ItemID = Column(UNIQUEIDENTIFIER, primary_key=True)
    Path = Column(Unicode(425), nullable=False, unique=True)
    Name = Column(Unicode(425), nullable=False)
    ParentID = Column(ForeignKey('Catalog.ItemID'), index=True)
    Type = Column(Integer, nullable=False)
    Content = Column(IMAGE)
    Intermediate = Column(UNIQUEIDENTIFIER)
    SnapshotDataID = Column(UNIQUEIDENTIFIER, index=True)
    LinkSourceID = Column(ForeignKey('Catalog.ItemID'), index=True)
    Property = Column(NTEXT(1073741823))
    Description = Column(Unicode(512))
    Hidden = Column(BIT)
    CreatedByID = Column(ForeignKey('Users.UserID'), nullable=False)
    CreationDate = Column(DateTime, nullable=False)
    ModifiedByID = Column(ForeignKey('Users.UserID'), nullable=False)
    ModifiedDate = Column(DateTime, nullable=False)
    MimeType = Column(Unicode(260))
    SnapshotLimit = Column(Integer)
    Parameter = Column(NTEXT(1073741823))
    PolicyID = Column(ForeignKey('Policies.PolicyID'), nullable=False)
    PolicyRoot = Column(BIT, nullable=False)
    ExecutionFlag = Column(Integer, nullable=False)
    ExecutionTime = Column(DateTime)
    SubType = Column(Unicode(128))
    ComponentID = Column(UNIQUEIDENTIFIER)

    Users = relationship('Users', primaryjoin='Catalog.CreatedByID == Users.UserID')
    parent = relationship('Catalog', remote_side=[ItemID], primaryjoin='Catalog.LinkSourceID == Catalog.ItemID')
    Users1 = relationship('Users', primaryjoin='Catalog.ModifiedByID == Users.UserID')
    parent1 = relationship('Catalog', remote_side=[ItemID], primaryjoin='Catalog.ParentID == Catalog.ItemID')
    Policies = relationship('Policies')


class ModelItemPolicy(Base):
    __tablename__ = 'ModelItemPolicy'
    __table_args__ = (
        Index('IX_ModelItemPolicy', 'CatalogItemID', 'ModelItemID'),
    )

    ID = Column(UNIQUEIDENTIFIER, primary_key=True)
    CatalogItemID = Column(UNIQUEIDENTIFIER, nullable=False)
    ModelItemID = Column(Unicode(425), nullable=False)
    PolicyID = Column(ForeignKey('Policies.PolicyID'), nullable=False)

    Policies = relationship('Policies')


class PolicyUserRole(Base):
    __tablename__ = 'PolicyUserRole'
    __table_args__ = (
        Index('IX_PolicyUserRole', 'RoleID', 'UserID', 'PolicyID', unique=True),
    )

    ID = Column(UNIQUEIDENTIFIER, primary_key=True)
    RoleID = Column(ForeignKey('Roles.RoleID'), nullable=False)
    UserID = Column(ForeignKey('Users.UserID'), nullable=False)
    PolicyID = Column(ForeignKey('Policies.PolicyID'), nullable=False)

    Policies = relationship('Policies')
    Roles = relationship('Roles')
    Users = relationship('Users')


class Schedule(Base):
    __tablename__ = 'Schedule'
    __table_args__ = (
        Index('IX_Schedule', 'Name', 'Path', unique=True),
    )

    ScheduleID = Column(UNIQUEIDENTIFIER, primary_key=True)
    Name = Column(Unicode(260), nullable=False)
    StartDate = Column(DateTime, nullable=False)
    Flags = Column(Integer, nullable=False)
    NextRunTime = Column(DateTime)
    LastRunTime = Column(DateTime)
    EndDate = Column(DateTime)
    RecurrenceType = Column(Integer)
    MinutesInterval = Column(Integer)
    DaysInterval = Column(Integer)
    WeeksInterval = Column(Integer)
    DaysOfWeek = Column(Integer)
    DaysOfMonth = Column(Integer)
    Month = Column(Integer)
    MonthlyWeek = Column(Integer)
    State = Column(Integer)
    LastRunStatus = Column(Unicode(260))
    ScheduledRunTimeout = Column(Integer)
    CreatedById = Column(ForeignKey('Users.UserID'), nullable=False)
    EventType = Column(Unicode(260), nullable=False)
    EventData = Column(Unicode(260))
    Type = Column(Integer, nullable=False)
    ConsistancyCheck = Column(DateTime)
    Path = Column(Unicode(260))

    Users = relationship('Users')


class SecData(Base):
    __tablename__ = 'SecData'
    __table_args__ = (
        Index('IX_SecData', 'PolicyID', 'AuthType', unique=True),
    )

    SecDataID = Column(UNIQUEIDENTIFIER, primary_key=True)
    PolicyID = Column(ForeignKey('Policies.PolicyID'), nullable=False)
    AuthType = Column(Integer, nullable=False)
    XmlDescription = Column(NTEXT(1073741823), nullable=False)
    NtSecDescPrimary = Column(IMAGE, nullable=False)
    NtSecDescSecondary = Column(NTEXT(1073741823))

    Policies = relationship('Policies')


class CachePolicy(Base):
    __tablename__ = 'CachePolicy'

    CachePolicyID = Column(UNIQUEIDENTIFIER, primary_key=True)
    ReportID = Column(ForeignKey('Catalog.ItemID'), nullable=False, unique=True)
    ExpirationFlags = Column(Integer, nullable=False)
    CacheExpiration = Column(Integer)

    Catalog = relationship('Catalog')


class DataSets(Base):
    __tablename__ = 'DataSets'
    __table_args__ = (
        Index('IX_DataSet_ItemID_Name', 'ItemID', 'Name'),
    )

    ID = Column(UNIQUEIDENTIFIER, primary_key=True)
    ItemID = Column(ForeignKey('Catalog.ItemID'), nullable=False)
    LinkID = Column(ForeignKey('Catalog.ItemID'), index=True)
    Name = Column(Unicode(260), nullable=False)

    Catalog = relationship('Catalog', primaryjoin='DataSets.ItemID == Catalog.ItemID')
    Catalog1 = relationship('Catalog', primaryjoin='DataSets.LinkID == Catalog.ItemID')


class DataSource(Base):
    __tablename__ = 'DataSource'

    DSID = Column(UNIQUEIDENTIFIER, primary_key=True)
    ItemID = Column(ForeignKey('Catalog.ItemID'), index=True)
    SubscriptionID = Column(UNIQUEIDENTIFIER, index=True)
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

    Catalog = relationship('Catalog')


class ModelDrill(Base):
    __tablename__ = 'ModelDrill'
    __table_args__ = (
        Index('IX_ModelDrillModelID', 'ModelDrillID', 'ModelID', 'ReportID', unique=True),
    )

    ModelDrillID = Column(UNIQUEIDENTIFIER, primary_key=True)
    ModelID = Column(ForeignKey('Catalog.ItemID'), nullable=False)
    ReportID = Column(ForeignKey('Catalog.ItemID'), nullable=False)
    ModelItemID = Column(Unicode(425), nullable=False)
    Type = Column(TINYINT, nullable=False)

    Catalog = relationship('Catalog', primaryjoin='ModelDrill.ModelID == Catalog.ItemID')
    Catalog1 = relationship('Catalog', primaryjoin='ModelDrill.ReportID == Catalog.ItemID')


t_ModelPerspective = Table(
    'ModelPerspective', metadata,
    Column('ID', UNIQUEIDENTIFIER, nullable=False),
    Column('ModelID', ForeignKey('Catalog.ItemID'), nullable=False, index=True),
    Column('PerspectiveID', NTEXT(1073741823), nullable=False),
    Column('PerspectiveName', NTEXT(1073741823)),
    Column('PerspectiveDescription', NTEXT(1073741823))
)


class Subscriptions(Base):
    __tablename__ = 'Subscriptions'

    SubscriptionID = Column(UNIQUEIDENTIFIER, primary_key=True)
    OwnerID = Column(ForeignKey('Users.UserID'), nullable=False)
    Report_OID = Column(ForeignKey('Catalog.ItemID'), nullable=False)
    Locale = Column(Unicode(128), nullable=False)
    InactiveFlags = Column(Integer, nullable=False)
    ExtensionSettings = Column(NTEXT(1073741823))
    ModifiedByID = Column(ForeignKey('Users.UserID'), nullable=False)
    ModifiedDate = Column(DateTime, nullable=False)
    Description = Column(Unicode(512))
    LastStatus = Column(Unicode(260))
    EventType = Column(Unicode(260), nullable=False)
    MatchData = Column(NTEXT(1073741823))
    LastRunTime = Column(DateTime)
    Parameters = Column(NTEXT(1073741823))
    DataSettings = Column(NTEXT(1073741823))
    DeliveryExtension = Column(Unicode(260))
    Version = Column(Integer, nullable=False)
    ReportZone = Column(Integer, nullable=False, server_default=text("((0))"))

    Users = relationship('Users', primaryjoin='Subscriptions.ModifiedByID == Users.UserID')
    Users1 = relationship('Users', primaryjoin='Subscriptions.OwnerID == Users.UserID')
    Catalog = relationship('Catalog')


class ActiveSubscriptions(Base):
    __tablename__ = 'ActiveSubscriptions'

    ActiveID = Column(UNIQUEIDENTIFIER, primary_key=True)
    SubscriptionID = Column(ForeignKey('Subscriptions.SubscriptionID'), nullable=False)
    TotalNotifications = Column(Integer)
    TotalSuccesses = Column(Integer, nullable=False)
    TotalFailures = Column(Integer, nullable=False)

    Subscriptions = relationship('Subscriptions')


class Notifications(Base):
    __tablename__ = 'Notifications'

    NotificationID = Column(UNIQUEIDENTIFIER, primary_key=True)
    SubscriptionID = Column(ForeignKey('Subscriptions.SubscriptionID'), nullable=False)
    ActivationID = Column(UNIQUEIDENTIFIER)
    ReportID = Column(UNIQUEIDENTIFIER, nullable=False)
    SnapShotDate = Column(DateTime)
    ExtensionSettings = Column(NTEXT(1073741823), nullable=False)
    Locale = Column(Unicode(128), nullable=False)
    Parameters = Column(NTEXT(1073741823))
    ProcessStart = Column(DateTime, index=True)
    NotificationEntered = Column(DateTime, nullable=False, index=True)
    ProcessAfter = Column(DateTime, index=True)
    Attempt = Column(Integer)
    SubscriptionLastRunTime = Column(DateTime, nullable=False)
    DeliveryExtension = Column(Unicode(260), nullable=False)
    SubscriptionOwnerID = Column(UNIQUEIDENTIFIER, nullable=False)
    IsDataDriven = Column(BIT, nullable=False)
    BatchID = Column(UNIQUEIDENTIFIER)
    ProcessHeartbeat = Column(DateTime)
    Version = Column(Integer, nullable=False)
    ReportZone = Column(Integer, nullable=False, server_default=text("((0))"))

    Subscriptions = relationship('Subscriptions')


t_ReportSchedule = Table(
    'ReportSchedule', metadata,
    Column('ScheduleID', ForeignKey('Schedule.ScheduleID'), nullable=False, index=True),
    Column('ReportID', ForeignKey('Catalog.ItemID'), nullable=False, index=True),
    Column('SubscriptionID', ForeignKey('Subscriptions.SubscriptionID'), index=True),
    Column('ReportAction', Integer, nullable=False)
)
