from typing import List
from bkjc_database.CONFIG import globDbConfig


from bkjc_database.BaseImport import *
from bkjc_database.SqlBase import init
from bkjc_database.SqlTool import to_dict
from bkjc_database import core
from bkjc_database.NerCarDataBase.mysql.models.ncdplatedevice import Camera

from bkjc_database.property.DataBaseInterFace import DbItem

from bkjc_database.NerCarDataBase.mysql.models.ncdplatedevice import *


class DeviceDb(DbItem):
    def __init__(self):
        if globDbConfig.database_type == "ncdhotstrip":
            self.databaseName = "Ncdplatedevice"
        else:
            self.databaseName = "Ncdplatedevice"
        super().__init__(self.databaseName)

    def getCameraInfo(self):
        lastCamera: Camera
        cameraDict = {}
        with self.Session() as session:
            for c in range(10):
                try:
                    lastCamera = session.query(Camera).where(Camera.cam == c + 1)[-1]
                    dicData = to_dict(lastCamera)
                    dicData["isRun"] = True
                    cameraDict[dicData['cam']] = dicData
                except:
                    break
            return cameraDict

    def getLightInfo(self):
        light: Light
        lightDict = {}
        with self.Session() as session:
            for c in range(10):
                try:
                    lasttlight = session.query(Light)[-1]
                    lasttlight=to_dict(lasttlight)
                    lasttlight["isRun"]=True
                    lightDict[str(lasttlight.LightNo)] = lasttlight
                except:
                    break
            return lightDict


deviceDb = DeviceDb()
Session = deviceDb.Session


deviceDb.createDatabase(Base.metadata)