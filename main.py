import uvicorn
from core import mainApp as app
import config

if __name__ == '__main__':
    if config.steelLevelEnable:
        import subbProject.SteelLevel.init
        subbProject.SteelLevel.init.initServer(app)
        import subbProject.SteelLevel.script
        import subbProject.SteelLevel.api
    if config.conditionMonitoringEnable:
        import subbProject.ConditionMonitoring.core
        subbProject.ConditionMonitoring.core.initServer(app)
        import subbProject.ConditionMonitoring.main

    if config.forwarder:
        from utils import forwarderServer
        forwarderServer.app.run(host=config.info["ip"], port=config.info["port"])
    elif config.plcForwarder:
        from utils import plcServer
        plcServer.app.run(host=config.info["ip"], port=config.info["port"])
    else:
        uvicorn.run(app=app, host=config.info["ip"], port=config.info["port"])

