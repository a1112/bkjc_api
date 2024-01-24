#  encoding=utf-8
"""
"""
from typing import List
from datetime import datetime

from bkjc_database.NerCarDataBase.SqlBase import init
from bkjc_database.NerCarDataBase.core import beforeInit
from bkjc_database.NerCarDataBase.sqlserver.models.SteelRecord import SteelID, Steel, SteelGradeInfo

databaseName = "SteelRecord"

from bkjc_database.NerCarDataBase.BaseImport import *

engine: Engine
Base: automap_base
Session: sessionmaker
inspector: Inspector
table_names: list


def dbInit():
    session = None
    global engine, Base, Session, inspector, table_names
    engine, Base, Session, session, inspector = init(databaseName)
    table_names = inspector.get_table_names()


if beforeInit:
    dbInit()


def getSteelID(number: int = None, startNo=0) -> List[SteelID]:
    #  获取最新的 SteelID 数据
    session = Session()
    try:
        if startNo:
            return session.query(SteelID).filter(SteelID.No > startNo).order_by(SteelID.No.desc())[0:number][::-1]
        if not number:
            number = 128
        return session.query(SteelID).order_by(SteelID.No.desc())[0:number][::-1]
    except:
        session.rollback()
    finally:
        session.close()


def getSteel(number: int = None, startNo=None, flushDefectCount=False) -> List[Steel]:
    session = Session()
    try:
        if not number:
            number = 128
        if startNo is not None:
            steels = session.query(Steel).filter(Steel.ID > startNo).order_by(Steel.ID)[0:number]
        else:
            steels = session.query(Steel).order_by(Steel.ID.desc())[0:number][::-1]
        return steels
    except:
        session.rollback()
    finally:
        session.close()


def getFirstDateTime():
    """
    返回 steel 表 第一条数据的时间
    """
    session = Session()
    try:
        return session.query(Steel)[0].TopDetectTime
    except:
        session.rollback()
    finally:
        session.close()


def getLastDateTime():
    """
    返回 steel 表 最新数据的时间
    """
    session = Session()
    try:
        return session.query(Steel).order_by(Steel.ID.desc())[0].TopDetectTime
    except:
        session.rollback()
    finally:
        session.close()


def getSteelCount():
    """
    获取 Steel 数量
    """
    session = Session()
    try:
        return session.query(func.max(Steel.ID)).scalar()
    except:
        session.rollback()
    finally:
        session.close()


def getSteelCountByTopDetectTime(fromDateTime: datetime, toDateTime: datetime = None, count=False):
    """
    根据日期来统计 钢板生产数量
    """
    return getSteelCountByDetectTime(Steel.TopDetectTime, fromDateTime, toDateTime, count)


def getSteelCountByBottomDetectTime(fromDateTime: datetime, toDateTime: datetime = None, count=False):
    """
    根据日期来统计 钢板生产数量
    """
    return getSteelCountByDetectTime(Steel.BottomDetectTime, fromDateTime, toDateTime, count)


def getSteelCountByDetectTime(field, fromDateTime: datetime, toDateTime: datetime = None, count=False):
    session = Session()
    try:
        if count:
            if not toDateTime:
                return session.query(Steel).filter(field >= fromDateTime).count()
            return session.query(Steel).filter(
                and_(field >= fromDateTime, field <= toDateTime)).count()
        else:
            query: Query
            if not toDateTime:
                query = session.query(Steel.SequeceNo).filter(field >= fromDateTime)
            else:
                query = session.query(Steel.SequeceNo).filter(
                    and_(field >= fromDateTime, field <= toDateTime))
            try:
                return query[-1][0] - query[0][0] + 1
            except IndexError:
                return 0
    except:
        session.rollback()
    finally:
        session.close()


def addSteelId(ID, Width=0, Thick=0, Length=0, Used=0, AddTime=datetime.now(), SteelStatus=0, SteelType=None):
    """
    增加一条 SteelId 信息
    id:  钢板 ID
    Width： 宽度
    Thick： 厚度
    Length： 长度
    Used：是否使用
    AddTime： 添加时间
    SteelStatus：的检测状态
    SteelType: 钢种信息
    """
    session = Session()
    try:
        one_steel = SteelID(ID=ID, Width=Width, Thick=Thick, Length=Length, Used=Used, AddTime=AddTime,
                            SteelStatus=SteelStatus, SteelType=SteelType)
        session.add(one_steel)
        session.commit()
    except:
        session.rollback()
    finally:
        session.close()


def getSteelSeqNoListbySeqNo(seqNo: int):
    session = Session()
    try:
        queryItem = Steel.SequeceNo
        return [i[0] for i in
                session.query(queryItem).filter(queryItem > seqNo).order_by(queryItem.desc()).all()]
    except:
        session.rollback()
    finally:
        session.close()


def getSteelIdBySeqNo(seqNo):
    """
    :param seqNo:
    :return:
    """
    session = Session()
    try:
        queryItem = Steel.SteelID
        return session.query(queryItem).filter(Steel.SequeceNo == seqNo).scalar()
    except:
        session.rollback()
    finally:
        session.close()


def getSteelBySteelId(steelId) -> List[Steel]:
    session = Session()
    try:
        return session.query(Steel).filter(Steel.SteelID == steelId).all()
    except:
        session.rollback()
    finally:
        session.close()


def getGradeInfoBy(seqNo):
    """
    获取分级数据
    """
    gradInfo = None
    session = Session()
    try:
        gradInfo = session.query(SteelGradeInfo).filter(SteelGradeInfo.SequeceNo == seqNo).all()
    except:
        session.rollback()
    finally:
        session.close()
    if gradInfo and len(gradInfo) > 0:
        return gradInfo[0]
    return None
