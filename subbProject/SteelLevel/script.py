import time
from  threading import Thread

from Base.module import DefectProject
from subbProject.SteelLevel.DataSet import api, LevelSet
from subbProject.SteelLevel import toExcel
from subbProject.SteelLevel.Base.module import SteelProject
from subbProject.SteelLevel.main import levelBySteelProject
from subbProject.ApiForwarder import core
from .configs import levelConfig


class ScriptLevel(Thread):
    def __init__(self,v):
        super().__init__()
        FactoryID, DeviceName, DeviceIp = v.values()
        self.DeviceName=DeviceName
        self.steelLevelUrl = fr"http://127.0.0.1:{core.basePrt+FactoryID}"
        self.start()

    def run(self):
        print("run")

        # for item in range(200):
        #     itemSize = 1000
        #     dataList = api.steelList(itemSize, 200000 + item * itemSize,steelLevelUrl=self.steelLevelUrl)
        #     # dataList = api.searchByData("2024-05-1 0:0:0", "2024-05-10 0:0:0")
        #     for steelInfo in dataList:  # 查询钢板
        #         print("steelInfo_____", steelInfo)
        #         steelInfo: SteelProject
        #         levelBySteelProject(steelInfo)
        #         toExcel.append(steelInfo)
        #         # LevelSet.addSteel(steelInfo)
        #     toExcel.saveExcel_()

        maxSeq = LevelSet.getMaxSteelNoByproductionLine(self.DeviceName)  # 获取当前已经判断级别的 最大值
        getCount = 100
        oldSeqNo = maxSeq
        while True:
            for steelInfo in api.steelList(getCount, oldSeqNo,steelLevelUrl=self.steelLevelUrl):  # 查询钢板
                steelInfo: SteelProject
                steelInfo.productionLine = self.DeviceName

                if oldSeqNo == steelInfo.steelID:
                    continue

                levelBySteelProject(steelInfo)
                # toExcel.append(steelInfo)
                LevelSet.addSteel(steelInfo)


                oldSeqNo = steelInfo.steelID
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
                info = levelConfig.steelLevel(steelInfo, filterDefects)
                print(info)
                i, defList, levelMsg = info
                steelInfo.level = i, defList, levelMsg
                toExcel.append(steelInfo)
                LevelSet.addSteel(steelInfo)
                # 获取 钢板等级
            time.sleep(5)