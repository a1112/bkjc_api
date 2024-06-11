import datetime
import logging
from io import BytesIO
from pathlib import Path

import webcolors
from PIL import Image
from bkjc_database import NerCarDataBase

from bkjc_database.dbm import dbm
from fastapi.responses import StreamingResponse

import config
import tool
from api.api_core import api_core
from core import steelGetApp as app

sourceImageCache = {}  # 缓存大图
defectItemCache = {}  # 缓存缺陷小图

g_bytesIO = None
sC = 0
if dbm.isSqlServer():
    import bkjc_database.NerCarDataBase.sqlserver
else:
    import bkjc_database.NerCarDataBase.mysql


def getImageIO(image: Image.Image, format_="jpeg"):
    """
    :param format_:
    :param image:
    :return:
    """
    bytesIO = BytesIO()
    try:
        image.save(bytesIO, format=format_)
    except BaseException as e:
        logging.error(e)
        raise e
    bytesIO.seek(0)
    return bytesIO


@app.get("/getDelayed")
async def getDelayed():
    """获取延时"""
    return True


async def clearCache():
    """清理缓存"""
    global defectItemCache

    defectItemCache = {}


import bkjc_tools


def addSteelCache(steel, steelId):
    """　　　
    缓存数据
    :param steel:
    :param steelId:
    :return:
    """
    return api_core.get_steelInfo(steel, steelId)


@app.get("/steelList/{num:int}/{start_seqNo:int}")
def getSteelList(start_seqNo, num):
    steels = dbm.getSteelByNum(num, False, start_seqNo, desc=False)
    infos = []
    for (steel, steelId) in steels:
        if dbm.isSqlServer():  # 3.0
            pass
        info = addSteelCache(steel, steelId)
        infos.append(info)
    return infos


@app.get("/steelGet/{num:int}/{defectOnly:int}")
def getSteelInfoNum(num: int = 100, defectOnly=0):
    """
    获取最新的N条钢板信息. \n
    该接口主要测试使用。 \n
    :return:        \n
    """
    steels = dbm.getSteelByNum(num, defectOnly)[::-1]
    infos = []
    for (steel, steelId) in steels:
        if dbm.isSqlServer():  # 3.0
            pass
        info = addSteelCache(steel, steelId)
        infos.append(info)
    return infos


def getRec(enumIndex, defect):
    """获取坐标矩形 缺陷"""
    if dbm.isSqlServer():
        return [defect.TopInImg + config.HEIGHT * defect.ImageIndex, defect.RightInImg + enumIndex * config.WIDTH,
                defect.BottomInImg - defect.TopInImg,
                defect.RightInImg - defect.LeftInImg,
                ]
    else:
        defect: bkjc_database.NerCarDataBase.mysql.Ncdhotstripdefect.Camdefect1
        return [defect.topInImg + config.HEIGHT * defect.imgIndex, defect.rightInImg + enumIndex * config.WIDTH,
                defect.bottomInImg - defect.topInImg,
                defect.rightInImg - defect.leftInImg,
                ]


import bkjc_database


def getBox(defect, scale=1):
    if dbm.isSqlServer():
        from bkjc_database.NerCarDataBase.sqlserver.models import ClientDefectDB1
        defect: ClientDefectDB1.Defect
        box = [defect.LeftInImg, defect.TopInImg, defect.RightInImg - defect.LeftInImg,
               defect.BottomInImg - defect.TopInImg]
        return box
    else:
        defect: bkjc_database.NerCarDataBase.mysql.Ncdhotstripdefect.Camdefect1
        box = [defect.leftInSrcImg, defect.topInSrcImg, defect.rightInSrcImg - defect.leftInSrcImg,
               defect.bottomInImg - defect.topInSrcImg]
        out = [-10, -10, 20, 20]
        return [int(i * scale) + j for i, j in zip(box, out)]


