from bkjc_database.NerCarDataBase import core
if core.drive == "sqlserver":
    from .ss.dbi import SqlServer_3d0 as SqlObj
else:
    from .ms.dbi import Mysql_4d0 as SqlObj

dbm = SqlObj()
