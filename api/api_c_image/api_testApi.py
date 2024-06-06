from os.path import *
import time

from PIL import Image

from core import testApp as app
import config
import tool
from fastapi.responses import StreamingResponse
from bkjc_tools import CimgReadCore
from api.api_core import api_core


@app.get("/file/{fileUrl:path}")
async def getFile(fileUrl: str = ""):
    """
    通过指定路径，文件的直接访问支持常规文件 例如 图像，PDF，txt ... \n
    该接口主要测试使用。 \n
    :param fileUrl: \n
    :return:        \n
    """
    print(fileUrl)
    if exists(fileUrl):
        file_like = open(fileUrl, mode="rb")
        return StreamingResponse(file_like)
    return {"文件不存在 !"}


@app.get("/img/count/{fileUrl:path}")
def get_file_cunt(fileUrl):
    """
    根据文件夹 获取表检图像数量    \n
    测试使用    \n
    :param fileUrl:        \n
    :return: int 图像的数量        \n
    """
    return len(tool.getImgList(fileUrl))


@app.get("/img/join/{fileUrl:path}")
async def get_all_join_file(fileUrl: str, resize: int = 4096, start: int = 0, end: int = 0):
    """
    从文件夹 获取 纵向拼接的图像文件    \n
    测试使用    \n
    :param end:    结束序号（可选）    \n
    :param start: 起始序号（可选）    \n
    :param resize: 设置拼接图像    \n
    :param fileUrl: 文件夹的路径    \n
    :return: HTTP 图像    \n
    """
    return tool.get_all_join_file(fileUrl, resize, start, end)


@app.get("/img/{fileUrl:path}")
def getCimg(fileUrl: str = "", resize: int = 4096):
    """
    访问 cimg 文件，解析为 jpg 返回

    :param resize: 可选参数，图像返回的宽度
    :type resize: int
    :param fileUrl: 路径
    :type fileUrl: str
    :return: 返回一个 StreamingResponse 对象，包含解析后的图像数据
    :rtype: StreamingResponse
    """
    sTime = time.time()
    if not exists(fileUrl):
        return {"msg": "文件不存在 !",
                "code": 404}
    try:
        resize_factor = resize / config.WIDTH
        img = Image.fromarray(CimgReadCore.ReadCimgToNumpyArray(fileUrl))
        if resize != config.WIDTH:
            img = img.resize((resize, int(resize_factor * config.HEIGHT)))
        return StreamingResponse(tool.getImageIO(img), media_type="image/jpeg")
    except BaseException as e:
        return {str(e)}
    finally:
        eTime = time.time()
        print("请求 {} 耗时 {} S".format(fileUrl, eTime - sTime))


@app.get("/cimg/{cameraIndex:int}/{seqNo:int}/{imageIndex:int}/{resize:int}")
def cimg(cameraIndex, seqNo, imageIndex, resize=4096):
    """
    获取图像
    """
    img = api_core.get_cimage(cameraIndex, seqNo, imageIndex)

    if resize != config.WIDTH:
        resize_factor = resize / config.WIDTH
        img = img.resize((resize, int(resize_factor * config.HEIGHT)))
    return StreamingResponse(tool.getImageIO(img), media_type="image/jpeg")
