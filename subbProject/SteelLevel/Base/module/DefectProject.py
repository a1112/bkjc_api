from ...Base.module._ModelBase_ import ModelBase
from ...DataSet.models import DefectLevel
from ...configs.ConfigRead import levelConfig
from ...configs.DefectClass import defectClass2LevelDefectClass


class DefectProject(ModelBase):
    def __init__(self, json_data):
        self._json_data = json_data
        defCLS = defectClass2LevelDefectClass(self.defectID)

        self.defInfo = levelConfig.defectLevelDict[defCLS]
        var = {'defectNo': 216, 'defectID': 12, 'bmIndex': 1,
               'seqNo': 519, 'cameraId': 1, 'imageIndex': 26, 'defectX': 26752,
               'defectY': 192, 'defectWidth': 150, 'defectHeight': 64,
               'leftInImg': 128, 'rightInImg': 192, 'topInImg': 128,
               'bottomInImg': 278, 'leftInSteel': -1457, 'rightInSteel': -1438,
               'topInSteel': 5660, 'bottomInSteel': 5660,
               'rec': [26752, 192, 150, 64],
               'box': [549, -43, 116, 111],
               'boxX': 549, 'boxY': -43,
               'boxW': 116, 'boxH': 111,
               'defectCoefficient': '0 %',
               'grade': 0}
        self.levelInfo = {}

    @property
    def defectNo(self):
        return self._json_data['defectNo']

    @property
    def defectID(self):
        return self._json_data['defectID']

    @property
    def defectName(self):
        return self.defInfo['name']

    @property
    def bmIndex(self):
        return self._json_data['bmIndex']

    @property
    def seqNo(self):
        return self._json_data['seqNo']

    @property
    def cameraId(self):
        return self._json_data['cameraId']

    @property
    def imageIndex(self):
        return self._json_data['imageIndex']

    @property
    def defectX(self):
        return self._json_data['defectX']

    @property
    def defectY(self):
        return self._json_data['defectY']

    @property
    def defectWidth(self):
        return self._json_data['defectWidth']

    @property
    def defectHeight(self):
        return self._json_data['defectHeight']

    @property
    def width(self):
        return self.rightInSteel-self.leftInSteel

    @property
    def height(self):
        return self.bottomInSteel-self.topInSteel

    @property
    def leftInImg(self):
        return self._json_data['leftInImg']

    @property
    def rightInImg(self):
        return self._json_data['rightInImg']

    @property
    def topInImg(self):
        return self._json_data['topInImg']

    @property
    def bottomInImg(self):
        return self._json_data['bottomInImg']

    @property
    def leftInSteel(self):
        return self._json_data['leftInSteel']

    @property
    def rightInSteel(self):
        return self._json_data['rightInSteel']

    @property
    def topInSteel(self):
        return self._json_data['topInSteel']

    @property
    def bottomInSteel(self):
        return self._json_data['bottomInSteel']

    @property
    def rec(self):
        return self._json_data['rec']

    @property
    def box(self):
        return self._json_data['box']

    @property
    def boxX(self):
        return self._json_data['boxX']

    @property
    def boxY(self):
        return self._json_data['boxY']

    @property
    def boxW(self):
        return self._json_data['boxW']

    @property
    def boxH(self):
        return self._json_data['boxH']

    @property
    def defectCoefficient(self):
        return self._json_data['defectCoefficient']

    @property
    def grade(self):
        return self._json_data['grade']

    @property
    def msg(self):
        if "msg" in self._json_data:
            return self._json_data['msg']
        return ""

    @property
    def level(self):
        return self.levelInfo

    @level.setter
    def level(self, value):
        self.levelInfo = value

    @property
    def levelCode(self):
        return {
            "L": 1,
            "M": 2,
            "S": 3
        }[self.level]

    def getDefectLevel(self):
        return DefectLevel(
            defectNo=self.defectNo,
            defectID=self.defectID,
            defectName=self.defectName,
            bmIndex=self.bmIndex,
            seqNo=self.seqNo,
            classId=self.defectID,
            cameraId=self.cameraId,
            ImageIndex=self.imageIndex,
            imageX=self.leftInImg,
            imageY=self.topInImg,
            imageW=self.rightInImg - self.leftInImg,
            imageH=self.bottomInImg - self.topInImg,
            steelX=self.leftInSteel,
            steelY=self.topInSteel,
            steelW=self.rightInSteel - self.leftInSteel,
            steelH=self.bottomInSteel - self.topInSteel,
            level=self.levelCode,
            levelMsg=self.level
        )

    def __str__(self):
        return str(self._json_data)
