import json
import socket
from pathlib import Path

from core import get_path, get_config_path

maxSteelInfoCache = 200
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"
MAIN_INFO = json.load(Path(get_path("config/info.json")).open("r", encoding="utf-8"))
info = MAIN_INFO

locType = info["locType"] if "locType" in info else "3.0"


def isLoc():
    # 是否未本机
    locConfig = info["useLoc"] if "useLoc" in info else False
    if socket.gethostname() in ["lcx_ace"]:
        return True
    return locConfig


# 4.0 系统的缺陷读取
defectClassFile = info["defectClassFile"] if "defectClassFile" in info else get_config_path("config/DefectClass.json")

# 转接模式,转发表面检测数据
forwarder = info["forwarder"] if "forwarder" in info else False
forward_url = info["forward_url"] if "forward_url" in info else ""

# 是否是PLC数据转发
plcForwarder = info["plcForwarder"] if "plcForwarder" in info else False
plcForwarderUrl = info["plcForwarderUrl"] if "plcForwarderUrl" in info else ""
plcForwarderRack = info["plcForwarderRack"] if "plcForwarderRack" in info else 0
plcForwarderSlot = info["plcForwarderSlot"] if "plcForwarderSlot" in info else 4


DEFECT_GET_HQ_TYPE = 1
DEFECT_GET_DEFECT_TYPE = 2
defectType = DEFECT_GET_DEFECT_TYPE
database_type = info["database_type"] if "database_type" in info else ""

WIDTH = info["WIDTH"]
HEIGHT = info["HEIGHT"]
old_dllRead_poolSize = 20
CAMERA_COUNT = 2
TopFace = info["TopFace"]
BottomFace = info["BottomFace"]
maxSave = info["epochSize"] if "epochSize" in info else 60000
maxEpoch = info["epoch"] if "epoch" in info else 9999
cropDefect = info["cropDefect"] if "cropDefect" in info else False

useYolo = False

FILES_DIRECTORY = Path(get_path("./files"))

UPLOAD_DIRECTORY = FILES_DIRECTORY / "uploaded_files"
UPLOAD_DIRECTORY.mkdir(exist_ok=True, parents=True)
DOWNLOAD_DIRECTORY = FILES_DIRECTORY / "downloaded_files"
DOWNLOAD_DIRECTORY.mkdir(exist_ok=True, parents=True)
CLIENT_DIRECTORY = FILES_DIRECTORY / "client_files"
CLIENT_CONFIG_FILE = CLIENT_DIRECTORY / "info.json"
CLIENT_DIRECTORY.mkdir(exist_ok=True, parents=True)

base_encoding = "utf-8"

def getInfo():
    return MAIN_INFO

def getFolderBySeqNo(cameraId, seqNo):
    ip = info["TopFace"] if int(cameraId) in info["upCamera"] else info["BottomFace"]
    imgUrl = info["source"].format(ip, str(cameraId), str(int(seqNo) % maxSave).rjust(info["sourceLen"], "0"))
    loopIndex = (int(int(seqNo) / maxSave) % maxEpoch)
    if loopIndex % maxEpoch:
        return Path(imgUrl) / str(loopIndex % maxEpoch)
    return Path(imgUrl)

def getCimgFile(cameraId, seqNo, imageIndex):
    if useLoc:
        return f"test/cimg/imageSource{cameraId}/041447/{str(imageIndex).rjust(4, '0')}.cimg"
    return str(Path(getFolderBySeqNo(cameraId, seqNo)) / f"{str(imageIndex).rjust(4, '0')}.cimg")


def getDefectFolder_4d0(cameraId, seqNo):
    ip = info["TopDefect"] if int(cameraId) in info["upCamera"] else info["BottomDefect"]
    imgUrl = info["defectSource"].format(ip, str(int(seqNo)))
    return imgUrl


def getDefectImgFile_4d0(cameraId, seqNo, defectId):
    if cropDefect:
        return None
    return str(Path(getDefectFolder_4d0(cameraId, seqNo)) / f"{str(defectId)}.bmp")


def getFolderBySeqNo_4d0(cameraId, seqNo):
    ip = info["TopFace"] if int(cameraId) in info["upCamera"] else info["BottomFace"]
    imgUrl = info["source"].format(ip, str(int(seqNo)))
    return imgUrl


def getImgFile_4d0(cameraId, seqNo, imageIndex):
    return str(Path(getFolderBySeqNo_4d0(cameraId, seqNo)) / f"{str(imageIndex)}.jpg")


steelLevelEnable = info["steelLevelEnable"] if "steelLevelEnable" in info else False
xlsxFile = get_config_path('涟钢钢板质量判定标准表(横切、热处理线）2023.8.25.xlsx')
steelLevelUrl = "http://172.25.2.43:900"
steelLevelTemplateDataOut = get_path("template/templateDataOut.xlsx")
plant_classification = "热处理一厂"
productionLine_classification = "横切一号线"
steelLevelTabelServerUrl = info["steelLevelTabelServerUrl"] if "steelLevelTabelServerUrl" in info else False


ipListJson = get_config_path("ipList.json")

conditionMonitoringEnable = info["conditionMonitoringEnable"] if "conditionMonitoringEnable" in info else False

if __name__ == "__main__":
    print(getFolderBySeqNo(2, 315580))