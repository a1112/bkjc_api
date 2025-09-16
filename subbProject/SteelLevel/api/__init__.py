import datetime
import json
from io import BytesIO
from pathlib import Path

import xlsxwriter
from starlette.responses import StreamingResponse

import config
from bkjc_database.SqlTool import to_dict
from ..DataSet.LevelSet import getSteelLevelByDate, getAllSteelLevel
from ..configs.DataRead import LevelDataGet, xlsxDataGet
from ..configs.DefectClass import defectClass2LevelDefectClassInfo
from ..init import app
from ..DataSet import LevelSet
from fastapi import File, UploadFile, Response
from ..toExcel import saveExcel
from ..configs import ConfigRead



@app.get("/steelLevel/info")
def get_steel_level_info():
    steelLevelInfo = LevelSet.getSteelLevelInfo()
    return {"min": steelLevelInfo[0], "max": steelLevelInfo[1]}

@app.get("/delay")
async def get_delay():
    return True


@app.get("/getLevelData")
async def get_level_data():
    steels = getAllSteelLevel()
    return to_dict(steels)


@app.get("/steelLevel/exportSteelLevelByTime/{startTime:str}/{endTime:str}/{fileName:path}")
def exportSteelLevelByTime(startTime, endTime, fileName):
    startTime = datetime.datetime.strptime(startTime, config.TIMESTAMP_FORMAT)
    endTime = datetime.datetime.strptime(endTime, config.TIMESTAMP_FORMAT)
    print(startTime)
    print(endTime)
    print(fileName)

    output = BytesIO()
    steels = getSteelLevelByDate(startTime, endTime)
    workbook = saveExcel(steels, None)
    workbook.save(output)
    output.seek(0)
    headers = {
        fr"Content-Disposition": f"attachment; filename={fileName}",
        # "Content-Length": str(file_size)  # 设置文件大小
    }

    # 将 BytesIO 对象传递给 StreamingResponse，设置内容类型和附件名称
    response = StreamingResponse(output, headers=headers,
                                 media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response



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

@app.get("/steelLevel/export_test")
def export_test():
    output = BytesIO()
    steels = getAllSteelLevel()
    workbook = saveExcel(steels, None)
    workbook.save(output)
    output.seek(0)
    # file_size=output.tell()
    headers = {
        "Content-Disposition": f"attachment; filename=example.xlsx",
        # "Content-Length": str(file_size)  # 设置文件大小
    }

    # 将 BytesIO 对象传递给 StreamingResponse，设置内容类型和附件名称
    response = StreamingResponse(output, headers=headers,
                                 media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    return response

def export_text():
    steels = getAllSteelLevel()
    saveExcel(steels, "steelLevel.xlsx")