from bkjc_database.NerCarDataBase.mysql.models import ncdplatedevice
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
            CameraInfo = ncdplatedevice.getCameraInfo()
            LightInfo = ncdplatedevice.getLightInfo()
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
