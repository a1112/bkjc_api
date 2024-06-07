# from collections import defaultdict
# from ConfigRead import levelConfig
# from DataSet.api import getDefectDict
import json
from pathlib import Path
import config
# defectDict = getDefectDict()
# print(defectDict)
# print(levelConfig.defectLevelDict)
var = [
    {
        "name": "未命名",
        "color": "#00ff40",
        "id": 0,
        "grade": 0
    },
    {
        "name": "划伤",
        "color": "#ff8040",
        "id": 1,
        "grade": 0
    },
    {
        "name": "凹坑",
        "color": "#c9a536",
        "id": 2,
        "grade": 0
    },
    {
        "name": "结疤",
        "color": "#c65539",
        "id": 3,
        "grade": 0
    },
    {
        "name": "氧化铁皮",
        "color": "#38c772",
        "id": 4,
        "grade": 0
    },
    {
        "name": "边裂",
        "color": "#36c966",
        "id": 5,
        "grade": 0
    },
    {
        "name": "辊印",
        "color": "#43bca0",
        "id": 6,
        "grade": 0
    },
    {
        "name": "油污",
        "color": "#94b847",
        "id": 7,
        "grade": 0
    },
    {
        "name": "擦伤",
        "color": "#bc7c43",
        "id": 8,
        "grade": 0
    },
    {
        "name": "舌尾印",
        "color": "#43bc6d",
        "id": 9,
        "grade": 0
    },
    {
        "name": "压痕",
        "color": "#425c7d",
        "id": 10,
        "grade": 0
    },
    {
        "name": "挫伤",
        "color": "#219e95",
        "id": 11,
        "grade": 0
    },
    {
        "name": "丸料凹坑",
        "color": "#0080c0",
        "id": 12,
        "grade": 0
    },
    {
        "name": "氧化物凹坑",
        "color": "#00ff00",
        "id": 13,
        "grade": 0
    },
    {
        "name": "夹杂",
        "color": "#ff0080",
        "id": 14,
        "grade": 0
    }
]

class DefectCheckList:
    pass


def defectClass2LevelDefectClassInfo():
    jsFile = config.get_config_path("LevelTabel.json")
    print(jsFile)
    jsData = json.load(Path(jsFile).open("r", encoding="utf-8"))
    return jsData


def defectClass2LevelDefectClass(defectClass):
    try:
        return {
            1: 9,
            2: 16,
            3: 2,
            4: 5,
            5: 3,
            6: 7,
            7: 11,
            8: 9,
            10: 14,
            11: 13,
            12: 16,
            13: 16
            # 14
        }[defectClass]
    except:
        return 0
