import sys
import os
import json
from pathlib import Path


def get_path(path_name):
    return os.path.join(os.path.dirname(sys.executable) if "python.exe" not in sys.executable else
                        os.path.dirname(__file__), path_name)


MAIN_INFO = json.load(Path(get_path("config/info.json")).open("r",encoding="utf-8"))

info = MAIN_INFO
useLoc = info["useLoc"] if "useLoc" in info else False
maxSteelInfoCache = 200
if useLoc:
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

from bkjc_database import core


core.setBaseUrl(ip=info["upServer"], port=1433, user=info["user"], password=info["password"], drive_=info["drive"],
                chart='utf8')
DEFECT_GET_HQ_TYPE=1
DEFECT_GET_DEFECT_TYPE=2
defectType=DEFECT_GET_DEFECT_TYPE

database_type = info["database_type"] if "database_type" in info else ""

print(f"database_type {database_type}")
WIDTH = info["WIDTH"]
HEIGHT = info["HEIGHT"]
old_dllRead_poolSize = 20
CAMERA_COUNT = 2
TopFace = info["TopFace"]
BottomFace = info["BottomFace"]
maxSave = info["maxSave"] if "maxSave" in info else 60000
maxEpoch = info["maxEpoch"] if "maxEpoch" in info else 4
useYolo = False

FILES_DIRECTORY = Path(get_path("./files"))

UPLOAD_DIRECTORY = FILES_DIRECTORY/"uploaded_files"
UPLOAD_DIRECTORY.mkdir(exist_ok=True, parents=True)
DOWNLOAD_DIRECTORY = FILES_DIRECTORY/"downloaded_files"
DOWNLOAD_DIRECTORY.mkdir(exist_ok=True, parents=True)
CLIENT_DIRECTORY = FILES_DIRECTORY/"client_files"
CLIENT_CONFIG_FILE = CLIENT_DIRECTORY/"info.json"
CLIENT_DIRECTORY.mkdir(exist_ok=True, parents=True)


base_encoding = "utf-8"


def getInfo():
    return MAIN_INFO


def getFolderBySeqNo(cameraId, seqNo):
    ip = info["TopFace"] if int(cameraId) in info["upCamera"] else info["BottomFace"]
    imgUrl = info["source"].format(ip, str(cameraId), str(int(seqNo) % maxSave).rjust(info["sourceLen"], "0"))
    url = Path(imgUrl) / str(int(int(seqNo) / maxSave) % maxEpoch)
    return url


def getCimgFile(cameraId, seqNo, imageIndex):
    if useLoc:
        return f"test/cimg/imageSource{cameraId}/041447/{str(imageIndex).rjust(4, '0')}.cimg"
    return str(Path(getFolderBySeqNo(cameraId, seqNo)) / f"{str(imageIndex).rjust(4, '0')}.cimg")


def getDefectFolder_4d0(cameraId, seqNo):
    ip = info["TopDefect"] if int(cameraId) in info["upCamera"] else info["BottomDefect"]
    imgUrl = info["defectSource"].format(ip, str(int(seqNo)))
    return imgUrl


def getDefectImgFile_4d0(cameraId, seqNo, defectId):
    return str(Path(getDefectFolder_4d0(cameraId, seqNo)) / f"{str(defectId)}.bmp")


def getFolderBySeqNo_4d0(cameraId, seqNo):
    ip = info["TopFace"] if int(cameraId) in info["upCamera"] else info["BottomFace"]
    imgUrl = info["source"].format(ip, str(int(seqNo)))
    return imgUrl


def getImgFile_4d0(cameraId, seqNo, imageIndex):
    return str(Path(getFolderBySeqNo_4d0(cameraId, seqNo)) / f"{str(imageIndex)}.jpg")


if __name__=="__main__":
    print(getFolderBySeqNo(2,315580))