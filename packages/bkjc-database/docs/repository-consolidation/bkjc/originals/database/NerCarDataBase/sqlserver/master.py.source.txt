#  encoding = utf-8
"""
SQL server 系统表
"""

from bkjc_database.NerCarDataBase.SqlBase import init  # , try_get_table
databaseName = "master"
engine, Base, Session, session, inspector = init(databaseName)
table_names = inspector.get_table_names()
database_names = [database_name[0] for database_name in session.execute("SELECT name FROM sys.databases").fetchall()]
# for table_name in table_names:
#     table = try_get_table(Base, table_name)
#     exec("{} = table".format(table_name))
