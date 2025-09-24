import datetime

import requests
# from bkjc_database import SqlTool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from subbProject.SteelLevel.Base.module import DefectProject, SteelProject, UserDataProject
from .models import Base, SteelLevel, DefectLevel, UserData
from. import level_config
# 创建一个 SQLite 数据库引擎



engine = create_engine('mysql+pymysql://root:nercar@127.0.0.1:3306/SteelLevel', echo=False)

def getDateInfo(dateTime):
    """
    将时间戳，datetime，转换成 字典
    :param dateTime:
    :return:
    """
    if isinstance(dateTime, datetime.datetime):
        return {"year": dateTime.year,
                "month": dateTime.month,
                "weekday": dateTime.weekday(),
                "day": dateTime.day,
                "hour": dateTime.hour,
                "minute": dateTime.minute,
                "second": dateTime.second,
                }
    if isinstance(dateTime, (float, int)):
        return getDateInfo(datetime.datetime.fromtimestamp(dateTime))
    if isinstance(dateTime, datetime.timedelta):
        return {"day": dateTime.days,
                "hour": int(dateTime.seconds / 3600),
                "minute": int(dateTime.seconds / 60) % 60,
                "second": dateTime.seconds % 60
                }


def to_dict(obj, up_Data: dict = None):
    """
    转换成可序列化的字典
    """
    if hasattr(obj, "__dict__") and "_sa_instance_state" in obj.__dict__:
        if not up_Data:
            up_Data = {}
        if len(obj.__dict__) <= 1:
            rd = {key: to_dict(getattr(obj, key)) for key in obj.__dir__() if not key.startswith('_')
                  and key not in ["metadata"] and key not in up_Data}
        else:
            rd = {key: to_dict(getattr(obj, key)) for key in obj.__dict__ if
                  key not in ["_sa_instance_state"] and key not in up_Data}
        rd.update(up_Data)
        return rd
    elif isinstance(obj, datetime.datetime):
        return getDateInfo(obj)
    else:
        return obj

# 声明一个基类
# 创建数据库表
Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)


def defectLevel(defectInfo, steelInfo):
    # 进行判级
    pass


def steelLevel(steelInfo, filterDefects):
    pass


def addDefect(defect):
    defect: DefectProject

    test = {
            'defectNo': 195,
            'defectID': 14,
            'bmIndex': 1,
            'seqNo': 519,
            'cameraId': 1,
            'imageIndex': 7,
            'defectX': 7296,
            'defectY': 231,
            'defectWidth': 237,
            'defectHeight': 103,
            'leftInImg': 128,
            'rightInImg': 231,
            'topInImg': 128,
            'bottomInImg': 365,
            'leftInSteel': -1189,
            'rightInSteel': -1158,
            'topInSteel': 1419,
            'bottomInSteel': 1477,

            'rec': [7296, 231, 237, 103],
            'box': [778, 61, 125, 30],
            'boxX': 778, 'boxY': 61,
            'boxW': 125, 'boxH': 30,
            'defectCoefficient': '0 %',
            'grade': 0}
    # defect = test
    session = Session()
    defect: DefectProject
    session.add(
        defect.getDefectLevel()
    )
    session.commit()


def addSteel(steel):
    # 添加 判级 ，钢板信息表
    steel: SteelProject
    session = Session()
    session.add(steel.getSteelLevel())
    session.commit()


def clearAll():
    session = Session()
    session.query(SteelLevel).delete()
    session.query(DefectLevel).delete()
    session.commit()
    session.close()


def getMaxSteelNo():
    session = Session()
    try:
        maxItem = session.query(SteelLevel).order_by(SteelLevel.seqNo.desc())[0]
        return maxItem.seqNo
    except BaseException:
        return 0

def getMaxSteelNoByproductionLine(productionLine):
    with Session() as session:
        try:
            maxItem = session.query(SteelLevel).where(productionLine==SteelLevel.productionLine_classification).order_by(SteelLevel.id.desc())[0]
            print(f"{productionLine} maxItem maxId: {maxItem.id} {maxItem.seqNo}")
            return maxItem.seqNo
        except BaseException:
            return 0



def getSteelLevelInfo():
    with Session() as session:
        try:
            minItem = session.query(SteelLevel).order_by(SteelLevel.seqNo)[0]
            maxItem = session.query(SteelLevel).order_by(SteelLevel.seqNo.desc())[0]
            return to_dict(minItem), to_dict(maxItem)
        except BaseException:
            return {}, {}


def hasUserFileData(fileName):
    with Session() as session:
        try:
            minItem = session.query(UserData).where(fileName==UserData.fileName).all()
            if minItem:
                return True
            return False
        except BaseException:
            return False


def addUserData(userItem):
    userItem: UserDataProject
    with Session() as session:
        session.add(userItem.getUserData())
        session.commit()


def getUserDatByPackageNo(packageNo):

    with Session() as session:
        items = session.query(UserData).where(packageNo==UserData.busNumber).all()
        print(items)
        return items

def getSteelLevelByDate(startDate, endDate, productionLine = None):
    with Session() as session:
        que=session.query(SteelLevel).where(SteelLevel.detectTime>startDate).where(SteelLevel.detectTime<endDate)
        if not productionLine:
            pass
        else:
            que=que.filter(SteelLevel.productionLine_classification == productionLine)
        return que[:10000]

def getAllSteelLevel():
    with Session() as session:
        items = session.query(SteelLevel)
        return items.all()