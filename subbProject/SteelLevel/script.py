import time
from  threading import Thread
from subbProject.SteelLevel.DataSet import api, LevelSet
from . import toExcel
from .Base.module import SteelProject
from .main import levelBySteelProject


class Script1(Thread):
    def __init__(self):
        super().__init__()
        self.start()

    def run(self):
        time.sleep(5)
        print("run")
        for item in range(100):
            dataList = api.steelList(500, 207934+item * 500)
            # dataList = api.searchByData("2024-05-1 0:0:0", "2024-05-10 0:0:0")
            for steelInfo in dataList:  # 查询钢板
                print("steelInfo_____", steelInfo)
                steelInfo: SteelProject
                levelBySteelProject(steelInfo)
                toExcel.append(steelInfo)
                LevelSet.addSteel(steelInfo)
            toExcel.saveExcel_()


sc1 = Script1()
