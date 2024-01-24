#  encoding=utf-8
"""
操作数据库的核心功能模块
相机缺陷数据库结合
"""
from collections import defaultdict
from typing import List
import logging

from . import ConfigCenter, master
from bkjc_database.NerCarDataBase.BaseImport import *
from .models.ClientDefectDB1 import *
from ..SqlBase import init

baseDB_name = "ClientDefectDB"

engine: Engine
Base: automap_base
Session: sessionmaker
session: Session
inspector: Inspector
table_names: list


class ClientDefectDB:
    """
    相机数据库存在N个，无法使用传统的自动映射
    某个相机数据库将会实例该类
    """

    def __init__(self, DataBaseName: str, is_up: False):
        self.DataBaseName: str = DataBaseName
        self.engine:Engine
        self.session:sessionmaker
        self.engine, self.Base, self.Session, self.session, self.inspector = init(DataBaseName)
        self.is_up = is_up

    def __repr__(self):
        """
        命名输出
        """
        return self.DataBaseName + self.__module__ + hex(id(self))


__CameraDict__ = {}
upCamera: List[ClientDefectDB] = []  # 上表相机数据库
underCamera: List[ClientDefectDB] = []  # 下表相机数据库
allCamera: List[ClientDefectDB]


def dbInit():
    # global engine, Base, Session, session, inspector, table_names
    # engine, Base, Session, session, inspector = init(baseDB_name+"0")
    # table_names = inspector.get_table_names()
    global allCamera
    for index in ConfigCenter.upCameraIdList:
        DB_name = baseDB_name + str(index)
        if DB_name not in master.database_names:
            logging.error("{} 缺陷数据库未定义，请检查数据库是否配置正确".format(DB_name))
        else:
            __CameraDict__[index] = ClientDefectDB(DB_name, True)
            upCamera.append(__CameraDict__[index])
    for index in ConfigCenter.underCameraIdList:
        DB_name = baseDB_name + str(index)
        if DB_name not in master.database_names:
            logging.error("{} 缺陷数据库未定义，请检查数据库是否配置正确".format(DB_name))
        else:
            __CameraDict__[index] = ClientDefectDB(DB_name, False)
            underCamera.append(__CameraDict__[index])
    allCamera = upCamera + underCamera


def activateCamera(camera):
    """
    激活 对应的数据库
    """
    if isinstance(camera, int):
        if camera not in __CameraDict__:
            logging.error("无法激活 {}".format(baseDB_name + str(camera)))
            return False
        return activateCamera(__CameraDict__[camera])
    global engine, Base, Session, session, inspector
    engine, Base, Session, session, inspector = camera.engine, camera.Base, camera.Session, camera.session, camera.inspector
    return True


def getDefectBySequeceNo(steel_ID):
    """获取所有的 Steel 列 """
    return getUpDefectBySequeceNo(steel_ID) + getUnderDefectBySequeceNo(steel_ID)


def getUpDefectBySequeceNo(steel_ID) -> List[Defect]:
    """
    获取上表 缺陷
    """
    re_data = []
    [re_data.extend(ds) for ds in
     [cameraDb.session.query(Defect).filter(Defect.SteelNo == steel_ID) for cameraDb in upCamera]]
    return re_data


def getUpDefectCountBySequeceNo(SequeceNo=None) -> int:
    """
    根据 steel_ID 获取缺陷 总数
    """
    if None is SequeceNo:
        return sum([cameraDb.session.query(func.max(Defect.ID)).scalar() for cameraDb in upCamera])
        # sum([cameraDb.session.query(Defect).count() for cameraDb in upCamera])
    return sum([cameraDb.session.query(Defect).filter(Defect.SteelNo == SequeceNo).count() for cameraDb in upCamera])


def getUnderDefectCountBySequeceNo(SequeceNo=None) -> int:
    """
    根据 steel_ID 获取 下表 缺陷 总数
    """
    if None is SequeceNo:
        return sum([cameraDb.session.query(func.max(Defect.ID)).scalar() for cameraDb in underCamera])
        #  return sum([cameraDb.session.query(Defect).count() for cameraDb in underCamera])
    return sum([cameraDb.session.query(Defect).filter(Defect.SteelNo == SequeceNo).count() for cameraDb in underCamera])


def getDefectCountBySequeceNo(SequeceNo=None) -> int:
    """
    根据 SequeceNo 下表 缺陷 总数
    """
    return getUpDefectCountBySequeceNo(SequeceNo) + getUnderDefectCountBySequeceNo(SequeceNo)


def getUnderDefectBySequeceNo(SequeceNo) -> List[Defect]:
    """
    获取下表 缺陷
    """
    re_data = []
    [re_data.extend(ds) for ds in
     [cameraDb.session.query(Defect).filter(Defect.SteelNo == SequeceNo) for cameraDb in underCamera]]
    return re_data


def getDefectInfoBySequeceNo(sequeceNo) -> dict:
    """
    获取 缺陷 JSON 数据
    """
    re_dict = defaultdict(dict)
    re_dict["count"]['sum'] = 0
    re_dict["count"]['info'] = defaultdict(int)
    for i, cameraDb in enumerate(allCamera):
        itemData = [item[0] for item in cameraDb.session.query(Defect.Class).filter(Defect.SteelNo == sequeceNo).all()]
        re_dict[i]["sum"] = len(itemData)
        re_dict["count"]['sum'] += re_dict[i]["sum"]
        re_dict[i]["info"] = {}
        for key in list(set(itemData)):
            it_count = itemData.count(key)
            re_dict[i]["info"][key] = it_count
            re_dict["count"]['info'][key] += it_count
    return re_dict


dbInit()

