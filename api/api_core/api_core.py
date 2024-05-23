from PIL import Image

from bkjc_tools import CimgReadCore
import config
from bkjc_database.dbm import dbm
from api.ImageCache import CimgCache, TimeoutDict
from bkjc_database import SqlTool


def getTestImage():
    """
    Returns a test image.
    """
    return Image.open("test/test.bmp")


cimageCache = CimgCache(1000)


def get_defect_image(cameraId, seqNo, defectId):
    if dbm.isSqlServer():
        return None
    else:
        return config.getDefectImgFile_4d0(cameraId, seqNo, defectId)


def get_cimage(cameraIndex, seqNo, imageIndex) -> Image.Image:
    """
    Retrieves the large image.

    Args:
        cameraIndex (int): The camera index.
        seqNo (int): The sequence number.
        imageIndex (int): The image index.

    Returns:
        PIL.Image: The retrieved image.
    """
    if not dbm.isSqlServer():
        imageIndex += 1
    if cimageCache[cameraIndex, seqNo, imageIndex]:
        return cimageCache[cameraIndex, seqNo, imageIndex]
    if dbm.isSqlServer():
        if config.useLoc:
            img = getTestImage()
        else:
            fileUrl = config.getCimgFile(cameraIndex, seqNo, imageIndex)
            img = Image.fromarray(CimgReadCore.ReadCimgToNumpyArray(fileUrl))
    else:
        fileUrl = config.getImgFile_4d0(cameraIndex, seqNo, imageIndex)
        img = Image.open(fileUrl)
    cimageCache[cameraIndex, seqNo, imageIndex] = img
    return img


def getNumStr(num, size=4):
    """
    Returns a string representation of a number with leading zeros.

    Args:
        num (int): The number to convert.
        size (int): The desired size of the string. Defaults to 4.

    Returns:
        str: The string representation of the number with leading zeros.
    """
    num = str(num)
    return (size - len(num)) * "0" + num


def get_defect_max_cimage(cameraId, seqNo, imageIndex) -> Image.Image:
    """
    Retrieves the large image.

    Args:
        cameraId (int): The camera ID.
        seqNo (int): The sequence number.
        imageIndex (int): The image index.

    Returns:
        PIL.Image: The retrieved image.
    """
    return get_cimage(cameraId, seqNo, imageIndex)


steelInfoCache = TimeoutDict(1000)


