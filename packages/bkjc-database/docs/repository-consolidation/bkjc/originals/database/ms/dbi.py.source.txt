import webcolors

from bkjc_database.NerCarDataBase.mysql.Ncdhotstrip import underCameraIdList, upCameraIdList
from bkjc_database.interface.DataBaseInterFace import DataBaseInterFace
from bkjc_database.NerCarDataBase.mysql import Ncdhotstrip
from bkjc_database.NerCarDataBase.mysql import Ncdhotstripdefect


class Mysql_4d0(DataBaseInterFace):

    def isSqlServer(self):
        return False

    def getSteelByNum(self, number, defectOnly, startID=None):
        session = Ncdhotstrip.Session()
        try:
            que = session.query(Ncdhotstrip.Steelrecord,
                                Ncdhotstrip.Rcvsteelprop).join(Ncdhotstrip.Rcvsteelprop,
                                                               Ncdhotstrip.Rcvsteelprop.steelID == Ncdhotstrip.Steelrecord.steelID,
                                                               isouter=True)
            if startID:
                que = que.filter(Ncdhotstrip.Steelrecord.seqNo > startID)
            if not defectOnly:
                res = [[i_, j_] for i_, j_ in que.order_by(
                    Ncdhotstrip.Steelrecord.seqNo.desc())[0:number]]
            else:
                res = [[i_, j_] for i_, j_ in
                       que.filter(Ncdhotstrip.Steelrecord.defectNum > 0).order_by(
                           Ncdhotstrip.Steelrecord.seqNo.desc())[0:number]]
            print(res)
            return res
        except:
            session.rollback()
            raise
        finally:
            pass

    def getSteelById(self, steelId):
        try:
            que = Ncdhotstrip.session.query(Ncdhotstrip.Steelrecord,
                                            Ncdhotstrip.Steelrecord.steelID).join(Ncdhotstrip.Rcvsteelprop,
                                                                                  Ncdhotstrip.Steelrecord.steelID == Ncdhotstrip.Rcvsteelprop.steelID,
                                                                                  isouter=True)
            que = que.filter(steelId == Ncdhotstrip.Steelrecord.id)
            return [[i_, j_] for i_, j_ in que.order_by(
                Ncdhotstrip.Steelrecord.seqNo.desc())[0:100]]
        except:
            Ncdhotstrip.session.rollback()
            raise
        finally:
            pass
            # session.close()

    def getSteelBySeqNo(self, seqNo):
        try:
            que = Ncdhotstrip.session.query(Ncdhotstrip.Steelrecord,
                                            Ncdhotstrip.Steelrecord.steelID).join(Ncdhotstrip.Rcvsteelprop,
                                                                                  Ncdhotstrip.Steelrecord.steelID == Ncdhotstrip.Rcvsteelprop.steelID,
                                                                                  isouter=True)
            que = que.filter(seqNo == Ncdhotstrip.Steelrecord.seqNo)
            return [[i_, j_] for i_, j_ in que.order_by(
                Ncdhotstrip.Steelrecord.seqNo.desc())[0:100]]
        except:
            Ncdhotstrip.session.rollback()
            raise
        finally:
            pass
            # session.close()

    def getSteelBySteelNo(self, steelNo):
        try:
            que = Ncdhotstrip.session.query(Ncdhotstrip.Steelrecord,
                                            Ncdhotstrip.Steelrecord.steelID).join(Ncdhotstrip.Rcvsteelprop,
                                                                                  Ncdhotstrip.Steelrecord.steelID == Ncdhotstrip.Rcvsteelprop.steelID,
                                                                                  isouter=True)
            que = que.filter(steelNo == Ncdhotstrip.Steelrecord.steelID)
            return [[i_, j_] for i_, j_ in que.order_by(
                Ncdhotstrip.Steelrecord.seqNo.desc())[0:500]]
        except:
            Ncdhotstrip.session.rollback()
            raise
        finally:
            pass
            # session.close()

    def getSteelByDate(self, fromDate, toDate):
        try:
            que = Ncdhotstrip.session.query(Ncdhotstrip.Steelrecord,
                                            Ncdhotstrip.Steelrecord.steelID).join(Ncdhotstrip.Rcvsteelprop,
                                                                                  Ncdhotstrip.Steelrecord.steelID == Ncdhotstrip.Rcvsteelprop.steelID,
                                                                                  isouter=True)
            que = que.filter(
                and_(Ncdhotstrip.Steelrecord.detectTime >= fromDate, Ncdhotstrip.Steelrecord.detectTime <= toDate))
            return [[i_, j_] for i_, j_ in que.order_by(
                Ncdhotstrip.Steelrecord.seqNo.desc())[0:500]]
        except:
            Ncdhotstrip.session.rollback()
            raise
        finally:
            pass
            # session.close()

    def getDefectBySeqNo(self, seqNo):
        seqNo = int(seqNo)
        reInfo = {"upCount": 0, "downCount": 0, "upCameraList": Ncdhotstrip.upCameraIdList,
                  "downCameraList": Ncdhotstrip.underCameraIdList}

        for camera in Ncdhotstrip.allCamera:
            try:
                reInfo[camera] = {}
                defectClass = Ncdhotstripdefect.Camdefect2
                if camera == 1:
                    defectClass = Ncdhotstripdefect.Camdefect1
                reInfo[camera]["defect"] = Ncdhotstripdefect.session.query(defectClass).filter(
                    defectClass.seqNo == seqNo).all()
                reInfo[camera]["count"] = len(reInfo[camera]["defect"])
                reInfo[camera]["is_up"] = camera == 1
                if reInfo[camera]["is_up"]:
                    reInfo["upCount"] += reInfo[camera]["count"]
                else:
                    reInfo["downCount"] += reInfo[camera]["count"]
            except:
                Ncdhotstripdefect.session.rollback()
                raise
            finally:
                pass
        return reInfo

    def getDefectClass(self):
        import json
        return [
            {
                "name": defect["desc"],
                "color": webcolors.rgb_to_hex((defect["color"]["red"], defect["color"]["green"], defect["color"]["blue"])),
                "id": defect["desc"],
                "grade": 0
            }
            for defect in json.load(open("DefectClass.json","r",encoding="utf-8"))["items"]]
        # class defect:
        #     def __init__(self, Name, Red, Green, Blue, Class, Grade):
        #         self.ID = Class
        #         self.Name = Name
        #         self.Red = Red
        #         self.Green = Green
        #         self.Blue = Blue
        #         self.Class = Class
        #         self.Grade = Grade
        # return [defect(f"测试{i}", i * 5, i * 5, i * 5, i, 1) for i in range(50)]

    def getCameraList(self):
        return [upCameraIdList, underCameraIdList]

    def getDefectItem(self, cameraId, defectId):
        defectClass = Ncdhotstripdefect.Camdefect2
        if cameraId == 1:
            defectClass = Ncdhotstripdefect.Camdefect1
        item = Ncdhotstripdefect.session.query(defectClass).filter(defectClass.defectID == defectId).all()
        if item:
            item = item[0]
            return item
        return None

    def getGradeInfo(self,seqNo):
        pass