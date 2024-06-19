from core import mainApp as app, tool
from bkjc_database.dbm import dbm

import config

@app.get("/")
async def home():
    """
    入口
    :return: A dictionary with a message indicating the purpose of the service and the available API endpoints.
    """
    return {"msg": "本服务主要用于请求图像，api接口可以访问 openapi.json， 文档请访问 /docs  或 /redoc"}


@app.get("/steel_info")
async def getSteelInfo(steelNo: str = ""):
    """
    根据钢板号获取钢板信息
    :param steelNo: 钢板号
    :return: 钢板信息
    """
    return dbm.getSteelInfo(steelNo)


@app.get("/info")
async def getCameraInfo():
    """
    获取相机信息
    :return: 相机信息
    """
    return tool.getInfo()


@app.get("/count")
async def get_image_Count(steelNo="", cameraId=0):
    """
    根据钢板号和相机ID获取各相机图像数量，不指定相机ID则返回对应字典
    :param steelNo: 钢板号
    :param cameraId: 相机ID
    :return: 图像数量
    """
    seqNo = dbm.getSeqIdBySteelNo(steelNo)
    if cameraId:
        url = config.getFolderBySeqNo(cameraId, seqNo)
        return len(tool.getImgList(url))
    else:
        return {k: config.getFolderBySeqNo(k, seqNo) for k in config.getInfo()["folders"]}


@app.get("/search")
async def get_img_by_steelNo(steelNo="", cameraId="1", resize=4096, start=0, end=0):
    """
    根据钢板号、相机ID和图像位置获取对应的图像
    :param resize: 图像resize
    :param steelNo: 查询的钢板号
    :param cameraId: 相机ID
    :param start: 起始的图像ID
    :param end: 结束的图像ID
    :return: 图像
    """
    seqNo = dbm.getSeqIdBySteelNo(steelNo)
    if not seqNo:
        return {"msg": "未找到记录！", "code": 404}
    folder = config.getFolderBySeqNo(cameraId, seqNo)
    return tool.get_all_join_file(folder, resize, start, end)

