import os
import glob
import shutil
from os.path import *


def organize_images(inFolder, startFile, outFoldr):
    """
    Organizes images in a folder based on their creation time.
    Args:
        inFolder (str): Path to the input folder containing the images.
        startFile (str): Name of the file to start organizing from.
        outFoldr (str): Path to the output folder where the organized images will be saved.
    Returns:
        None
    """
    outIndex = 0
    allFile = glob.glob(join(inFolder, "*.jpg"))
    allFile = allFile[allFile.index(startFile):]
    currentFolder = ""
    oldTime = 0
    for f_ in allFile:
        cTime = os.path.getctime(f_)
        if cTime - oldTime > 1000 * 10:
            currentFolder = join(outFoldr, str(outIndex), "1")
            os.makedirs(currentFolder, exist_ok=True)
            outIndex += 1
        oldTime = cTime
        shutil.copy(f_, currentFolder)
