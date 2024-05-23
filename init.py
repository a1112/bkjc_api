import logging

formatStr = '%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
formatStr2 = '%(asctime)s - %(levelname)s: %(message)s'
logging.basicConfig(level=logging.INFO,
                    format=formatStr)

def initDataBase(info):
    from bkjc_database import core
    core.CONFIG.database_type=info["database_type"]
    print(info["upServer"])
    core.setBaseUrl(ip=info["upServer"], user=info["user"], password=info["password"], drive_=info["drive"])