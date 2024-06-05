import uvicorn
from core import mainApp as app
import config
import pymssql

if __name__ == '__main__':
    if config.steelLevelEnable:
        import subbProject.SteelLevel.init
        subbProject.SteelLevel.init.initServer(app)
        import subbProject.SteelLevel.main
        import subbProject.SteelLevel.api
    if config.conditionMonitoringEnable:
        import subbProject.ConditionMonitoring.core
        subbProject.ConditionMonitoring.core.initServer(app)
        import subbProject.ConditionMonitoring.main

    if not config.forwarder:
        import api
        uvicorn.run(app=app, host=config.info["ip"], port=config.info["port"])
    else:
        import forwarderServer
        forwarderServer.app.run(host=config.info["ip"], port=config.info["port"])
