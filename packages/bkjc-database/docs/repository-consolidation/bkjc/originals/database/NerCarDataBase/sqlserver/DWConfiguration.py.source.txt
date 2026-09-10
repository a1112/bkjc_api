#  encoding=utf-8
"""
自动映射 DWQueue 数据库
"""
from bkjc_database.NerCarDataBase.BaseImport import *
if driveType == "mysql":
    from .mysqlModels.DWConfiguration import *
else:
    pass
databaseName = "DWConfiguration"

engine: Engine
Base: automap_base
Session: sessionmaker
session: Session
inspector: Inspector
table_names: list


def dbInit():
    global engine, Base, Session, session, inspector, table_names
    engine, Base, Session, session, inspector = init(databaseName)
    table_names = inspector.get_table_names()


if beforeInit:
    dbInit()
# logging.debug("开始尝试自动映射 {} 数据库".format(databaseName))
# for table_name in table_names:
#     table = try_get_table(Base, table_name)
#     exec("{} = table".format("auto"+table_name))
# logging.debug("完成自动映射 {} 数据库".format(databaseName))

#  自动映射
# compute_node = Base.classes.compute_node
# configuration_properties = Base.classes.configuration_properties
# database_file = Base.classes.database_file
# distribution = Base.classes.distribution
# filegroup = Base.classes.filegroup
# node = Base.classes.node
# pdw_sp_configure = Base.classes.pdw_sp_configure
# version_history = Base.classes.version_history
