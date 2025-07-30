import requests
import time
from datetime import datetime
from config import steelLevelUrl
from ..Base.module import SteelProject, DefectProject


def steelList(num, start_id) -> list[SteelProject]:
    url_ = f"{steelLevelUrl}/steelList/{num}/{start_id}"
    print(url_)
    jsonData = requests.get(url_).json()

    return [SteelProject(data) for data in jsonData]


def searchByData(startData, endData):
    if isinstance(startData, datetime):
        startData = startData.strftime("%Y-%m-%d %H:%M:%S")
    if isinstance(endData, datetime):
        endData = endData.strftime("%Y-%m-%d %H:%M:%S")
    url_ = f"{steelLevelUrl}/searchByDate/{startData}/{endData}"
    print(url_)
    jsonData = requests.get(url_).json()
    return [SteelProject(data) for data in jsonData]


def getDefectList(seqNo) -> list[DefectProject]:
    jsonData = requests.get(f"{steelLevelUrl}/getDefectView/{seqNo}").json()
    return [DefectProject(defect) for defect in jsonData["up"]["defectList"] + jsonData["down"]["defectList"]]


def getDefectDict() -> dict:
    jsonData = requests.get(f"{steelLevelUrl}/DefectDict").json()
    return {item["id"]: item for item in jsonData}


if  __name__=="__main__":
    print(searchByData("2024-05-1 0:48:26","2024-05-2 0:48:26"))