def getDefectListByDefectInfo(seqNo, defectsInfo=None):
    if not defectsInfo:
        defectsInfo = dbm.getDefectBySeqNo(seqNo)
    res = [[], []]
    for bmIndex, cameraIds in enumerate([defectsInfo["upCameraList"], defectsInfo["downCameraList"]]):
        #  bmIndex 0 上表面 1 下表面
        for enumIndex, cameraId in enumerate(cameraIds):
            for defect in defectsInfo[cameraId]["defect"]:
                try:
                    api_core.get_defectInfo(cameraId, defect.DefectNo)
                except:
                    api_core.get_defectInfo(cameraId, defect.defectID)

                defectInfo = {}
                if dbm.isSqlServer():
                    from bkjc_database.NerCarDataBase.sqlserver.models.ClientDefectDB1 import Defect
                    defect: Defect
                    rec = getRec(enumIndex, defect)
                    box = getBox(defect)
                    defectInfo = {
                        "defectNo": defect.DefectNo,  # 单个缺陷本身的Id
                        "defectID": defect.Class,  # 缺陷类别的Id
                        "bmIndex": 1 - bmIndex,  # 上表面1 下表面0
                        "seqNo": seqNo,
                        "cameraId": cameraId,
                        "imageIndex": defect.ImageIndex,
                        "defectX": rec[0],
                        "defectY": rec[1],
                        "defectWidth": rec[2],
                        "defectHeight": rec[3],
                        "leftInImg": defect.LeftInImg,
                        "rightInImg": defect.RightInImg,
                        "topInImg": defect.TopInImg,
                        "bottomInImg": defect.BottomInImg,
                        "leftInSteel": defect.LeftInSteel,
                        "rightInSteel": defect.RightInSteel,
                        "topInSteel": defect.TopInSteel,
                        "bottomInSteel": defect.BottomInSteel,
                        "rec": rec,
                        "box": box,
                        "boxX": box[0],
                        "boxY": box[1],
                        "boxW": box[2],
                        "boxH": box[3],
                        "defectCoefficient": f"{defect.Grade} %",
                        "grade": defect.Grade,
                        "area": defect.Area
                    }
                else:
                    from bkjc_database.NerCarDataBase.mysql.models.ncdplatedefect import Camdefect1
                    defect: Camdefect1
                    rec = getRec(enumIndex, defect)
                    box = getBox(defect, 0.25)
                    defectInfo = {
                        "defectNo": defect.defectID,  # 单个缺陷本身的Id
                        "defectID": defect.defectClass,  # 缺陷类别的Id
                        "bmIndex": 1 - bmIndex,  # 上表面1 下表面0
                        "seqNo": seqNo,
                        "cameraId": cameraId,
                        "imageIndex": defect.imgIndex-1,
                        "defectX": rec[0],
                        "defectY": rec[1],
                        "defectWidth": rec[2],
                        "defectHeight": rec[3],
                        "leftInImg": defect.leftInImg,
                        "rightInImg": defect.rightInImg,
                        "topInImg": defect.topInImg,
                        "bottomInImg": defect.bottomInImg,
                        "leftInSteel": defect.leftInObj,
                        "rightInSteel": defect.rightInObj,
                        "topInSteel": defect.topInObj,
                        "bottomInSteel": defect.bottomInObj,
                        "rec": rec,
                        "box": box,
                        "boxX": box[0],
                        "boxY": box[1],
                        "boxW": box[2],
                        "boxH": box[3],
                        "defectCoefficient": f"{defect.grade} %",
                        "grade": defect.grade
                    }
                api_core.set_defectInfo(cameraId, defectInfo["defectNo"], defectInfo)
                res[bmIndex].append(defectInfo)
    return res

def tryGetWidthInfo(source):
    if config.useLoc:
        source = "test/width.txt"
    try:
        with open(source) as f:
            lined = f.read().split("\n")
            seqNo, imageCount = [item.split('=')[1] for item in lined[0].split("&")]
            steelLen, steelLeft, steelRight, imageIndex = zip(*[item.split("&") for item in lined[2:]])
            return {
                "seqNo": int(seqNo),
                "imageCount": int(imageCount),
                "steelLen": [int(i) for i in steelLen],  # list
                "steelLeft": [int(i) for i in steelLeft],
                "steelRight": [int(i) for i in steelRight],
                "imageIndex": [int(i) for i in imageIndex]
            }
    except BaseException as e:
        print("文件读取失败！")
        print(source)
        logging.error(e)
        return {
            "imageCount": 50,
        }

def getWidthInfos(seqNo, cameraList):
    """
    获取宽度文件


    """
    if dbm.isSqlServer():
        return [[tryGetWidthInfo(r"\\{}\Width{}\{}\width.txt".format(
            config.TopFace if not bmIndex else config.BottomFace,
            cameraIndex,
            getNumStr(seqNo, 6)
        )) for cameraIndex in cameraIndex] for bmIndex, cameraIndex in
            enumerate(cameraList)]
    else:
        res=[]
        for bmIndex, cameraIndex in enumerate(cameraList):
            ress=[]
            for cameraId in cameraIndex:
                source = config.getFolderBySeqNo_4d0(cameraId, seqNo)
                ress.append({
                    "imageCount": len(list(Path(source).glob("*.*")))
                })
            res.append(ress)
        return res


