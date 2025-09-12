import config
from datetime import datetime
from subbProject.SteelLevel.Base.module._ModelBase_ import ModelBase
from subbProject.SteelLevel.DataSet.models import UserData
from subbProject.SteelLevel.configs.DefectClass import defectClass2LevelDefectClass


class UserDataProject(ModelBase):
    def __init__(self, json_data):
        self._json_data = json_data
        self._fileName = json_data["fileName"]
        self._steelName = json_data["steelName"]
        self._plant_classification = json_data["plant_classification"]
        self._productionLine_classification = json_data["productionLine_classification"]
        self._productionTime = datetime.strptime(json_data["productionTime"], config.TIMESTAMP_FORMAT)
        self._steelType = json_data["steelType"]
        self._steelLevel = json_data["steelLevel"]
        self._steelLevelCode = json_data["steelLevelCode"]
        self._residualReasonCode = json_data["residualReasonCode"]
        self._defectCode = json_data["defectCode"]
        self._scrapReasonCode = json_data["scrapReasonCode"]
        self._downgradeNote = json_data["downgradeNote"]
        self._busNumber = json_data["busNumber"]

    @property
    def fileName(self):
        return self._fileName

    @property
    def steelName(self):
        return self._steelName

    @property
    def plant_classification(self):
        return self._plant_classification

    @property
    def productionLine_classification(self):
        return self._productionLine_classification

    @property
    def productionTime(self):
        return self._productionTime

    @property
    def steelType(self):
        return self._steelType

    @property
    def steelLevel(self):
        return self._steelLevel

    @property
    def steelLevelCode(self):
        return self._steelLevelCode

    @property
    def residualReasonCode(self):
        return self._residualReasonCode

    @property
    def defectCode(self):
        return self._defectCode

    @property
    def scrapReasonCode(self):
        return self._scrapReasonCode

    @property
    def downgradeNote(self):
        return self._downgradeNote

    @property
    def busNumber(self):
        return self._busNumber

    def getUserData(self):

        return UserData(
            fileName=self.fileName,  # 插入的文件名称
            steelName=self.steelName,
            plant_classification=self.plant_classification,
            productionLine_classification=self.productionLine_classification,
            productionTime=self.productionTime,
            steelType=self.steelType,
            steelLevel=self.steelLevel,
            steelLevelCode=self.steelLevelCode,
            residualReasonCode=self.residualReasonCode,
            defectCode=self.defectCode,
            scrapReasonCode=self.scrapReasonCode,
            downgradeNote=self.downgradeNote,
            busNumber=self.busNumber
        )

    def __str__(self):
        return str(self._json_data)


def getUserDataProject(item) -> UserDataProject:
    var = {'None_0': '非校验', '材料号': '4C04558500', '厂别区分': 'H9_热处理一厂', '生产时刻': '2024-05-20 00:07:53',
           '厚度 (mm)': '8', '宽度 (mm)': '1800', '材料实际重量': '8.26', '最终牌号': 'CCS-B', '产品等级码': '一等品',
           '余材原因代码': ' ', '缺陷代码': ' ', '报废原因代码': ' ', '缺陷责任单位': ' ', '降级注释': ' ',
           '报废注释': ' ',
           '钢卷缺陷描述': ' ', '入口材料号': '4A10611900', '热轧母卷号': '4A10611900'}

    return UserDataProject(
        {
            "fileName": item['fileName'],
            "steelName": item['材料号'],
            "plant_classification":  item['厂区分别'],
            "productionLine_classification": item['产线区分'],
            "productionTime": item['生产时间'],
            "steelType": item['钢种'],
            "steelLevel": item['产品等级'],
            "steelLevelCode":  item['产品等级'],
            "residualReasonCode": item['判级原因'],
            "defectCode": item['缺陷等级'],
            "scrapReasonCode": item['判级原因'],
            "downgradeNote": item['缺陷等级'],
            "busNumber": item['捆包号']
        }
    )

