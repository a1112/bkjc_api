import logging

from bkjc_database.dbm import init_dbm

from bkjc_database import CONFIG

from subbProject.ApiForwarder import core

import multiprocessing
import time

def server_item(k, v):
    import uvicorn
    from core import mainApp as app
    import config
    FactoryID, DeviceName, DeviceIp = v.values()
    print(fr"DeviceIp {DeviceIp}")
    init_dbm(CONFIG.DbConfig4d0(DeviceIp))
    server_ip = "127.0.0.1"
    server_port = core.basePrt+int(k)

    try:
        import api
        uvicorn.run(app = app, host = server_ip, port = server_port)
    except TimeoutError as e:
        logging.error(fr"{DeviceName} {DeviceIp} 连接超时")


if __name__ == '__main__':
    processes=[]
    for k,v in core.tabelList.items():
        p = multiprocessing.Process(target=server_item, args=(k,v))
        processes.append(p)
        p.start()
    for p in processes:
        p.join()