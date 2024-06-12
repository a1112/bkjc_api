import time
from threading import Thread
from .DataSet import LevelSet
from subbProject.SteelLevel.DataSet import api
from .Base.module import SteelProject, DefectProject
from .configs import levelConfig
from . import toExcel
from . import AddUseDataThread


def levelBySteelProject(steelInfo):
    steelInfo: SteelProject
    defects = api.getDefectList(steelInfo.steelID)
    filterDefects = []
    for defect in defects:  # 查询缺陷
        defect: DefectProject
        defectLevel = levelConfig.defectLevel(defect, steelInfo)
        if defectLevel in ["L", "M", "S"]:
            defect.level = defectLevel
            # 严重缺陷
            LevelSet.addDefect(
                defect
            )
            filterDefects.append(defect)
    defList, levelMsg = levelConfig.steelLevel(steelInfo, filterDefects)
    steelInfo.level = defList, levelMsg
    # 获取 钢板等级


def main():
    # 循环访问
    maxSeq = LevelSet.getMaxSteelNo()  # 获取当前已经判断级别的 最大值
    getCount = 100
    oldSeqNo = maxSeq
    while True:
        for steelInfo in api.steelList(getCount, oldSeqNo):  # 查询钢板
            steelInfo: SteelProject
            if oldSeqNo == steelInfo.steelID:
                continue
            oldSeqNo = steelInfo.steelID
            levelBySteelProject(steelInfo)
            toExcel.append(steelInfo)
            LevelSet.addSteel(steelInfo)
            # defects = api.getDefectList(steelInfo.steelID)
            # filterDefects = []
            # for defect in defects:  # 查询缺陷
            #     defect: DefectProject
            #     defectLevel = levelConfig.defectLevel(defect, steelInfo)
            #     if defectLevel in ["L", "M", "S"]:
            #         defect.level = defectLevel
            #         # 严重缺陷
            #         LevelSet.addDefect(
            #             defect
            #         )
            #         filterDefects.append(defect)
            # defList, levelMsg = levelConfig.steelLevel(steelInfo, filterDefects)
            # steelInfo.level = defList, levelMsg
            #
            # toExcel.append(steelInfo)
            # LevelSet.addSteel(steelInfo)
            # # 获取 钢板等级
        time.sleep(5)


def startMain():
    Thread(target=main).start()


if __name__ == "__main__":
    main()