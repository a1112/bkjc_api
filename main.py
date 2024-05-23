import uvicorn
from core import mainApp as app
import config
import pymssql

if __name__ == '__main__':

    import subbProject.SteelLevel.main

    if not config.forwarder:
        import api
        uvicorn.run(app=app, host=config.info["ip"], port=config.info["port"])
    else:
        import forwarderServer
        forwarderServer.app.run(host=config.info["ip"],port=config.info["port"])