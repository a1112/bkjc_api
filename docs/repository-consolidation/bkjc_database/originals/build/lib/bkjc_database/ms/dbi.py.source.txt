from sqlalchemy import and_

from bkjc_database.NerCarDataBase.mysql.Ncdhotstrip import underCameraIdList, upCameraIdList
from bkjc_database.property.DataBaseInterFace import DataBaseInterFace
from bkjc_database.NerCarDataBase.mysql import Ncdhotstrip
from bkjc_database.NerCarDataBase.mysql import Ncdhotstripdefect


def _rgb_to_hex(rgb_tuple):
    r, g, b = rgb_tuple
    r = max(0, min(int(r), 255))
    g = max(0, min(int(g), 255))
    b = max(0, min(int(b), 255))
    return "#{:02x}{:02x}{:02x}".format(r, g, b)


class Mysql_4d0(DataBaseInterFace):

    def isSqlServer(self):
        return False

    def addSteelrecord(self, steelrecord: Ncdhotstrip.Steelrecord):
        with Ncdhotstrip.Session() as session:
            session.add(steelrecord)
            session.commit()

    def addRcvsteelprop(self, rcvsteelprop: Ncdhotstrip.Rcvsteelprop):
        with Ncdhotstrip.Session() as session:
            session.add(rcvsteelprop)
            session.commit()


    def getSteelByNum(self, number, defectOnly=False, startID=None, desc=True):
        with Ncdhotstrip.Session() as session:
            print(session)
            try:
                que = session.query(Ncdhotstrip.Steelrecord,
                                    Ncdhotstrip.Rcvsteelprop).join(Ncdhotstrip.Rcvsteelprop,
                                                                   Ncdhotstrip.Rcvsteelprop.steelID == Ncdhotstrip.Steelrecord.steelID,
                                                                   isouter=False)
                if startID:
                    que = que.filter(Ncdhotstrip.Steelrecord.seqNo > startID)
                if desc:
                    ord_item = Ncdhotstrip.Steelrecord.seqNo.desc()
                else:
                    ord_item = Ncdhotstrip.Steelrecord.seqNo.asc()
                if not defectOnly:
                    res = [[i_, j_] for i_, j_ in que.order_by(
                        ord_item)[0:number]]
                else:
                    res = [[i_, j_] for i_, j_ in
                           que.filter(Ncdhotstrip.Steelrecord.defectNum > 0).order_by(
                               ord_item)[0:number]]
                return res
            except:
                session.rollback()
                raise

    def getSteelById(self, steelId):
        return self.getSteelBySeqNo(steelId)

    def getSteelBySeqNo(self, seqNo):
        with Ncdhotstrip.Session() as session:
            try:
                que = session.query(Ncdhotstrip.Steelrecord,
                                                Ncdhotstrip.Steelrecord.steelID).join(Ncdhotstrip.Rcvsteelprop,
                                                                                      Ncdhotstrip.Steelrecord.steelID == Ncdhotstrip.Rcvsteelprop.steelID,
                                                                                      isouter=False)
                que = que.filter(seqNo == Ncdhotstrip.Steelrecord.seqNo)
                return [[i_, j_] for i_, j_ in que.order_by(
                    Ncdhotstrip.Steelrecord.seqNo.desc())[0:100]]
            except:
                session.rollback()
                raise
                # session.close()

    def getSteelBySteelNo(self, steelNo):
        with Ncdhotstrip.Session() as session:
            try:
                que = session.query(Ncdhotstrip.Steelrecord,
                                                Ncdhotstrip.Steelrecord.steelID).join(Ncdhotstrip.Rcvsteelprop,
                                                                                      Ncdhotstrip.Steelrecord.steelID == Ncdhotstrip.Rcvsteelprop.steelID,
                                                                                      isouter=False)
                que = que.filter(steelNo == Ncdhotstrip.Steelrecord.steelID)
                return [[i_, j_] for i_, j_ in que.order_by(
                    Ncdhotstrip.Steelrecord.seqNo.desc())[0:500]]
            except:
                session.rollback()
                raise
            # session.close()

    def getSteelByDate(self, fromDate, toDate):
        with Ncdhotstrip.Session() as session:
            try:
                que = session.query(Ncdhotstrip.Steelrecord,
                                                Ncdhotstrip.Steelrecord.steelID).join(Ncdhotstrip.Rcvsteelprop,
                                                                                      Ncdhotstrip.Steelrecord.steelID == Ncdhotstrip.Rcvsteelprop.steelID,
                                                                                      isouter=False)
                que = que.filter(
                    and_(Ncdhotstrip.Steelrecord.detectTime >= fromDate, Ncdhotstrip.Steelrecord.detectTime <= toDate))
                return [[i_, j_] for i_, j_ in que.order_by(
                    Ncdhotstrip.Steelrecord.seqNo.desc())[0:500]]
            except:
                session.rollback()
                raise

    def getDefectBySeqNo(self, seqNo):
        seqNo = int(seqNo)
        reInfo = {"upCount": 0, "downCount": 0, "upCameraList": Ncdhotstrip.upCameraIdList,
                  "downCameraList": Ncdhotstrip.underCameraIdList}

        for camera in Ncdhotstrip.allCamera:
            with Ncdhotstripdefect.Session() as session:
                try:
                    reInfo[camera] = {}
                    defectClass = Ncdhotstripdefect.Camdefect2
                    if camera == 1:
                        defectClass = Ncdhotstripdefect.Camdefect1
                    reInfo[camera]["defect"] = session.query(defectClass).filter(
                        defectClass.seqNo == seqNo).all()
                    reInfo[camera]["count"] = len(reInfo[camera]["defect"])
                    reInfo[camera]["is_up"] = camera == 1
                    if reInfo[camera]["is_up"]:
                        reInfo["upCount"] += reInfo[camera]["count"]
                    else:
                        reInfo["downCount"] += reInfo[camera]["count"]
                except:
                    session.rollback()
                    raise
        return reInfo

    def getDefectClass(self):
        import json
        return [
            {
                "name": defect["desc"],
                "color": _rgb_to_hex((defect["color"]["red"], defect["color"]["green"], defect["color"]["blue"])),
                "id": defect["desc"],
                "grade": 0
            }
            for defect in json.load(open("DefectClass.json","r",encoding="utf-8"))["items"]]

    def getCameraList(self):
        return [upCameraIdList, underCameraIdList]

    def getDefectItem(self, cameraId, defectId):
        defectClass = Ncdhotstripdefect.Camdefect2
        with Ncdhotstripdefect.Session() as session:
            if cameraId == 1:
                defectClass = Ncdhotstripdefect.Camdefect1
            item = session.query(defectClass).filter(defectClass.defectID == defectId).all()
            if item:
                item = item[0]
                return item
            return None

    def getGradeInfo(self, seqNo):
        pass
