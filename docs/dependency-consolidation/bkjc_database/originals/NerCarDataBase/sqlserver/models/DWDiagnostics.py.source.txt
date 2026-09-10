# coding: utf-8
from sqlalchemy import BigInteger, Column, DateTime, Float, Index, Integer, Table, Unicode
from sqlalchemy.dialects.mssql import BIT, DATETIME2, UNIQUEIDENTIFIER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


t_dm_pdw_component_health_active_alerts = Table(
    'dm_pdw_component_health_active_alerts', metadata,
    Column('pdw_node_id', Integer, nullable=False),
    Column('component_id', Integer, nullable=False),
    Column('component_instance_id', Unicode(255), nullable=False),
    Column('alert_id', Integer, nullable=False),
    Column('alert_instance_id', Unicode(255), nullable=False),
    Column('current_value', Unicode(255)),
    Column('previous_value', Unicode(255)),
    Column('create_time', DATETIME2, nullable=False)
)


t_dm_pdw_component_health_alerts = Table(
    'dm_pdw_component_health_alerts', metadata,
    Column('pdw_node_id', Integer, nullable=False),
    Column('component_id', Integer, nullable=False),
    Column('component_instance_id', Unicode(255), nullable=False),
    Column('alert_id', Integer, nullable=False),
    Column('alert_instance_id', Unicode(255), nullable=False),
    Column('current_value', Unicode(255)),
    Column('previous_value', Unicode(255)),
    Column('create_time', DATETIME2, nullable=False)
)


t_dm_pdw_component_health_status = Table(
    'dm_pdw_component_health_status', metadata,
    Column('pdw_node_id', Integer, nullable=False),
    Column('component_id', Integer, nullable=False),
    Column('group_id', Integer, nullable=False),
    Column('component_instance_id', Unicode(255), nullable=False),
    Column('property_id', Integer, nullable=False),
    Column('property_value', Unicode(32)),
    Column('update_time', DATETIME2, nullable=False)
)


t_dm_pdw_os_performance_counters = Table(
    'dm_pdw_os_performance_counters', metadata,
    Column('machine_name', Unicode(255), nullable=False),
    Column('pdw_node_id', Integer, nullable=False),
    Column('counter_name', Unicode(255), nullable=False),
    Column('counter_category', Unicode(255), nullable=False),
    Column('instance_name', Unicode(255)),
    Column('counter_value', Float(53), nullable=False),
    Column('last_update_time', DATETIME2, nullable=False)
)


class PdwComponentAlertsData(Base):
    __tablename__ = 'pdw_component_alerts_data'

    CustomContext_Node_Id = Column('CustomContext.Node.Id', Integer, nullable=False)
    CustomContext_InstanceId = Column('CustomContext.InstanceId', Unicode(255), nullable=False)
    CustomContext_ComponentInstanceId = Column('CustomContext.ComponentInstanceId', Unicode(255), nullable=False)
    CustomContext_AlertId = Column('CustomContext.AlertId', Integer, nullable=False)
    CustomContext_ParentId = Column('CustomContext.ParentId', Integer, nullable=False)
    CustomContext_CurrentValue = Column('CustomContext.CurrentValue', Unicode(255))
    CustomContext_PreviousValue = Column('CustomContext.PreviousValue', Unicode(255))
    DateTimePublished = Column(DATETIME2, nullable=False)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False, index=True)
    Builtin_RowId = Column(UNIQUEIDENTIFIER, primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)


