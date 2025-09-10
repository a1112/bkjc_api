from pathlib import Path
from openpyxl import load_workbook

from collections import defaultdict
from subbProject.SteelLevel.configs.DataRead import LevelDataGet
from configs.DefectClass import defectClass2LevelDefectClass
from config import xlsxFile

# 打开 Excel 文件

baseTabelName = "缺陷规则表"
glob_defectLevelConfig = None


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
            if name == "缺陷规则表":
                defectLevelDict[line[0]] = {
                    "id": int(line[0]),
                    "name": line[1],
                    "msg": line[2],
                    "L": getLevel(line[6:10]),
                    "M": getLevel(line[10:14]),
                    "S": getLevel(line[14:18])
                }
                print(getLevel(line[6:10]))
                print(getLevel(line[10:14]))
                print(getLevel(line[14:18]))


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
    if name == "缺陷规则表":
        lines = data[4:]
    else:
        lines = data[4:]
    for line in lines:
        try:
            if name == "缺陷规则表":
                steelLevelDict[line[0]] = {
                    "id": int(line[0]),
                    "name": line[1],
                    "msg": line[2],
                    1: getLevel(line[7:11]),
                    2: getLevel(line[1:15]),
                    3: getLevel(line[15:19])
                }

            else:
                if line[0] is None:
                    continue
                steelLevelDict[line[0]] = {
                    "id": int(line[0]),
                    "name": line[1],
                    "msg": line[2],
                    1: getLevel(line[15:18]),
                    2: getLevel(line[18:21]),
                    3: getLevel(line[21:24])
                }
        except:
            raise
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

    def getDefectLevel(self, defectClass, levelLevel):
        print("getDefectLevel")
        print(self.name)
        print(defectClass, levelLevel)
        print(self.defectLevelConfig)
        print(self.defectLevelConfig.defectLevelDict[defectClass][levelLevel])
        return self.defectLevelConfig.defectLevelDict[defectClass][levelLevel]

    def defectLevel(self, defect, steelInfo):
        global glob_defectLevelConfig
        defectClass = defectClass2LevelDefectClass(defect.defectID)
        print(self.name)
        print(defect.defectID)
        print(self.defectLevelDict[defectClass])
        for levelLevel in ["S", "M", "L"]:
            if defectClass not in self.defectLevelDict:
                raise
            levelConfig = self.defectLevelDict[defectClass][levelLevel]
            print(levelConfig)
            if defectClass == 0:
                return "L"
            code = levelConfig[-1]
            if code is None:
                print(fr"{self.name} {levelLevel} 未设置规则，使用默认规则。 ")
                print(glob_defectLevelConfig.defectLevelConfig.defectLevelDict)
                levelConfig = glob_defectLevelConfig.defectLevelConfig.defectLevelDict[defectClass][levelLevel]
            # levelConfig = glob_defectLevelConfig.defectLevelConfig.defectLevelDict[defectClass][levelLevel]
            code = levelConfig
            msg = fr"{self.name} {levelLevel} {self.defectLevelDict[defectClass]["name"]}"
            levelCode = self.levelDefectByCode(defect, code, msg)
            print(levelCode)
            if levelCode:
                return levelLevel
            return "L"
        return "L"

    def levelDefectByCode(self, defect, code, msg):
        defect: "DefectProject"
        print("缺陷判级　" + msg)
        print(code)
        levelCode = code[-1]
        print(levelCode)
        height_mm = defect.rightInSteel - defect.leftInSteel
        width_mm = defect.bottomInSteel - defect.topInSteel
        area_mm = height_mm * width_mm
        height_cm = height_mm / 10
        width_cm = width_mm / 10
        area_cm = height_cm * width_cm
        print(fr"width {width_mm} mm")
        print(fr"height {height_mm} mm")


        if eval(levelCode):
            return True
        return False


