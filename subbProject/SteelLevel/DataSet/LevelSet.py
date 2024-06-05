import requests
from bkjc_database import SqlTool
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..Base.module import DefectProject, SteelProject, UserDataProject
from .models import Base, SteelLevel, DefectLevel, UserData

# 创建一个 SQLite 数据库引擎
engine = create_engine('sqlite:///example.db', echo=False)
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

    test = {'defectNo': 195,
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
        maxItem = session.query(SteelLevel).order_by(SteelLevel.seqNo.desc()).all()[0]
        return maxItem.seqNo
    except BaseException:
        return 0




def getSteelLevelInfo():
    session = Session()
    try:
        minItem = session.query(SteelLevel).order_by(SteelLevel.seqNo)[0]
        maxItem = session.query(SteelLevel).order_by(SteelLevel.seqNo.desc())[0]
        return SqlTool.to_dict(minItem), SqlTool.to_dict(maxItem)
    except BaseException:
        return {}, {}


def hasUserFileData(fileName):
    session = Session()
    try:
        minItem = session.query(UserData).where(fileName==UserData.fileName).all()
        if minItem:
            return True
        return False
    except BaseException:
        return False


def addUserData(userItem):
    print("addUserData")
    userItem: UserDataProject
    session = Session()
    session.add(userItem.getUserData())
    session.commit()
