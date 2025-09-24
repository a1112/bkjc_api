import datetime
import json
from io import BytesIO
from pathlib import Path

import xlsxwriter
from starlette.responses import StreamingResponse

import config

from subbProject.ApiForwarder import core as ApiForwarderCore

from ..DataSet.LevelSet import getSteelLevelByDate, getAllSteelLevel, to_dict
from ..configs.DataRead import LevelDataGet, xlsxDataGet
from ..configs.DefectClass import defectClass2LevelDefectClassInfo
from ..init import app
from ..DataSet import LevelSet
from fastapi import File, UploadFile, Response
from ..toExcel import saveExcel
from ..configs import ConfigRead



# @app.get("/steelLevel/info")
# def get_steel_level_info():
#     """
#     判级规则
#     """
#     steelLevelInfo = LevelSet.getSteelLevelInfo()
#     return {"min": steelLevelInfo[0], "max": steelLevelInfo[1]}

@app.get("/delay")
async def get_delay():
    """
    延时测试
    """
    return True


# @app.get("/getLevelData")
# async def get_level_data():
#
#     steels = [to_dict(item) for item in getAllSteelLevel()]
#
#     for item in steels:
#         for k in item.keys():
#             if not item[k]:
#                 item[k]=""
#     return steels

@app.get("/productionLineInfo")
async def get_productionLineInfo():
    """
    获取所有的产线信息
    """
    tabelList = ApiForwarderCore.tabelList
    return tabelList

@app.get("/getLevelTabel")
async def getLevelTabel():
    """
    获取判级规则
    """
    return ConfigRead.getLevelTabel()


@app.get("/exportSteelLevelByTime/{startTime:str}/{endTime:str}/{fileName:path}")
def exportExcelByTime(productionLine,startTime, endTime, fileName):
    """
        导出excel文件
        productionLine:产线名词,不进行填写则是全部产线
        时间格式： ”%Y-%m-%d %H:%M:%S“
    """

    startTime = datetime.datetime.strptime(startTime, config.TIMESTAMP_FORMAT)
    endTime = datetime.datetime.strptime(endTime, config.TIMESTAMP_FORMAT)

    output = BytesIO()
    steels = getSteelLevelByDate(startTime, endTime,productionLine=productionLine)
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

@app.get("")


# @app.get("/defectLevel/{bmIndex:int}/{defectId:int}")
# def getDefectLevel(defectId):
#     pass




# @app.get("/getLocalLevelData")
# def getLocalLevelData():
#     return xlsxDataGet()


@app.get("/getLevelData")
def getLevelData():
    return LevelDataGet()


@app.get("/getDefectInfo")
def getDefectInfo():
    return defectClass2LevelDefectClassInfo()

@app.get("/getLevelTitle")
def getLevelTitle():
    """
        部分字段的说明

    """

    # id = Column(Integer, primary_key=True)
    # plant_classification = Column(String)
    # productionLine_classification = Column(String)
    # steelName = Column(String)
    # packageName = Column(String)
    # seqNo = Column(Integer)
    # steelID = Column(Integer)
    # steelType = Column(String)
    # length = Column(Float)
    # width = Column(Float)
    # thick = Column(Float)
    # upDefectNum = Column(Integer)  # 不同缺陷等级的数量
    # downDefectNum = Column(Integer)  # 不同缺陷等级的数量
    # detectTime = Column(DateTime)
    # level = Column(Integer)
    # levelInfo = Column(String)
    # grade = Column(Integer)
    # msg = Column(String)
    #
    # level_up = Column(Integer)
    # levelInfo_up = Column(String)
    # grade_up = Column(Integer)
    # msg_up = Column(String)
    #
    # level_under = Column(Integer)
    # levelInfo_under = Column(String)
    # grade_under = Column(Integer)
    # msg_under = Column(String)

    return [
        {
            "key":"id",
            "name":"判级Id",
            "fillWidth":False,
            "item_width":150
        },{
            "key": "productionLine_classification",
            "name": "产线名称",
            "fillWidth":False,
            "item_width":150
        },{
            "key": "packageName",
            "name": "捆包号",
            "fillWidth":False,
            "item_width":150
        },{
            "key": "steelName",
            "name": "钢板号",
            "fillWidth":False,
            "item_width":150
        },{
            "key": "steelType",
            "name": "钢种",
            "fillWidth":False,
            "item_width":150
        },{
            "key": "length",
            "name": "长",
            "fillWidth":False,
            "item_width":100
        },{
            "key": "width",
            "name": "宽",
            "fillWidth":False,
            "item_width":100
        },{
            "key": "thick",
            "name": "厚",
            "fillWidth":False,
            "item_width":100
        },{
            "key": "level",
            "name": "等级",
            "fillWidth":False,
            "item_width":100
        },{
            "key": "msg",
            "name": "信息",
            "fillWidth":True,
            "item_width":150
        }
    ]

# @app.get("/steelLevel/export_test")
# def export_test():
#     output = BytesIO()
#     steels = getAllSteelLevel()
#     workbook = saveExcel(steels, None)
#     workbook.save(output)
#     output.seek(0)
#     # file_size=output.tell()
#     headers = {
#         "Content-Disposition": f"attachment; filename=example.xlsx",
#         # "Content-Length": str(file_size)  # 设置文件大小
#     }
#
#     # 将 BytesIO 对象传递给 StreamingResponse，设置内容类型和附件名称
#     response = StreamingResponse(output, headers=headers,
#                                  media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
#     return response
#
# @app.get("/getProductionLine")
# def getProductionLine():
#     return ApiForwarderCore.tabelList


def export_text():
    steels = getAllSteelLevel()
    saveExcel(steels, "steelLevel.xlsx")