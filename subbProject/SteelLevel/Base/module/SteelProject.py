from datetime import datetime

from config import TIMESTAMP_FORMAT
from ...Base.module._ModelBase_ import ModelBase
from ...DataSet.models import SteelLevel
from ...tool import getPackageNo


class SteelProject(ModelBase):
    def __init__(self, jsonData):
        self.jsonData = jsonData
        self._level = 1
        self._packageNo_ = ""

    @property
    def id(self):
        return self.jsonData["id"]

    @property
    def steelNo(self):
        return self.jsonData["steelNo"]

    @property
    def packageName(self):
        if not self._packageNo_:
            gpn=getPackageNo(self.steelNo)
            self._packageNo_= gpn
            return gpn
        return self._packageNo_
    @property
    def seqNo(self):
        return self.jsonData["steelID"]

    @property
    def steelID(self):
        return self.jsonData["steelID"]

    @property
    def steelType(self):
        return self.jsonData["steelType"]

    @property
    def steelLength(self):
        return self.jsonData["steelLength"]

    @property
    def steelWidth(self):
        return self.jsonData["steelWidth"]

    @property
    def steelThick(self):
        return self.jsonData["steelThick"]

    @property
    def upDefectNum(self):
        return self.jsonData["upDefectNum"]

    @property
    def downDefectNum(self):
        return self.jsonData["downDefectNum"]

    @property
    def errorLevel(self):
        return self.jsonData["errorLevel"]

    @property
    def grade(self):
        return self.jsonData["grade"]

    @property
    def detectTime(self):
        print(self.jsonData["detectTime"])
        return datetime.strptime(self.jsonData["detectTime"], TIMESTAMP_FORMAT)

    @property
    def topLen(self):
        return self.jsonData["topLen"]

    @property
    def bottomLen(self):
        return self.jsonData["bottomLen"]

    @property
    def level(self):
        return self._level[0]

    @property
    def levelInfo(self):
        return self._level[1]
    @property
    def levelCode(self):
        if len(self._level[0]) < 15:
            return "一等品"
        return "二等品"

    @level.setter
    def level(self, value):
        self._level = value

    def getSteelLevel(self):
        return SteelLevel(
            steelName=self.steelNo,
            packageName=self.packageName,
            seqNo=self.seqNo,
            steelID=self.steelID,
            steelType=self.steelType,
            length=self.steelLength,
            width=self.steelWidth,
            thick=self.steelThick,
            detectTime=self.detectTime,
            grade=self.grade,
            level=(len(self._level[0]) > 0) + 1,
            msg=self._level[1],
        )

    def __str__(self):
        return str(self.jsonData)