@app.get("/getDefectView/{seqNo:int}")
def getDefectView(seqNo: int):
    global defectItemCache
    """
    根据steelId 返回. \n
    :param seqNo:
    :return: 上下表面缺陷数据集合
    """
    defectInfo = dbm.getDefectBySeqNo(seqNo)
    upWidthInfo, downWidthInfo = getWidthInfos(seqNo, [defectInfo["upCameraList"],
                                                       defectInfo["downCameraList"]])
    defectListUp, defectListDown = getDefectListByDefectInfo(seqNo, defectInfo)
    defectListUp.sort(key=lambda item: item["imageIndex"])
    defectListDown.sort(key=lambda item: (item["imageIndex"], item["cameraId"]))
    upImageCount = upWidthInfo[0]["imageCount"] if upWidthInfo else 0
    downImageCount = downWidthInfo[0]["imageCount"] if upWidthInfo else 0
    if dbm.isSqlServer():
        reData = {
            "up": {
                "steelInfo": {
                    #   钢板信息
                    "imageCount": upImageCount,
                    "drawWidth": upImageCount * config.WIDTH,  # 渲染长度，
                    "drawHeight": config.WIDTH * config.CAMERA_COUNT  # 渲染高度，会拉伸/挤压到渲染区域的高度  （这里的高度指转换后的实际宽度）
                },
                "defectList": defectListUp,
                "outLineUp": [],
                "outLineDown": []
            },
            "down": {
                "steelInfo": {
                    #   钢板信息
                    "imageCount": downImageCount,
                    "drawWidth": downImageCount * config.HEIGHT,  # 渲染长度，
                    "drawHeight": config.WIDTH * config.CAMERA_COUNT  # 渲染高度，会拉伸/挤压到渲染区域的高度  （这里的高度指转换后的实际宽度）
                },
                "defectList": defectListDown,
                "outLineUp": [],
                "outLineDown": []
            },
        }
    else:

        reData = {
            "up": {
                "steelInfo": {
                    #   钢板信息
                    "imageCount": upImageCount,
                    "drawWidth": upImageCount * config.WIDTH,  # 渲染长度，
                    "drawHeight": config.WIDTH * config.CAMERA_COUNT  # 渲染高度，会拉伸/挤压到渲染区域的高度  （这里的高度指转换后的实际宽度）
                },
                "defectList": defectListUp[:2000],
                "outLineUp": [],
                "outLineDown": []
            },
            "down": {
                "steelInfo": {
                    #   钢板信息
                    "imageCount": downImageCount,
                    "drawWidth": downImageCount * config.HEIGHT,  # 渲染长度，
                    "drawHeight": config.WIDTH * config.CAMERA_COUNT  # 渲染高度，会拉伸/挤压到渲染区域的高度  （这里的高度指转换后的实际宽度）
                },
                "defectList": defectListDown[:2000],
                "outLineUp": [],
                "outLineDown": []
            },
        }
    return reData


@app.get("/DefectDict")
def getDefectDict():
    """
    获取缺陷字典 {id:{color:"",name:"" ...}} \n
    :return:
    """
    defects = dbm.getDefectClass()
    if dbm.isSqlServer():
        return {defect.ID: {
            "name": defect.Name,
            "color": webcolors.rgb_to_hex((defect.Red, defect.Green, defect.Blue)),
            "id": defect.Class,
            "grade": defect.Grade
            # 根据需求增加
        } for defect in defects}
    else:
        return defects


def getNumStr(num, size=4):
    num = str(num)
    return (size - len(num)) * "0" + num


# def cacheMaxImageByDefectInfo(cameraId=None, seqNo=None, imageIndex=None, defectInfo_=None):
#     """
#     缺陷小兔额获取
#     """
#     global defectItemCache
#     if defectInfo_:
#         cameraId = defectInfo_["cameraId"]
#         seqNo = defectInfo_["seqNo"]
#         imageIndex = defectInfo_["imageIndex"]
#     return api_core.get_defect_max_cimage(cameraId,seqNo,imageIndex)


@app.get("/maxImage/{cameraID:int}/{seqNo:int}/{imageIndex:int}")
def getMaxImage(cameraID: int, seqNo: int, imageIndex: int):
    """BUG 调用前请调用 getimage"""
    return StreamingResponse(getImageIO(api_core.get_defect_max_cimage(cameraID, seqNo, imageIndex)),
                             media_type="image/jpeg")


@app.get("/image/{cameraId:int}/{defectId:int}")
def getimage(cameraId: int, defectId: int):
    """
    获取缺陷图像
    """
    return getDefectImage(cameraId, defectId)


@app.get("/defectImage/{cameraID:int}/{defectID:int}")
def getDefectImage(cameraID, defectID):
    """
    4.0 only
    """
    if dbm.isSqlServer():
        pass
    else:
        defect = dbm.getDefectItem(cameraID, defectID)
        if defect:
            defect: bkjc_database.NerCarDataBase.mysql.Ncdhotstripdefect.Camdefect1
            source = config.getDefectImgFile_4d0(defect.camNo, defect.seqNo, defect.defectID)
            if source:
                image = Image.open(source)
                return StreamingResponse(getImageIO(image), media_type="image/jpeg")
    defectInfo = api_core.get_defectInfo(cameraID, defectID)
    image = api_core.get_defect_max_cimage(cameraID, defectInfo["seqNo"], defectInfo["imageIndex"])
    box = defectInfo['box']
    return StreamingResponse(getImageIO(image.crop(
        (box[0], box[1], box[0] + box[2], box[1] + box[3])
    )), media_type="image/jpeg")


