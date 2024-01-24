from threading import Thread
import time
from bkjc_database.NerCarDataBase.mysql import Ncdhotstripdefect, defectinfodatabase
from bkjc_database.NerCarDataBase.mysql import Ncdhotstrip


class DefectSynchronizer(Thread):
    def __init__(self):
        super().__init__()
        print("DefectSynchronizer")
        # self.start()

    def run(self):
        seq_steelNoDict = {}
        while True:
            for istop in [0,1]:
                defectId = defectinfodatabase.getLastDefectId(istop)
                for defect in Ncdhotstripdefect.getDefectByDefectId(istop + 1, defectId):
                    defect: Ncdhotstripdefect.Camdefect1
                    if defect.seqNo in seq_steelNoDict:
                        steel = seq_steelNoDict[defect.seqNo]
                    else:
                        steel = Ncdhotstrip.getSteelBySeqNo(defect.seqNo)
                        seq_steelNoDict[defect.seqNo] = steel
                    defectinfodatabase.appendDefect(defect, steel)
                    if len(seq_steelNoDict)>100:
                        seq_steelNoDict={}
                        defectinfodatabase.session.commit()
            defectinfodatabase.session.commit()
            time.sleep(60)
            # 查询最新的defect
