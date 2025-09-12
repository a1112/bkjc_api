#  encoding = utf-8
"""
SQL server 系统表
"""
from sqlalchemy import text

from bkjc_database.property.DataBaseInterFace import DbItem
from bkjc_database.SqlBase import init  # , try_get_table
databaseName = "master"


class Master(DbItem):

    def __init__(self):
        super().__init__(databaseName)

    @property
    def database_names(self):
        """数据库名称列表"""
        with self.Session() as session:
            return [database_name[0] for database_name in session.execute(text("SELECT name FROM sys.databases")).fetchall()]


database_names = Master().database_names
