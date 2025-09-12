from bkjc_database import CONFIG

dbm = None

def _get_dbm_(config:CONFIG.DbConfigBase):
    if config.drive == "sqlserver":
        from .ss.dbi import SqlServer_3d0 as SqlObj
    else:
        from .ms.dbi import Mysql_4d0 as SqlObj
    return SqlObj()

def init_dbm(config:CONFIG.DbConfigBase):
    global dbm
    dbm_ = _get_dbm_(config)
    dbm = dbm_

def get_dbm(config:CONFIG.DbConfigBase,reGet=False):
    global dbm
    if reGet:
        return _get_dbm_(config)
    if not dbm:
        init_dbm(config)
    return dbm
init_dbm(CONFIG.DbConfig4d0())