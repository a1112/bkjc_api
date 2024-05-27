import json

from enum import Enum
from CameraStatus import getCameraInfo, getLightInfo

from core import app

from BKVisionListener.states.computer import ComputerStates


def formatObject(args):
    retDict_ = {}
    for k, v in args.items():
        if k == "family":
            retDict_[k] = int(v)
        elif isinstance(v, dict):
            retDict_[k] = formatObject(v)
        else:
            if isinstance(v, Enum):
                retDict_[k] = int(v)
            elif isinstance(v, (int, str, float)):
                retDict_[k] = v

            elif isinstance(v, list):
                retList = []
                for item in v:
                    retList.append(formatObject({"item": item})["item"])
                retDict_[k] = retList
            else:
                retDict = {}
                for k_ in v.__dir__():
                    if "_" in k_[0] or k_ in ["index", "count"]:
                        continue
                    retDict[k_] = getattr(v, k_)
                    # print(type(retDict[k_]))
                retDict_[k] = retDict
    return retDict_


@app.get("/serverStatus")
def getComputerStatus():
    computerDict = ComputerStates().__dict__()
    computerDict.update(formatObject({"camera": getCameraInfo(),
                                      "light": getLightInfo(),
                                      "pc": [{
                                          "ip": "127.0.3.100",
                                          "msg": "横切1号线"
                                      }]
                                      }))
    return computerDict


@app.get("/getAlarmSettings")
def getAlarmSettings():
    """
    获取到全部的设置参数 json
    """
    alarmFile = "alarm.json"
    alarmData = json.load(open(alarmFile, "r",encoding='utf-8'))
    return alarmData


@app.post("/setSettings")
def setSettings():
    """
    设置参数
    """


if __name__ == "__main__":
    status = getComputerStatus()
    print(status["disk"]["disk_io_counters"])
