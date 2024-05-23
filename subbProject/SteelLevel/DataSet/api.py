import requests
import time

from config import steelLevelUrl
from ..Base.module import SteelProject, DefectProject


def steelList(num, start_id) -> list[SteelProject]:
    url_ = f"{steelLevelUrl}/steelList/{num}/{start_id}"
    jsonData = requests.get(url_).json()
    print(url_)
    return [SteelProject(data) for data in jsonData]


def getDefectList(seqNo) -> list[DefectProject]:
    jsonData = requests.get(f"{steelLevelUrl}/getDefectView/{seqNo}").json()
    return [DefectProject(defect) for defect in jsonData["up"]["defectList"] + jsonData["down"]["defectList"]]


def getDefectDict() -> dict:
    jsonData = requests.get(f"{steelLevelUrl}/DefectDict").json()
    return {item["id"]: item for item in jsonData}
