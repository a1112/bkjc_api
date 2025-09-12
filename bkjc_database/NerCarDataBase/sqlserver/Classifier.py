#  encoding=utf-8
"""
"""
from bkjc_database.NerCarDataBase.BaseImport import *
from bkjc_database.NerCarDataBase.SqlBase import init
from bkjc_database.NerCarDataBase.core import beforeInit

databaseName = "Classifier"
engine: Engine
Base: automap_base
Session: sessionmaker
inspector: Inspector
table_names: list


def dbInit():
    global engine, Base, __Session__, inspector, table_names
    engine, Base, __Session__, inspector = init(databaseName)
    table_names = inspector.get_table_names()


dbInit()