class PdwComponentHealthData(Base):
    __tablename__ = 'pdw_component_health_data'
    __table_args__ = (
        Index('IX_pdw_component_health_data_SourceNameNodeId', 'CustomContext.SourceName', 'CustomContext.CurrentNode.Id'),
    )

    CustomContext_SourceName = Column('CustomContext.SourceName', Unicode(128), nullable=False)
    CustomContext_CurrentNode_Id = Column('CustomContext.CurrentNode.Id', Integer, nullable=False)
    CustomContext_Node_Id = Column('CustomContext.Node.Id', Integer, nullable=False)
    CustomContext_ComponentId = Column('CustomContext.ComponentId', Integer, nullable=False)
    CustomContext_ParentId = Column('CustomContext.ParentId', Integer, nullable=False)
    CustomContext_InstanceId = Column('CustomContext.InstanceId', Unicode(255), nullable=False)
    CustomContext_DetailId = Column('CustomContext.DetailId', Integer, nullable=False)
    CustomContext_DetailValue = Column('CustomContext.DetailValue', Unicode(255))
    DateTimePublished = Column(DATETIME2, nullable=False)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False, index=True)
    Builtin_RowId = Column(Unicode(255), primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)
    CustomContext_ClusterId = Column('CustomContext.ClusterId', Unicode(255), nullable=False)


t_pdw_component_health_data_lock = Table(
    'pdw_component_health_data_lock', metadata,
    Column('CustomContext.SourceName', Unicode(255), nullable=False),
    Column('CustomContext.ClusterId', Unicode(255), nullable=False)
)


t_pdw_diag_sessions = Table(
    'pdw_diag_sessions', metadata,
    Column('name', Unicode(255), nullable=False),
    Column('xml_data', Unicode(4000)),
    Column('is_active', BIT, nullable=False),
    Column('host_address', Unicode(255), nullable=False),
    Column('principal_id', Integer, nullable=False),
    Column('database_id', Integer)
)


class PdwDiagnosticsSessions(Base):
    __tablename__ = 'pdw_diagnostics_sessions'

    session_name = Column(Unicode(255), primary_key=True)
    definition = Column(Unicode, nullable=False)
    host_address = Column(Unicode(255), nullable=False)
    owner_id = Column(Unicode(255))
    table_name = Column(Unicode(255), nullable=False)
    is_enabled = Column(BIT, nullable=False)


class PdwErrors(Base):
    __tablename__ = 'pdw_errors'

    MachineName = Column(Unicode(255), nullable=False)
    CurrentNode_Id = Column('CurrentNode.Id', Integer, nullable=False)
    CurrentNode_Type = Column('CurrentNode.Type', Unicode(32), nullable=False)
    FullName = Column(Unicode(255), nullable=False)
    ThreadId = Column(Integer, nullable=False)
    ProcessId = Column(Integer, nullable=False)
    ModuleName = Column(Unicode(255), nullable=False)
    ErrorId = Column(Unicode(36), nullable=False)
    Session_SessionId = Column('Session.SessionId', Unicode(32))
    Query_QueryId = Column('Query.QueryId', Unicode(36))
    CustomContext_SPID = Column('CustomContext.SPID', Integer)
    Message = Column(Unicode)
    DateTimePublished = Column(DATETIME2, nullable=False)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False, index=True)
    Builtin_RowId = Column(UNIQUEIDENTIFIER, primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)


t_pdw_health_alerts = Table(
    'pdw_health_alerts', metadata,
    Column('alert_id', Integer, nullable=False),
    Column('component_id', Integer, nullable=False),
    Column('alert_name', Unicode(255), nullable=False),
    Column('state', Unicode(32), nullable=False),
    Column('severity', Unicode(32), nullable=False),
    Column('type', Unicode(32), nullable=False),
    Column('description', Unicode(4000)),
    Column('condition', Unicode(255)),
    Column('status', Unicode(32)),
    Column('condition_value', BIT)
)


t_pdw_health_component_groups = Table(
    'pdw_health_component_groups', metadata,
    Column('group_id', Integer, nullable=False),
    Column('group_name', Unicode(255), nullable=False)
)


t_pdw_health_component_properties = Table(
    'pdw_health_component_properties', metadata,
    Column('property_id', Integer, nullable=False),
    Column('component_id', Integer, nullable=False),
    Column('property_name', Unicode(255), nullable=False),
    Column('physical_name', Unicode(255), nullable=False),
    Column('is_key', BIT, nullable=False)
)


