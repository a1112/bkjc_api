import datetime
import json
from pathlib import Path

import config
from ..configs.DataRead import LevelDataGet, xlsxDataGet
from ..configs.DefectClass import defectClass2LevelDefectClassInfo
from ..init import app
from ..DataSet import LevelSet
from fastapi import File, UploadFile, Response

from ..configs import ConfigRead


@app.get("/steelLevel/info")
def get_steel_level_info():
    steelLevelInfo = LevelSet.getSteelLevelInfo()
    return {"min": steelLevelInfo[0], "max": steelLevelInfo[1]}


@app.get("/steelLevel/exportSteelLevelByTime/{startTime:str}/{endTime:str}/{fileName:path}")
def exportSteelLevelByTime(startTime, endTime, fileName):
    startTime = datetime.datetime.strptime(startTime, config.TIMESTAMP_FORMAT)
    endTime = datetime.datetime.strptime(endTime, config.TIMESTAMP_FORMAT)
    print(startTime)
    print(endTime)
    print(fileName)


@app.get("/steelLevel/defectLevel/{bmIndex:int}/{defectId:int}")
def getDefectLevel(defectId):
    pass


@app.get("/steelLevel/getLevelTabel")
def getLevelTabel():
    return ConfigRead.getLevelTabel()


@app.get("/steelLevel/getLocalLevelData")
def getLocalLevelData():
    return xlsxDataGet()


@app.get("/steelLevel/getLevelData")
def getLevelData():
    return LevelDataGet()


@app.get("/steelLevel/getDefectInfo")
def getDefectInfo():
    return defectClass2LevelDefectClassInfo()
