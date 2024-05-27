import sys
import os
import json
from pathlib import Path
import init
TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

def get_path(path_name):
    return os.path.join(os.path.dirname(sys.executable) if "python.exe" not in sys.executable else
                        os.path.dirname(__file__), path_name)

def get_config_path(path_name):
    return get_path("config/"+path_name)

MAIN_INFO = json.load(Path(get_path("config/info.json")).open("r", encoding="utf-8"))

info = MAIN_INFO
useLoc = info["useLoc"] if "useLoc" in info else False
locType = info["locType"] if "locType" in info else "3.0"
maxSteelInfoCache = 200
if useLoc:
    if locType=="4.0":
        info = {
            "cameraCount": 8,
            "upCamera": [1],
            "downCamera": [2],
            "upServer": "127.0.0.1",
            "system": "4.0",
            "drive": "mysql",
            "user": "root",
            "database_type": "ncdplate",
            "password": "nercar",
            "downServer": "192.168.3.100",
            "source": "\\\\{}\\ImageSource\\{}",
            "sourceLen": 6,
            "TopFace": "TopFace",
            "BottomFace": "BottomFace",
            "ip": "0.0.0.0",
            "port": 809,
            "WIDTH": 4096,
            "HEIGHT": 1024,
            "useLoc": True
        }
    elif locType == "3.0":
        info = {
            "cameraCount": 8,
            "upCamera": [1],
            "downCamera": [2],
            "upServer": "127.0.0.1",
            "system": "3.0",
            "drive": "sqlserver",
            "user": "sa",
            "database_type": "ncdplate",
            "password": "519223",
            "downServer": "192.168.3.100",
            "source": "\\\\{}\\ImageSource{}\\{}",
            "sourceLen": 6,
            "TopFace": "TopFace",
            "BottomFace": "BottomFace",
            "ip": "0.0.0.0",
            "port": 809,
            "WIDTH": 4096,
            "HEIGHT": 1024,
            "useLoc": True
        }
print(info["drive"])

defectClassFile = info["defectClassFile"] if "defectClassFile" in info else get_config_path("DefectClass.json")

forwarder = info["forwarder"] if "forwarder" in info else False
forward_url = info["forward_url"] if "forward_url" in info else ""
if not forwarder:
    init.initDataBase(info)


DEFECT_GET_HQ_TYPE = 1
DEFECT_GET_DEFECT_TYPE = 2
defectType = DEFECT_GET_DEFECT_TYPE

database_type = info["database_type"] if "database_type" in info else ""

print(f"database_type {database_type}")
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

# def getFolderBySeqNo(cameraId, seqNo):
#     ip = info["TopFace"] if int(cameraId) in info["upCamera"] else info["BottomFace"]
#     imgUrl = info["source"].format(ip, str(cameraId), str(int(seqNo) % maxSave).rjust(info["sourceLen"], "0"))
#     folderNo = int(int(seqNo) / maxSave)
#     url = Path(imgUrl) / str(int(int(seqNo) / maxSave) % maxEpoch)
#     return url

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
steelLevelUrl = "http://127.0.0.1:809"
steelLevelTemplateDataOut = get_path("template/templateDataOut.xlsx")

conditionMonitoringEnable = info["conditionMonitoringEnable"] if "conditionMonitoringEnable" in info else False

if __name__ == "__main__":
    print(getFolderBySeqNo(2, 315580))