t_pdw_health_component_status_mappings = Table(
    'pdw_health_component_status_mappings', metadata,
    Column('property_id', Integer, nullable=False),
    Column('component_id', Integer, nullable=False),
    Column('physical_name', Unicode(255), nullable=False),
    Column('logical_name', Unicode(255))
)


t_pdw_health_components = Table(
    'pdw_health_components', metadata,
    Column('component_id', Integer, nullable=False),
    Column('group_id', Integer, nullable=False),
    Column('component_name', Unicode(255), nullable=False)
)


class PdwHealthComponentsData(Base):
    __tablename__ = 'pdw_health_components_data'

    CustomContext_ComponentId = Column('CustomContext.ComponentId', Integer, nullable=False)
    CustomContext_ParentId = Column('CustomContext.ParentId', Integer, nullable=False)
    CustomContext_ComponentName = Column('CustomContext.ComponentName', Unicode(255), nullable=False)
    CustomContext_ComponentType = Column('CustomContext.ComponentType', Unicode(255), nullable=False)
    CustomContext_Description = Column('CustomContext.Description', Unicode(4000))
    CustomContext_AlertType = Column('CustomContext.AlertType', Unicode(32), nullable=False)
    CustomContext_AlertState = Column('CustomContext.AlertState', Unicode(32), nullable=False)
    CustomContext_AlertSeverity = Column('CustomContext.AlertSeverity', Unicode(32), nullable=False)
    CustomContext_AlertThresholdCondition = Column('CustomContext.AlertThresholdCondition', Unicode(255))
    CustomContext_AlertThresholdConditionValue = Column('CustomContext.AlertThresholdConditionValue', BIT)
    CustomContext_Status = Column('CustomContext.Status', Unicode(255))
    CustomContext_ComponentWmiNamespace = Column('CustomContext.ComponentWmiNamespace', Unicode(255))
    CustomContext_ComponentWmiClass = Column('CustomContext.ComponentWmiClass', Unicode)
    CustomContext_LogicalName = Column('CustomContext.LogicalName', Unicode(255), nullable=False)
    CustomContext_PhysicalName = Column('CustomContext.PhysicalName', Unicode(255), nullable=False)
    CustomContext_IsKeyProperty = Column('CustomContext.IsKeyProperty', BIT, nullable=False)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False)
    Builtin_RowId = Column(Unicode(255), primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)


class PdwLoaderBackupRunDetailsData(Base):
    __tablename__ = 'pdw_loader_backup_run_details_data'

    CustomContext_Run_Id = Column('CustomContext.Run_Id', Integer, nullable=False)
    CustomContext_Pdw_Node_Id = Column('CustomContext.Pdw_Node_Id', Integer, nullable=False)
    CustomContext_Status = Column('CustomContext.Status', Unicode(16))
    CustomContext_Start_Time = Column('CustomContext.Start_Time', DateTime)
    CustomContext_End_Time = Column('CustomContext.End_Time', DateTime)
    CustomContext_Total_Elapsed_time = Column('CustomContext.Total_Elapsed_time', Integer)
    CustomContext_Progress = Column('CustomContext.Progress', Integer)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False, index=True)
    Builtin_RowId = Column(Unicode(255), primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)


