#  encoding = utf-8
import os
import ctypes
import shutil
import threading

from PIL import Image

import sys
import numpy as np

from CONFIG import DLL_PATH, WIDTH, HEIGHT, POOL_SIZE

dllPath = os.path.join(DLL_PATH, "CimgRead.dll")
base_encoding = "gbk"


def loadDll(dll_url):
    """
    Load a DLL file.
    Args:
        dll_url (str): The path to the DLL file.
    Returns:
        ctypes.CDLL: The loaded DLL file.
    """
    print(fr"loadDll {sys.version_info}")
    if sys.version_info.major >= 3 and sys.version_info.minor >= 8:
        os.add_dll_directory(DLL_PATH)
        return ctypes.CDLL(dll_url, winmode=0)
    else:
        return ctypes.windll.LoadLibrary(dll_url)


CimgReadDll = loadDll(dllPath)


def ReadCimgToImage(from_cimg_fileName: str, width=4096, height=1024):
    """
    Read a Cimg file and convert it to a PIL Image object.

    Args:
        from_cimg_fileName (str): The path to the Cimg file.
        width (int): The desired width of the image. Default is 4096.
        height (int): The desired height of the image. Default is BASE_HEIGHT.

    Returns:
        PIL.Image.Image: The converted image.
    """
    image = Image.fromarray(ReadCimgToNumpyArray(from_cimg_fileName, width, height))
    image = image.crop((0, 0, width, height))
    return image


def ReadCimgToNumpyArray(from_cimg_fileName: str, width=WIDTH, height=HEIGHT):
    """
    Read a Cimg file and convert it to a NumPy array.

    Args:
        from_cimg_fileName (str): The path to the Cimg file.
        width (int): The desired width of the array. Default is 4096.
        height (int): The desired height of the array. Default is BASE_HEIGHT.

    Returns:
        np.ndarray: The converted NumPy array.
    """
    buff = ctypes.create_string_buffer(width * height)
    ReadCimgDataToBuff(buff, from_cimg_fileName)
    array: np.ndarray
    array = np.frombuffer(buff, np.uint8)
    return array.reshape(height, width)


class OldCimgRead:
    def __init__(self, index):
        """
        Initialize an instance of OldCimgRead.

        Args:
            index (int): The index of the instance.
        """
        self.lock = threading.Lock()
        dllPath = os.path.join(DLL_PATH, "OldCimgRead{}.dll".format(index))
        if not os.path.exists(dllPath):
            dllPathBase = os.path.join(DLL_PATH, "OldCimgRead{}.dll".format(1))
            shutil.copy(dllPathBase, dllPath)
        self.dll = loadDll(dllPath)

    def ReadCimgData(self, from_cimg_fileName, buff):
        """
        Read Cimg data and store it in the provided buffer.

        Args:
            from_cimg_fileName (bytearray): The path to the Cimg file.
            buff (ctypes.c_char_p): The buffer to store the data.
        """
        self.lock.acquire()
        try:
            self.dll.ReadCimgData(from_cimg_fileName, buff)
        finally:
            self.lock.release()

    def ReadCimgDataToBuff(self, buff, from_cimg_fileName: str):
        """
        Read Cimg data and store it in the provided buffer.

        Args:
            buff (ctypes.c_char_p): The buffer to store the data.
            from_cimg_fileName (str): The path to the Cimg file.
        """
        self.lock.acquire()
        try:
            self.dll.ReadCimgData(from_cimg_fileName.encode(base_encoding), buff)
        finally:
            self.lock.release()

    def locked(self):
        """
        Check if the instance is locked.

        Returns:
            bool: True if locked, False otherwise.
        """
        return self.lock.locked()


oldCimgDllList = []
semaphore = threading.Semaphore(POOL_SIZE)
try:
    for i in range(POOL_SIZE):
        oldCimgDllList.append(OldCimgRead(i))
except BaseException as e:
    print(e)


def getOldCimgDll() -> OldCimgRead:
    """
    Get an available instance of OldCimgRead.

    Returns:
        OldCimgRead: An available instance of OldCimgRead.
    """
    global oldCimgDllList

    for oldCimgdll in oldCimgDllList:
        if not oldCimgdll.locked():
            return oldCimgdll
    return getOldCimgDll()


def ReadCimgDataToBuff(buff, from_cimg_fileName: str, systemVersion=0):
    """
    Read Cimg data and store it in the provided buffer.

    Args:
        buff (ctypes.c_char_p): The buffer to store the data.
        from_cimg_fileName (str): The path to the Cimg file.
        systemVersion (int): The system version. Default is 0.
    """
    from_cimg_fileName = from_cimg_fileName.replace("\\", "/")
    dll = CimgReadDll if systemVersion == 1 else getOldCimgDll()
    dll.ReadCimgData(from_cimg_fileName.encode(base_encoding), buff)


def ReadCimgData(from_cimg_fileName: str, size=HEIGHT * WIDTH, systemVersion=0):
    """
    Read Cimg data and return it as a ctypes buffer.

    Args:
        from_cimg_fileName (str): The path to the Cimg file.
        size (int): The size of the buffer. Default is BASE_HEIGHT * 4096.
        systemVersion (int): The system version. Default is 0.

    Returns:
        ctypes.c_char_p: The ctypes buffer containing the data.
    """
    buff = ctypes.create_string_buffer(size)
    ReadCimgDataToBuff(buff, from_cimg_fileName, systemVersion=systemVersion)
    return buff


if __name__=="__main__":
    ReadCimgData("C:\\project\\bkjc_api\\test\\test4d0.cimg",size=5096*1024*4*4,systemVersion=1)