@app.get("/defectImage2/{cameraID:int}/{seqNo:int}/{defectID:int}")
def getDefectImage2(cameraID, seqNo, defectID):
    """
    通过 相机ID， 流水号， 缺陷ID 查找缺陷图像
    4.0 only
    """
    if dbm.isSqlServer():
        dbm.getDefectItem(cameraID, defectID)
        raise
    else:
        source = config.getDefectImgFile_4d0(cameraID, seqNo, defectID)
        image = Image.open(source)
        return StreamingResponse(getImageIO(image), media_type="image/jpeg")


@app.get("/getAppFlush/{currentSeqID:int}/{maxID:int}")
def getAppFlush(currentSeqID, maxID):
    reData = {
        "appendSteel": [addSteelCache(steel, steelId) for steel, steelId in dbm.getSteelByNum(1, False, maxID)][::-1],
    }
    return reData


@app.get("/getRealInfoById/{steelId:int}")
def getRealInfoById(steelId):
    res = dbm.getSteelById(steelId)
    if res:
        res = res[0][0]
        if not res:
            return {"msg": "没有找到数据"}
        # res:Steel
        try:
            seqNo = res.SequeceNo
        except:
            seqNo = res.seqNo
        defectInfo = dbm.getDefectBySeqNo(seqNo)
        defectListUp, defectListDown = getDefectListByDefectInfo(seqNo, defectInfo)
        reData = {
            "up": {
                "steelInfo": {
                    #   钢板信息
                    # "imageCount": upWidthInfo[0]["imageCount"],
                    # "drawWidth": upWidthInfo[0]["imageCount"] * 1024,  # 渲染长度，
                    "drawHeight": 4096 * 2  # 渲染高度，会拉伸/挤压到渲染区域的高度  （这里的高度指转换后的实际宽度）
                },
                "defectList": defectListUp,
                "outLineUp": [],
                "outLineDown": []
            },
            "down": {
                "steelInfo": {
                    #   钢板信息
                    # "imageCount": downWidthInfo[0]["imageCount"],
                    # "drawWidth": downWidthInfo[0]["imageCount"] * 1024,  # 渲染长度，
                    "drawHeight": 4096 * 2  # 渲染高度，会拉伸/挤压到渲染区域的高度  （这里的高度指转换后的实际宽度）
                },
                "defectList": defectListDown,
                "outLineUp": [],
                "outLineDown": []
            },
        }
        print(res)
        return {  # "lastObj": addSteelCache(res[0], res[1]),
            "data": reData
        }


@app.get("/searchByID/{id_:int}")
def searchByID(id_):
    try:
        return [addSteelCache(steel, steelId) for steel, steelId in dbm.getSteelBySeqNo(id_)]
    except BaseException as e:
        logging.error(e)
    return []


@app.get("/searchBySteelNo/{steelNo:str}")
def searchBySteelNo(steelNo):
    try:
        return [addSteelCache(steel, steelId) for steel, steelId in dbm.getSteelBySteelNo(steelNo)]
    except BaseException as e:
        logging.error(e)
    return []


@app.get("/searchByDate/{startTime:str}/{endTime:str}")
def searchByDate(startTime, endTime):
    """
    %Y-%m-%d %H:%M:%S
    """
    try:
        startTime = datetime.datetime.strptime(startTime, config.TIMESTAMP_FORMAT)
        endTime = datetime.datetime.strptime(endTime, config.TIMESTAMP_FORMAT)
        print(startTime)
        print(endTime)
        return [addSteelCache(steel, steelId) for steel, steelId in dbm.getSteelByDate(startTime, endTime)]
    except BaseException as e:
        logging.error(e)
    return []


@app.get("/widths/{steelId:str}")
def getWidths(steelId):
    # if config.useLoc:
    #     return getWidthInfos(steelId, [[1], [2]])
    res = getWidthInfos(steelId, dbm.getCameraList())
    return res


@app.get("/restartServer")
def restartServer():
    tool.killApp()


@app.get("/getGradeInfo/{seqNo:int}")
def getGradeInfo(seqNo):
    """
    获取 钢板的缺陷数据
    """
    res = api_core.getGradeInfo(seqNo)
    print(res)
    return res


@app.get("/getSharedFolder/{url_:str}")
def getSharedFolder(url_):
    print(url_)


if __name__ == "__main__":
    print(getWidths())
    pass
