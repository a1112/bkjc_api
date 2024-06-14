from pathlib import Path
from openpyxl import load_workbook

from collections import defaultdict

from subbProject.SteelLevel.configs.DataRead import LevelDataGet
from ..Base.module import DefectProject, SteelProject
from ..configs.DefectClass import defectClass2LevelDefectClass
from config import xlsxFile

# 打开 Excel 文件

baseTabelName = "缺陷规则表"


def getLevel(items):
    return items


def decodeDefectSheet(name, data):
    defectLevelDict = {0: {
        "id": 0,
        "name": "背景",
        "msg": "",
        "L": "",
        "M": "",
        "S": ""
    }}
    for line in data[4:]:
        try:
            if name == "默认规则":
                defectLevelDict[line[0]] = {
                    "id": int(line[0]),
                    "name": line[1],
                    "msg": line[2],
                    "L": getLevel(line[6:10]),
                    "M": getLevel(line[10:14]),
                    "S": getLevel(line[14:18])
                }
            else:
                defectLevelDict[line[0]] = {
                    "id": int(line[0]),
                    "name": line[1],
                    "msg": line[2],
                    "L": getLevel(line[3:7]),
                    "M": getLevel(line[7:11]),
                    "S": getLevel(line[11:15])
                }
        except:
            pass
    return defectLevelDict


def decodeSteelSheet(name, data):
    steelLevelDict = {}
    for line in data[4:]:
        try:
            if name == "默认规则":
                steelLevelDict[line[0]] = {
                    "id": int(line[0]),
                    "name": line[1],
                    "msg": line[2],
                    1: getLevel(line[15:18]),
                    2: getLevel(line[18:21]),
                    3: getLevel(line[21:24])
                }
            else:
                steelLevelDict[line[0]] = {
                    "id": int(line[0]),
                    "name": line[1],
                    "msg": line[2],
                    1: getLevel(line[15:18]),
                    2: getLevel(line[18:21]),
                    3: getLevel(line[21:24])
                }
        except:
            pass
    return steelLevelDict


class DefectLevelConfig:

    def __init__(self, name, data):
        self.name = name
        self.data = data
        # self.defectDict={}

        self.defectLevelDict = decodeDefectSheet(name, data)
        self.defectLevelConfig = None

    def setDefectLevelConfig(self, defectLevelConfig):
        self.defectLevelConfig = defectLevelConfig

    def defectLevel(self, defect, steelInfo):
        defectClass = defectClass2LevelDefectClass(defect.defectID)
        print(defect.defectID)
        print(self.defectLevelDict[defectClass])
        for levelLevel in ["S", "M", "L"]:
            if defectClass not in self.defectLevelDict:
                continue
            levelConfig = self.defectLevelDict[defectClass][levelLevel]
            if defectClass == 0:
                return "L"
            if not levelConfig[-1] and self.name != "默认规则":
                levelConfig = self.defectLevelConfig.defectLevelConfig.defectLevelDict[defectClass][levelLevel]
            code = levelConfig[-1]
            if code:
                return "L"
        return "L"