def get_steelInfo(steel, steelId):
    """
    Retrieves the steel information.

    Args:
        steel (object): The steel object.
        steelId (object): The steel ID object.

    Returns:
        dict: The steel information.
    """
    if dbm.isSqlServer():
        if steel.SequeceNo in steelInfoCache:
            return steelInfoCache[steel.SequeceNo]
        try:
            info = {
                "id": steel.ID,
                "steelNo": steel.SteelID.strip(),  # Steel plate number
                "steelID": steel.SequeceNo,  # Steel plate ID
                "steelType": steelId.SteelType,  # Steel type
                "steelLength": steelId.Length / 1000 if steelId.Length > 100 else steelId.Length,  # Length in meters
                "steelWidth": steelId.Width / 1000 if steelId.Width > 100 else steelId.Width,  # Width in meters
                "steelThick": steelId.Thick,  # Thickness in mm
                "upDefectNum": steel.TopDefectNum,  # Number of defects on the top surface
                "downDefectNum": steel.BottomDefectNum,  # Number of defects on the bottom surface
                "errorLevel": steel.Grade,  # 0: normal, 1: warning, 2: alarm, 3: severe alarm
                "grade": steel.Grade,
                "detectTime": steel.TopDetectTime.strftime(config.TIMESTAMP_FORMAT),
                "topLen": steel.TopLen,
                "bottomLen": steel.BottomLen,
                # To be supplemented later
            }
        except BaseException as e:
            info = {
                "id": steel.ID,
                "steelNo": steel.SteelID.strip(),  # Steel plate number
                "steelID": steel.SequeceNo,  # Steel plate ID
                "steelType": steel.SteelType,  # Steel type
                "steelLength": steel.TopLen / 1000,  # Length in meters
                "steelWidth": steel.TopWidth / 1000,  # Width in meters
                "steelThick": steel.Thick,  # Thickness in mm
                "upDefectNum": steel.TopDefectNum,  # Number of defects on the top surface
                "downDefectNum": steel.BottomDefectNum,  # Number of defects on the bottom surface
                "errorLevel": steel.Grade,  # 0: normal, 1: warning, 2: alarm, 3: severe alarm
                "grade": steel.Grade,
                "detectTime": steel.TopDetectTime.strftime(config.TIMESTAMP_FORMAT),
                "topLen": steel.TopLen,
                "bottomLen": steel.BottomLen,
                # To be supplemented later
            }
        steelInfoCache[steel.SequeceNo] = info
    else:
        from bkjc_database.NerCarDataBase.mysql.models.ncdplate import Steelrecord
        steel: Steelrecord
        if steel.seqNo in steelInfoCache:
            return steelInfoCache[steel.seqNo]
        try:
            info = {
                "id": steel.id,
                "steelNo": steel.steelID.strip(),  # Steel plate number
                "steelID": steel.seqNo,  # Steel plate ID
                "steelType": steel.steelType,  # Steel type
                "steelLength": steelId.len / 1000,  # Length in meters
                "steelWidth": steelId.width / 1000,  # Width in meters
                "steelThick": steelId.thick / 1000,  # Thickness in mm
                "upDefectNum": steel.defectNum,  # Number of defects on the top surface
                "downDefectNum": steel.defectNum,  # Number of defects on the bottom surface
                "errorLevel": steel.grade,  # 0: normal, 1: warning, 2: alarm, 3: severe alarm
                "grade": 1,
                "detectTime": steel.detectTime.strftime(config.TIMESTAMP_FORMAT),
                "topLen": steel.steelLen,
                "bottomLen": steel.steelLen,
                # To be supplemented later
            }
        except BaseException as e:
            print("addSteelCache error")
            info = {
                "id": steel.id,
                "steelNo": steel.steelID.strip(),  # Steel plate number
                "steelID": steel.seqNo,  # Steel plate ID
                "steelType": steel.steelType,  # Steel type
                "steelLength": steel.steelLen / 1000,  # Length in meters
                "steelWidth": steel.width / 1000,  # Width in meters
                "steelThick": steel.thick / 1000,  # Thickness in mm
                "upDefectNum": steel.defectNum,  # Number of defects on the top surface
                "downDefectNum": steel.defectNum,  # Number of defects on the bottom surface
                "errorLevel": steel.grade,  # 0: normal, 1: warning, 2: alarm, 3: severe alarm
                "grade": 1,
                "detectTime": steel.detectTime.strftime(config.TIMESTAMP_FORMAT),
                "topLen": steel.steelLen,
                "bottomLen": steel.steelLen,
                # To be supplemented later
            }
        steelInfoCache[steel.seqNo] = info
    return info


defectInfoCache = TimeoutDict(10000)


def get_defectInfo(cameraId, defectId):
    """
    Retrieves the defect information.

    Args:
        cameraId (int): The camera ID.
        defectId (int): The defect ID.

    Returns:
        object: The defect information.
    """
    return defectInfoCache[cameraId, defectId]


def set_defectInfo(cameraId, defectId, defectInfo):
    """
    Sets the defect information.

    Args:
        cameraId (int): The camera ID.
        defectId (int): The defect ID.
        defectInfo (object): The defect information.
    """
    defectInfoCache[cameraId, defectId] = defectInfo


def getGradeInfo(seqNo):
    """
    Retrieves the grade information.

    Args:
        seqNo (int): The sequence number.

    Returns:
        dict: The grade information.
    """
    gradeInfo = dbm.getGradeInfo(seqNo)
    if gradeInfo:
        return SqlTool.to_dict(gradeInfo)
    else:
        return {}
