
from core import app, tabelList
from workThread import workThreadDict


def getStateText(StateID:int):
    return {
        0: "未检测",
        1: "检测中",
        2: "报警"
    }[StateID]


def __getDeviceCurData__(deviceID:int):
    workThread = workThreadDict[deviceID]

    connection = workThread.connection
    return {
        "DeviceInfo": workThread.DeviceInfo,
        "SteelInfo": workThread.SteelInfo,
        "DeviceState": workThread.DeviceState,
        "DefectInfo": workThread.DefectInfo
    }


@app.get("/API/GetDeviceCurData.ashx")
def getDeviceCurData(DeviceID:int=0):
    DeviceID=str(DeviceID)
    if str(DeviceID) not in tabelList:
        return [
            __getDeviceCurData__(i)
            for i in tabelList.keys()
        ]
    return [__getDeviceCurData__(DeviceID)]

