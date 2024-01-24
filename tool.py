import time
from os.path import *
from io import BytesIO
from glob import glob
from PIL import Image
from bkjc_tools import CimgReadCore
import config
from fastapi.responses import StreamingResponse
import os
import signal


def getImageIO(image: Image.Image, format="jpeg"):
    """
    Converts the given PIL Image object to BytesIO object.

    Args:
        image (Image.Image): The PIL Image object to convert.
        format (str, optional): The image format. Defaults to "jpeg".

    Returns:
        BytesIO: The converted BytesIO object.
    """
    bytesIO = BytesIO()
    image.save(bytesIO, format=format)
    bytesIO.seek(0)
    return bytesIO


def joinCimg(fileList, resize=4096):
    """
    Joins multiple cimg files into a single image.

    Args:
        fileList (list): List of cimg file paths.
        resize (int, optional): The resize value. Defaults to 4096.

    Returns:
        Image.Image: The joined image.
    """
    resize = int(resize)
    resize_factor = resize / config.WIDTH
    maxImage = Image.new("L", (int(config.WIDTH * resize_factor), int(config.HEIGHT * len(fileList) * resize_factor)))
    w, h = maxImage.size
    for index, f_ in enumerate(fileList):
        itemImage = CimgReadCore.ReadCimgToImage(f_, config.WIDTH, config.HEIGHT)
        itemImage = itemImage.resize((w, int(config.HEIGHT * resize_factor)))
        itemW, itemH = itemImage.size
        maxImage.paste(itemImage, (0, index * itemH, itemW, int((index + 1) * itemH)))
    return maxImage


def getImgList(fileUrl, tp="*.cimg", start=0, end=0):
    """
    Retrieves a list of image files in the specified directory.

    Args:
        fileUrl (str): The directory path.
        tp (str, optional): The file type pattern. Defaults to "*.cimg".
        start (int, optional): The start index of the image list. Defaults to 0.
        end (int, optional): The end index of the image list. Defaults to 0.

    Returns:
        list: The list of image file paths.
    """
    imgList = glob(join(fileUrl, tp))
    if end:
        imgList = imgList[int(start):int(end)]
    return imgList


def getInfo():
    """
    Retrieves information from the config module.

    Returns:
        dict: The information dictionary.
    """
    return config.getInfo()


def get_all_join_file(fileUrl, resize, start, end):
    """
    Retrieves and joins all image files in the specified directory.

    Args:
        fileUrl (str): The directory path.
        resize (int): The resize value.
        start (int): The start index of the image list.
        end (int): The end index of the image list.

    Returns:
        StreamingResponse: The streaming response containing the joined image.
    """
    if not exists(fileUrl) or not isdir(fileUrl):
        return {
            "msg": "{} 图像文件夹 不存在".format(fileUrl),
            "code": 404
        }
    else:
        if exists(join(fileUrl, "info.json")):
            pass
        sTime = time.time()
        imageIO = getImageIO(joinCimg(getImgList(fileUrl, start=start, end=end), resize))
        eTime = time.time()
        print(eTime - sTime)
        return StreamingResponse(imageIO)


def killApp():
    """
    Kills the ApiServer.exe process and its child processes.

    Returns:
        None
    """
    return os.killpg(os.getpgid(0), signal.SIGTERM)

