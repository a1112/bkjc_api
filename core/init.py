import logging

formatStr = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
formatStr2 = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=formatStr)


def initDataBase(info):
    from bkjc_database import core
    from bkjc_database.dbm import init_dbm
    # info['port'] is the HTTP listening port, not the database port.
    settings = dict(info, port=info.get("db_port", 0))
    return init_dbm(core.configure_database(settings))