class PdwLoaderBackupRunsData(Base):
    __tablename__ = 'pdw_loader_backup_runs_data'

    CustomContext_Run_Id = Column('CustomContext.Run_Id', Integer, nullable=False)
    CustomContext_Name = Column('CustomContext.Name', Unicode(255))
    CustomContext_Submit_Time = Column('CustomContext.Submit_Time', DateTime)
    CustomContext_StartTime = Column('CustomContext.StartTime', DateTime)
    CustomContext_End_Time = Column('CustomContext.End_Time', DateTime)
    CustomContext_Total_Elapsed_Time = Column('CustomContext.Total_Elapsed_Time', Integer)
    CustomContext_Operation_Type = Column('CustomContext.Operation_Type', Unicode(16))
    CustomContext_Mode = Column('CustomContext.Mode', Unicode(16))
    CustomContext_Database = Column('CustomContext.Database', Unicode(255))
    CustomContext_Table = Column('CustomContext.Table', Unicode(255))
    CustomContext_Session_Id = Column('CustomContext.Session_Id', Unicode(255))
    CustomContext_Request_Id = Column('CustomContext.Request_Id', Unicode(255))
    CustomContext_Status = Column('CustomContext.Status', Unicode(16))
    CustomContext_Progress = Column('CustomContext.Progress', Integer)
    CustomContext_Command = Column('CustomContext.Command', Unicode(4000))
    CustomContext_Rows_Processed = Column('CustomContext.Rows_Processed', BigInteger)
    CustomContext_Rows_Rejected = Column('CustomContext.Rows_Rejected', BigInteger)
    CustomContext_Rows_Inserted = Column('CustomContext.Rows_Inserted', BigInteger)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False, index=True)
    Builtin_RowId = Column(Unicode(255), primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)
    CustomContext_PrincipalId = Column('CustomContext.PrincipalId', Integer)


class PdwLoaderRunStagesData(Base):
    __tablename__ = 'pdw_loader_run_stages_data'

    CustomContext_Run_Id = Column('CustomContext.Run_Id', Integer, nullable=False)
    CustomContext_Stage = Column('CustomContext.Stage', Unicode(30))
    CustomContext_Request_Id = Column('CustomContext.Request_Id', Unicode(255))
    CustomContext_Status = Column('CustomContext.Status', Unicode(16))
    CustomContext_Start_Time = Column('CustomContext.Start_Time', DateTime)
    CustomContext_End_Time = Column('CustomContext.End_Time', DateTime)
    CustomContext_Total_Elapsed_time = Column('CustomContext.Total_Elapsed_time', Integer)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False, index=True)
    Builtin_RowId = Column(Unicode(255), primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)


class PdwOsEventLogs(Base):
    __tablename__ = 'pdw_os_event_logs'

    MachineName = Column(Unicode(255), nullable=False)
    CurrentNode_Id = Column('CurrentNode.Id', Integer, nullable=False)
    CurrentNode_Type = Column('CurrentNode.Type', Unicode(32), nullable=False)
    CustomContext_LogName = Column('CustomContext.LogName', Unicode(255), nullable=False)
    CustomContext_SourceName = Column('CustomContext.SourceName', Unicode(255), nullable=False)
    CustomContext_EntryId = Column('CustomContext.EntryId', Unicode(255), nullable=False)
    CustomContext_EntryType = Column('CustomContext.EntryType', Unicode(255), nullable=False)
    CustomContext_TimeGeneated = Column('CustomContext.TimeGeneated', DATETIME2, nullable=False)
    CustomContext_TimeWritten = Column('CustomContext.TimeWritten', DATETIME2, nullable=False)
    Message = Column(Unicode)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False, index=True)
    Builtin_RowId = Column(UNIQUEIDENTIFIER, primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)


class PdwPerformanceData(Base):
    __tablename__ = 'pdw_performance_data'

    MachineName = Column(Unicode(255), nullable=False)
    CustomContext_Node_Id = Column('CustomContext.Node.Id', Integer, nullable=False)
    CustomContext_CounterValue = Column('CustomContext.CounterValue', Float(53), nullable=False)
    CustomContext_CounterName = Column('CustomContext.CounterName', Unicode(255), nullable=False)
    CustomContext_CounterCategory = Column('CustomContext.CounterCategory', Unicode(255), nullable=False)
    CustomContext_InstanceName = Column('CustomContext.InstanceName', Unicode(255))
    DateTimePublished = Column(DATETIME2, nullable=False)
    Builtin_DateTimeEntryCreated = Column(DATETIME2, nullable=False, index=True)
    Builtin_RowId = Column(Unicode(255), primary_key=True)
    Builtin_HasData = Column(BIT, nullable=False)


t_pdw_population_template = Table(
    'pdw_population_template', metadata,
    Column('temp_col', BIT)
)
