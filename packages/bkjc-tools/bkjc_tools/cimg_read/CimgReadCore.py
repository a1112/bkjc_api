"""CIMG compatibility API with lazy, serialized access to the vendor decoders.

Importing this module never loads DLLs, copies files, or registers shell handlers.
The vendor ABI still requires the caller's dimensions to match the encoded image.
"""
import ctypes
import os
from pathlib import Path
import sys
import threading

import numpy as np
from PIL import Image
from bkjc_tools.CONFIG import DLL_PATH, WIDTH, HEIGHT, POOL_SIZE

base_encoding = "gbk"
MAX_BUFFER_SIZE = 512 * 1024 * 1024


def loadDll(dll_url):
    path = Path(dll_url).resolve()
    if sys.platform != "win32" or ctypes.sizeof(ctypes.c_void_p) != 8:
        raise RuntimeError("CIMG decoding requires Windows x64 Python")
    if not path.is_file():
        raise FileNotFoundError(path)
    # Retain the directory handle with the library so lazy dependencies can resolve.
    directory = os.add_dll_directory(str(path.parent))
    try:
        library = ctypes.CDLL(str(path), winmode=0x00001100)
        function = library.ReadCimgData
        function.argtypes = [ctypes.c_char_p, ctypes.c_void_p]
        function.restype = None  # The legacy wrapper does not consume a return value.
        library._bkjc_dll_directory = directory
        return library
    except Exception:
        directory.close()
        raise


class OldCimgRead:
    def __init__(self, index, *, filename=None):
        self.path = Path(DLL_PATH) / (filename or f"OldCimgRead{index}.dll")
        self.lock = threading.Lock()
        self.dll = None

    def ReadCimgData(self, from_cimg_fileName, buff):
        with self.lock:
            if self.dll is None:
                self.dll = loadDll(self.path)
            self.dll.ReadCimgData(from_cimg_fileName, buff)

    def ReadCimgDataToBuff(self, buff, from_cimg_fileName):
        self.ReadCimgData(_encoded_path(from_cimg_fileName), buff)

    def locked(self):
        return self.lock.locked()


# Readers are lightweight until first use. Each numbered legacy DLL gets a lock.
oldCimgDllList = [OldCimgRead(index) for index in range(POOL_SIZE)]
CimgReadDll = OldCimgRead(0, filename="CimgRead.dll")
_selection_lock = threading.Lock()
_next_index = 0


def getOldCimgDll():
    global _next_index
    with _selection_lock:
        if not oldCimgDllList:
            raise RuntimeError("No legacy CIMG decoder configured")
        reader = oldCimgDllList[_next_index % len(oldCimgDllList)]
        _next_index += 1
        return reader  # A busy reader blocks on its lock; never recursively spins.


def _encoded_path(filename):
    filename = os.fsdecode(os.fspath(filename))
    if "\0" in filename:
        raise ValueError("NUL is not allowed in a CIMG path")
    if not Path(filename).is_file():
        raise FileNotFoundError(filename)
    return filename.replace("\\", "/").encode(base_encoding)


def _valid_size(size):
    if isinstance(size, bool) or not isinstance(size, int) or not 0 < size <= MAX_BUFFER_SIZE:
        raise ValueError("Invalid CIMG buffer size")
    return size


def ReadCimgDataToBuff(buff, from_cimg_fileName, systemVersion=0):
    if systemVersion not in (0, 1):
        raise ValueError("systemVersion must be 0 (legacy) or 1 (modern)")
    if not isinstance(buff, ctypes.Array):
        raise TypeError("A sized ctypes buffer is required")
    _valid_size(ctypes.sizeof(buff))
    encoded = _encoded_path(from_cimg_fileName)
    reader = CimgReadDll if systemVersion == 1 else getOldCimgDll()
    reader.ReadCimgData(encoded, buff)


def ReadCimgData(from_cimg_fileName, size=HEIGHT * WIDTH, systemVersion=0):
    buff = ctypes.create_string_buffer(_valid_size(size))
    ReadCimgDataToBuff(buff, from_cimg_fileName, systemVersion=systemVersion)
    return buff


def ReadCimgToNumpyArray(from_cimg_fileName, width=WIDTH, height=HEIGHT, systemVersion=0):
    _valid_size(width)
    _valid_size(height)
    buff = ReadCimgData(from_cimg_fileName, _valid_size(width * height), systemVersion)
    return np.frombuffer(buff, np.uint8).reshape(height, width).copy()


def ReadCimgToImage(from_cimg_fileName, width=WIDTH, height=HEIGHT, systemVersion=0):
    return Image.fromarray(ReadCimgToNumpyArray(from_cimg_fileName, width, height, systemVersion))
