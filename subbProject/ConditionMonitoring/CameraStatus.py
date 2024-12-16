from bkjc_database.NerCarDataBase.mysql import Ncdplatedevice
from threading import Thread
import time

CameraInfo = {}
LightInfo = {}
RkmonitorInfo={}

class getThread(Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        global CameraInfo, LightInfo,RkmonitorInfo
        while True:
            CameraInfo = Ncdplatedevice.deviceDb.getCameraInfo()
            LightInfo = Ncdplatedevice.deviceDb.getLightInfo()
            RkmonitorInfo = Ncdplatedevice.deviceDb.getRkmonitorInfo()
            time.sleep(2)


gt = getThread()
gt.start()


def getCameraInfo():
    return CameraInfo


def getLightInfo():
    return LightInfo

def getRkmonitorInfo():
    return RkmonitorInfo

if __name__ == "__main__":
    time.sleep(5)
    print(getCameraInfo())
