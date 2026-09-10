#  encoding=utf-8
"""
"""
from typing import List
from datetime import datetime

from bkjc_database.SqlBase import init
from bkjc_database.NerCarDataBase.sqlserver.models.SteelRecord import SteelID, Steel, SteelGradeInfo
from bkjc_database.property.DataBaseInterFace import DbItem

databaseName = "SteelRecord"

from bkjc_database.BaseImport import *


class SteelRecord(DbItem):
    def __init__(self):
        super().__init__(databaseName)

    def getSteelID(self,number: int = None, startNo=0) -> List[SteelID]:
        #  获取最新的 SteelID 数据
        with self.Session() as session:
            try:
                if startNo:
                    return session.query(SteelID).filter(SteelID.No > startNo).order_by(SteelID.No.desc())[0:number][::-1]
                if not number:
                    number = 128
                return session.query(SteelID).order_by(SteelID.No.desc())[0:number][::-1]
            except:
                session.rollback()

    def getSteel(self,number: int = None, startNo=None, flushDefectCount=False) -> List[Steel]:
        with self.Session() as session:
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

    def getFirstDateTime(self):
        """
        返回 steel 表 第一条数据的时间
        """
        with self.Session() as session:
            try:
                return session.query(Steel)[0].TopDetectTime
            except:
                session.rollback()

    def getLastDateTime(self):
        """
        返回 steel 表 最新数据的时间
        """
        with self.Session() as session:
            try:
                return session.query(Steel).order_by(Steel.ID.desc())[0].TopDetectTime
            except:
                session.rollback()


    def getSteelCount(self):
        """
        获取 Steel 数量
        """
        with self.Session() as session:
            try:
                return session.query(func.max(Steel.ID)).scalar()
            except:
                session.rollback()


    def getSteelCountByTopDetectTime(self,fromDateTime: datetime, toDateTime: datetime = None, count=False):
        """
        根据日期来统计 钢板生产数量
        """
        return getSteelCountByDetectTime(Steel.TopDetectTime, fromDateTime, toDateTime, count)


    def getSteelCountByBottomDetectTime(self,fromDateTime: datetime, toDateTime: datetime = None, count=False):
        """
        根据日期来统计 钢板生产数量
        """
        return getSteelCountByDetectTime(Steel.BottomDetectTime, fromDateTime, toDateTime, count)

    def getSteelCountByDetectTime(self,field, fromDateTime: datetime, toDateTime: datetime = None, count=False):
        with self.Session() as session:
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
        with self.Session() as session:
            try:
                one_steel = SteelID(ID=ID, Width=Width, Thick=Thick, Length=Length, Used=Used, AddTime=AddTime,
                                    SteelStatus=SteelStatus, SteelType=SteelType)
                session.add(one_steel)
                session.commit()
            except:
                session.rollback()


    def getSteelSeqNoListbySeqNo(self,seqNo: int):
        with self.Session() as session:
            try:
                queryItem = Steel.SequeceNo
                return [i[0] for i in
                        session.query(queryItem).filter(queryItem > seqNo).order_by(queryItem.desc()).all()]
            except:
                session.rollback()



    def getSteelIdBySeqNo(self,seqNo):
        """
        :param seqNo:
        :return:
        """
        with self.Session() as session:
            try:
                queryItem = SteelID.ID
                return session.query(queryItem).filter(SteelID.SequeceNo == seqNo).scalar()
            except:
                session.rollback()

    def getSteelBySteelId(self,steelId) -> List[Steel]:
        with self.Session() as session:
            try:
                return session.query(Steel).filter(Steel.SteelID == steelId).all()
            except:
                session.rollback()


    def getGradeInfoBy(self,seqNo):
        """
        获取分级数据
        """
        with self.Session() as session:
            gradInfo = None
            try:
                gradInfo = session.query(SteelGradeInfo).filter(SteelGradeInfo.SequeceNo == seqNo).all()
            except:
                session.rollback()
            if gradInfo and len(gradInfo) > 0:
                return gradInfo[0]
            return None


Session = SteelRecord().Session
getGradeInfoBy = SteelRecord().getGradeInfoBy
getSteelBySteelId = SteelRecord().getSteelBySteelId