class SteelLevelConfig:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        if name == "默认规则":
            self.steelTypes = ""
        else:
            self.steelTypes = self.decodeTypes(self.data[1][15])
        self.defectLevelConfig = DefectLevelConfig(name, data)
        self.steelLevelDict = decodeSteelSheet(name, data)

    def setDefectLevelConfig(self, defectLevelConfig):
        self.defectLevelConfig.setDefectLevelConfig(defectLevelConfig)

    def decodeTypes(self, dataLine: str):
        dataLine = dataLine.replace("\n", "", 999)
        dataLine = dataLine.replace(" ", "", 999)
        for sqItem in [":", "："]:
            if sqItem in dataLine:
                dataLine = dataLine.split(sqItem)[1]
        for sqItem in [",", "，", "、"]:
            if sqItem in dataLine:
                dataLine = dataLine.split(sqItem)
        return dataLine

    def isCurrentType(self, steelType):
        # 是否为当前判级钢板
        for st in self.steelTypes:
            if st in steelType:
                return True
        return False

    def steelLevel(self, steelInfo, filterDefects):
        print(f"filterDefects {len(filterDefects)}")
        defect: DefectProject
        steelInfo: SteelProject
        if not filterDefects:
            return [], "无缺陷"
        else:
            defList = []
            for defect in filterDefects:
                defect: DefectProject
                defectLevel = self.defectLevelConfig.defectLevel(defect, steelInfo)
                defectClass = defectClass2LevelDefectClass(defect.defectID)
                if defectClass == 0:
                    continue
                for levelIndex, level in enumerate(["L", "M", "S"]):
                    if defectLevel == level:
                        code = self.steelLevelDict[defectClass][levelIndex + 1]
                        print( self.steelLevelDict[defectClass])
                        code1 = code[0]
                        print(code1)
                        # if code1 is None:
                        #     continue
                        # if "不允许" in code1:
                        #     defList.append({
                        #         "level": level,
                        #         "name": self.steelLevelDict[defectClass]["name"],
                        #         "id": self.steelLevelDict[defectClass]["id"],
                        #         "defect": defect,
                        #         "width": defect.width,
                        #         "height": defect.height,
                        #         "msg": "",
                        #     })

                        defList.append({
                            "level": level,
                            "name": self.steelLevelDict[defectClass]["name"],
                            "id": self.steelLevelDict[defectClass]["id"],
                            "defect": defect,
                            "width": defect.width,
                            "height": defect.height,
                            "msg": "",
                        })
        # input()
        return defList, self.toMsgString(defList)

    def toMsgString(self, defList):
        _defList = defaultdict(list)
        for defect in defList:
            _defList[defect["name"]].append(defect)

        if defList:
            msg = ""
            for key, item in _defList.items():
                levelCounts = defaultdict(int)
                for defItem in item:
                    levelCounts[defItem["level"]] += 1
                levelMsg = ""
                for lev in ["L", "M", "S"]:
                    if lev in levelCounts:
                        levelMsg += f"{lev}: {levelCounts[lev]}"
                msg += f"[{item[0]['name']}：{len(item)} {levelMsg}] "
            return msg
        else:
            return "无影响判级缺陷"

    def getInfo(self):
        return {
            "name": self.name,
            "steelLevel": self.steelLevelDict,
            "defectLevel": self.defectLevelConfig.defectLevelDict
        }

    def defectLevel(self, defect, steelInfo):
        defect: DefectProject
        steelInfo: SteelProject
        return self.defectLevelConfig.defectLevel(defect, steelInfo)


class LevelConfig:
    def __init__(self):
        levelDatas = LevelDataGet()

        self.SteelLevelConfigList: list[SteelLevelConfig] = []
        data = []
        for name in levelDatas:
            if name == '缺陷规则表':
                data = levelDatas[name]
                self.defectLevelDict = decodeDefectSheet(name, data)
            else:
                self.decodeSteelSheet(name,levelDatas[name])
        for steelLevel in self.SteelLevelConfigList:
            data = levelDatas["缺陷规则表"]
            steelLevel.setDefectLevelConfig(SteelLevelConfig("默认规则", data))

    def decodeSteelSheet(self, name,data):
        # 解析 steel
        slc = SteelLevelConfig(name, data)
        self.SteelLevelConfigList.append(slc)

        def decodeSteelType(typeStr: str):
            types = typeStr.replace("\n", "").split("：")[1].split("等")[0].split("、")
            return types

        steelTypes = decodeSteelType(data[1][15])
        steelLevelDict = {
        }
        for line in data[6:]:
            steelLevelDict[int(line[0])] = {
                "id": int(line[0]),
                "name": line[1],
                "msg": line[2],
                "L": getLevel(line[6:10]),
                "M": getLevel(line[10:14]),
                "S": getLevel(line[14:18]),
                "code": getLevel(line[14:18]),
                "HQ": {},
                "RCL": {}
            }

    # print(steelLevelDict)

    def defectLevel(self, defect, steelInfo):
        defect: DefectProject
        steelInfo: SteelProject
        # 进行判级
        for steelLevel in self.SteelLevelConfigList:
            if steelLevel.isCurrentType(steelInfo.steelType):
                return steelLevel.defectLevel(defect, steelInfo)
        else:
            raise

    def steelLevel(self, steelInfo, filterDefects):
        steelInfo: SteelProject
        if not steelInfo.steelType:
            return [], "无法判断"
        # 进行判级#
        filterDefects: list[DefectProject]
        print(filterDefects)
        for steelLevel in self.SteelLevelConfigList:
            if steelLevel.isCurrentType(steelInfo.steelType):
                steelLevel = steelLevel.steelLevel(steelInfo, filterDefects)
                print(steelLevel)
                return steelLevel
        raise

    def getAllLevelTabel(self):
        return [tabel.getInfo() for tabel in self.SteelLevelConfigList]


if __name__ == "__main__":
    levelConfig = LevelConfig(str((Path(__file__).parent.parent / xlsxFile)))
else:
    levelConfig = LevelConfig()


def getLevelTabel():
    return levelConfig.getAllLevelTabel()