class SteelLevelConfig:
    def __init__(self, name, data):
        self.name = name
        self.data = data
        self.defectLevelConfig = DefectLevelConfig(name, data)

        self.steelLevelDict = decodeSteelSheet(name, data)
        if name == "缺陷规则表":
            self.steelTypes = ""
        else:
            self.steelTypes = self.decodeTypes(self.data[1][15])

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

    def getDefectLevel(self, defectClass, levelLevel):
        return self.defectLevelConfig.getDefectLevel(defectClass, levelLevel)

    def steelLevel(self, steelInfo, filterDefects):
        print(f"filterDefects {len(filterDefects)}")
        defect: "DefectProject"
        steelInfo: "SteelProject"
        if not filterDefects:
            return [], ["无缺陷", "无缺陷"], ""
        else:
            defList = []
            for defect in filterDefects:
                defect: "DefectProject"
                defectLevel = self.defectLevelConfig.defectLevel(defect, steelInfo)
                defectClass = defectClass2LevelDefectClass(defect.defectID)
                if defectClass == 0:
                    continue
                for levelIndex, level in enumerate(["L", "M", "S"]):
                    if defectLevel == level:
                        code = self.steelLevelDict[defectClass][levelIndex + 1]
                        print(self.steelLevelDict[defectClass])
                        code1 = code[0]
                        print(code1)
                        defList.append({
                            "level": level,
                            "name": self.steelLevelDict[defectClass]["name"],
                            "id": self.steelLevelDict[defectClass]["id"],
                            "defect": defect,
                            "width": defect.width,
                            "height": defect.height,
                            "msg": "",
                        })

        levelStr = self.leveSteelByCode(defList, self.steelLevelDict, "---")

        # input()
        return defList, self.toMsgString(defList), levelStr

    def leveSteelByCode(self, defect_list, code_list, msg):
        defect: "DefectProject"
        print(code_list)
        defect_dict = defaultdict(dict)

        steelLevelStr = ""
        for defect in defect_list:
            if not defect_dict[defect["id"]]:
                defect_dict[defect["id"]]["L"] = []
                defect_dict[defect["id"]]["S"] = []
                defect_dict[defect["id"]]["M"] = []
            defect_dict[defect["id"]][defect["level"]].append(defect)
        print(defect_dict)
        for defect_id in defect_dict:
            print(defect_id)
            steelLevelCodeItem = code_list[defect_id]

            for item_1, item_2 in zip([1, 2, 3], ["L", "M", "S"]):
                steelLevelCode = steelLevelCodeItem[item_1]
                defects = defect_dict[defect_id][item_2]
                print(steelLevelCode)
                print(defects)
                if steelLevelCode[0] is None:
                    print("未设立规则 {}".format(steelLevelCode))
                    continue
                elif "不允许" in steelLevelCode[0]:
                    if defects:
                        steelLevelStr += defects[0]["name"] + " " + item_2 + "级缺陷不允许 " + "数量" + str(
                            len(defects))
        return steelLevelStr

    def toMsgString(self, defList):
        _defList = defaultdict(list)
        for defect in defList:
            _defList[defect["name"]].append(defect)
        if defList:
            msg = ["", ""]
            for key, item in _defList.items():
                levelCounts = defaultdict(int)
                for defItem in item:
                    levelCounts[defItem["level"]] += 1
                levelMsg = ""
                for lev in ["L", "M", "S"]:
                    if lev in levelCounts:
                        levelMsg += f"{lev}: {levelCounts[lev]}"

                updefects = []
                doundefects = []
                if item[0]["defect"].bmIndex < 1:
                    msg[0] += f"[{item[0]['name']}：{len(item)} {levelMsg}] "
                else:
                    msg[1] += f"[{item[0]['name']}：{len(item)} {levelMsg}] "
            return msg
        else:
            return ["无影响判级缺陷", "无影响判级缺陷"]

    def getInfo(self):
        return {
            "name": self.name,
            "steelLevel": self.steelLevelDict,
            "defectLevel": self.defectLevelConfig.defectLevelDict
        }

    def defectLevel(self, defect, steelInfo):
        defect: "DefectProject"
        steelInfo: "SteelProject"
        return self.defectLevelConfig.defectLevel(defect, steelInfo)


class LevelConfig:
    def __init__(self):
        levelDatas = LevelDataGet()
        global glob_defectLevelConfig
        self.SteelLevelConfigList: list[SteelLevelConfig] = []
        data = []
        for name in levelDatas:
            if name == '缺陷规则表':
                data = levelDatas[name]
                self.defectLevelDict = decodeDefectSheet(name, data)
                glob_defectLevelConfig = SteelLevelConfig(name, data)
            else:
                self.decodeSteelSheet(name, levelDatas[name])
        # for steelLevel in self.SteelLevelConfigList:
        #     data = levelDatas["缺陷规则表"]
        #     steelLevel.setDefectLevelConfig(SteelLevelConfig("缺陷规则表", data))

    def decodeSteelSheet(self, name, data):
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
        defect: "DefectProject"
        steelInfo: "SteelProject"
        # 进行判级
        for steelLevel in self.SteelLevelConfigList:
            if steelLevel.isCurrentType(steelInfo.steelType):
                return steelLevel.defectLevel(defect, steelInfo)
        else:
            raise

    def steelLevel(self, steelInfo, filterDefects):
        steelInfo: "SteelProject"
        if not steelInfo.steelType:
            return [], ["", ""], ""
        # 进行判级#
        filterDefects: list["DefectProject"]
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
