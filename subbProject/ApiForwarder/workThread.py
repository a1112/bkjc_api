import time
from threading import Thread
from core import tabelList

import requests


class DeviceInfo:
    def __init__(self,id_):
        self.deviceId = id_
        self.factoryID=tabelList[id_]["FactoryID"]
        self.deviceName=tabelList[id_]["DeviceName"]
        if "ip" in tabelList[id_]:
            self.ip = tabelList[id_]["ip"]
        else:
            self.ip = ""
        self.port = str(getattr(tabelList[id_], "port", 809))


class WorkThread(Thread):
    def __init__(self,id_):
        self.deviceInfo = DeviceInfo(id_)
        self.hasIp=True
        self.connection = False
        self.SteelInfo = {
        # "//SteelID": "钢板号",
        "SteelID": "测试钢板号",
        # "//SteelLength": "钢板长度",
        "SteelLength": 10.23,
        # "//SteelWidth": "钢板宽度",
        "SteelWidth": 4.56,
        # "//SteelThick": "钢板厚度",
        "SteelThick": 0.05
    }
        self.DeviceInfo = {
        # "//FactoryID": "工厂号：1 一厂，2 二厂",
        "FactoryID": tabelList[str(id_)]["FactoryID"],
        # "//DeviceID": "设备编号 1 ~ 21",
        "DeviceID": int(id_),
        # "//DeviceName": "设备名称",
        "DeviceName": tabelList[str(id_)]["DeviceName"],
        # "Ip": self.deviceInfo.ip,
        # "Port": self.deviceInfo.port
    }
        self.DefectInfo = {
                # "//DefectID": "缺陷号码",
                "DefectID": 1,
                # "//DefectName": "缺陷名称",
                "DefectName": "划伤",
                # "//DefectGrade": "缺陷等级",
                "DefectGrade": 0,
                # "//DefectArea": "缺陷面积",
                "DefectArea": 0.34
            }
        self.DeviceState = {
        # "//StateID": "状态码： 0 未检测，1 检测中，2 报警 ",
        "StateID": 0,
        # "//StateText": "状态文本",
        "StateText": "未检测",
        # "//SpeedRoller": "辊道速度",
        "SpeedRoller": 0.0,
        }
        super().__init__()
        self.start()

    def _url_(self,sub_url):

        return "http://"+self.deviceInfo.ip+":"+self.deviceInfo.port+sub_url

    def testApi(self):
        url = self._url_("/")
        # print(url)
        req = requests.get(url)
        return True

    def getSteelInfo(self):
        url = self._url_("/steelGet/1/0")
        print(url)
        req = requests.get(url)
        return req.json()

    def run(self):
        while True:
            time.sleep(5)
            if not self.deviceInfo.ip:
                self.hasIp = False
                self.connection = False
                continue
            self.hasIp = True
            try:
                self.testApi()
            except Exception:
                self.connection = False
                continue
            try:
                jsonData = self.getSteelInfo()
                t = [{'id': 141620, 'steelNo': '4A193306000231', 'steelID': 141622, 'steelType': 'SY680T',
                      'steelLength': 8.87,
                      'steelWidth': 1.8, 'steelThick': 10.0, 'upDefectNum': 0, 'downDefectNum': 0, 'errorLevel': 0,
                      'grade': 1,
                      'detectTime': '2024-09-06 16:04:38', 'topLen': 8833, 'bottomLen': 8833}]
                self.SteelInfo["SteelID"] = jsonData[0]["steelNo"]
                self.SteelInfo["SteelLength"] = jsonData[0]["steelLength"]
                self.SteelInfo["SteelWidth"] = jsonData[0]["steelWidth"]
                self.SteelInfo["SteelThick"] = jsonData[0]["steelThick"]
            except Exception:
                pass

            self.connection = True

    def getDeviceInfo(self):
        return 0

    def getState(self):
        return 0


workThreadDict = {
    i:WorkThread(i)
    for i in tabelList.keys()
}


