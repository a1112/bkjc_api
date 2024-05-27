from bkjc_database.NerCarDataBase.mysql import Ncdplatedevice
from threading import Thread
import time

CameraInfo = {}
LightInfo = {}


class getThread(Thread):

    def __init__(self):
        super().__init__()

    def run(self):
        global CameraInfo, LightInfo
        while True:
            CameraInfo = Ncdplatedevice.deviceDb.getCameraInfo()
            LightInfo = Ncdplatedevice.deviceDb.getLightInfo()
            time.sleep(5)


gt = getThread()
gt.start()


def getCameraInfo():
    return CameraInfo


def getLightInfo():
    return LightInfo


if __name__ == "__main__":
    time.sleep(5)
    print(getCameraInfo())
