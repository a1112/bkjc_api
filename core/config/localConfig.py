from .BaseConfig import *

if locType == "4.0":
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
        "useLoc": True,
        "steelLevelEnable": True,
        "conditionMonitoringEnable": True
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
        "useLoc": True,
        "steelLevelEnable": True,
        "conditionMonitoringEnable": True
    }

steelLevelEnable = False
