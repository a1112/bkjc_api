#  encoding=utf-8
"""
操作数据库的核心功能模块
自动映射 DWQueue 数据库
"""
from bkjc_database.NerCarDataBase.BaseImport import *
from bkjc_database.NerCarDataBase.SqlBase import init

databaseName = "DWDiagnostics"

engine: Engine
Base: automap_base
Session: sessionmaker
__Session__: Session
inspector: Inspector
table_names: list

def get_db():
    db = __Session__()
    try:
        yield db
    finally:
        db.close()

def dbInit():
    global engine, Base, __Session__, session, inspector, table_names
    engine, Base, __Session__, session, inspector = init(databaseName)
    table_names = inspector.get_table_names()



dbInit()

def getTableList():
    pass

def drop_all():
    return Base.metadata.drop_all(engine)


def create_all():
    return Base.metadata.create_all(engine)

# logging.debug("开始尝试自动映射 {} 数据库".format(databaseName))
# for table_name in table_names:
#     table = try_get_table(Base, table_name)
#     exec("{} = table".format("auto"+table_name))
# logging.debug("完成自动映射 {} 数据库".format(databaseName))

# pdw_component_alerts_data = Base.classes.pdw_component_alerts_data
# pdw_component_health_data = Base.classes.pdw_component_health_data
# # pdw_component_health_data_lock = Base.classes.pdw_component_health_data_lock
# pdw_diagnostics_sessions = Base.classes.pdw_diagnostics_sessions
# pdw_errors = Base.classes.pdw_errors
# pdw_health_components_data = Base.classes.pdw_health_components_data
# pdw_loader_backup_run_details_data = Base.classes.pdw_loader_backup_run_details_data
# pdw_loader_backup_runs_data = Base.classes.pdw_loader_backup_runs_data
# pdw_loader_run_stages_data = Base.classes.pdw_loader_run_stages_data
# pdw_os_event_logs = Base.classes.pdw_os_event_logs
# pdw_performance_data = Base.classes.pdw_performance_data
# # pdw_population_template = Base.classes.pdw_population_template
