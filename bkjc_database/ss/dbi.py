from sqlalchemy import or_, and_

from bkjc_database import SqlTool

from bkjc_database.NerCarDataBase.sqlserver import ClientDefectDB, SteelRecord, ConfigCenter
from bkjc_database.property.DataBaseInterFace import DataBaseInterFace


class SqlServer_3d0(DataBaseInterFace):
    """
    A class representing a SQL Server database property.

    This class provides methods to interact with a SQL Server database and retrieve steel records.

    Attributes:
        None

    Methods:
        isSqlServer(): Checks if the database is SQL Server.
        getSteelByNum(number, defectOnly, startID=None): Retrieves steel records by number.
        getSteelById(steelId): Retrieves steel records by ID.
        getSteelBySeqNo(seqNo): Retrieves steel records by sequence number.
        getSteelBySteelNo(steelNo): Retrieves steel records by steel number.
        getSteelByDate(fromDate, toDate): Retrieves steel records by date range.
        getDefectBySeqNo(seqNo): Retrieves defect information by sequence number.
        getDefectClass(): Retrieves defect classes.
        getCameraList(): Retrieves the list of cameras.
        getDefectItem(cameraId, defectId): Retrieves defect items.
        getGradeInfo(seqNo): Retrieves grade information.
        getSeqIdBySteelNo(steelNo, index=-1): Retrieves the sequence ID of a steel record based on the steel number.
        getSteelInfo(steelNo): Retrieves the information of a steel record based on the steel number.
    """
    def isSqlServer(self):
        return True

    def getSteelByNum(self, number, defectOnly=False, startID=None, desc = True):
        """
        Retrieve a specified number of steel records.

        Args:
            number (int): The number of steel records to retrieve.
            defectOnly (bool): Flag indicating whether to retrieve only records with defects.
            startID (int, optional): The starting ID for filtering the records. Defaults to None.
            ord_item (bool, optional): Flag indicating whether to order the records in descending order. Defaults to True.
        Returns:
            list: A list of steel records, each represented as a list containing the steel object and its ID.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        with SteelRecord.Session() as session:
            try:
                que = session.query(SteelRecord.Steel, SteelRecord.SteelID).join(
                    SteelRecord.SteelID, SteelRecord.SteelID.ID == SteelRecord.Steel.SteelID, isouter=True
                )
                if startID:
                    que = que.filter(SteelRecord.Steel.ID > startID)

                if desc:
                    ord_item = SteelRecord.Steel.ID.desc()
                else:
                    ord_item = SteelRecord.Steel.ID.asc()

                if not defectOnly:
                    # res = [[i_, j_] for i_, j_ in que.order_by(ord_item)[0:number]]
                    res = [[i_, j_] for i_, j_ in que.order_by(ord_item)[0:number]][::-1]
                else:
                    # res = [[i_, j_] for i_, j_ in que.filter(
                    #     or_(SteelRecord.Steel.TopDefectNum > 0, SteelRecord.Steel.BottomDefectNum > 0)
                    # ).order_by(ord_item)[0:number]]
                    res = [[i_, j_] for i_, j_ in que.filter(
                        or_(SteelRecord.Steel.TopDefectNum > 0, SteelRecord.Steel.BottomDefectNum > 0)
                    ).order_by(ord_item)[0:number]][::-1]
                return res[::-1]
            except:
                session.rollback()
                raise

    def getSteelById(self, steelId):
            """
            Retrieves steel records by the given steel ID.

            Args:
                steelId (int): The ID of the steel.

            Returns:
                list: A list of steel records, each represented as a list containing two elements:
                      - The steel record object
                      - The steel ID object

            Raises:
                Exception: If an error occurs during the retrieval process.
            """
            with SteelRecord.Session() as session:
                try:
                    que = session.query(SteelRecord.Steel,
                                        SteelRecord.SteelID).join(SteelRecord.SteelID,
                                                                  SteelRecord.SteelID.ID == SteelRecord.Steel.SteelID,
                                                                  isouter=True)
                    que = que.filter(steelId == SteelRecord.Steel.ID)
                    return [[i_, j_] for i_, j_ in que.order_by(
                        SteelRecord.Steel.ID.desc())[0:10]]
                except:
                    session.rollback()
                    raise

    def getSteelBySeqNo(self, seqNo):
        """
        Retrieve steel records by sequence number.

        Args:
            seqNo (int): The sequence number to filter the records.

        Returns:
            list: A list of steel records and their corresponding IDs.

        Raises:
            Exception: If an error occurs during the database operation.
        """
        with SteelRecord.Session() as session:
            try:
                que = session.query(SteelRecord.Steel,
                                    SteelRecord.SteelID).join(SteelRecord.SteelID,
                                                              SteelRecord.SteelID.ID == SteelRecord.Steel.SteelID,
                                                              isouter=True)
                que = que.filter(seqNo == SteelRecord.Steel.SequeceNo)
                return [[i_, j_] for i_, j_ in que.order_by(
                    SteelRecord.Steel.ID.desc())[0:500]]
            except:
                session.rollback()
                raise

    def getSteelBySteelNo(self, steelNo):
        """
        Retrieves steel records based on the given steel number.

        Args:
            steelNo (str): The steel number to search for.

        Returns:
            list: A list of steel records matching the given steel number.
        """
        with SteelRecord.Session() as session:
            try:
                que = session.query(SteelRecord.Steel,
                                    SteelRecord.SteelID).join(SteelRecord.SteelID,
                                                              SteelRecord.SteelID.ID == SteelRecord.Steel.SteelID,
                                                              isouter=True)
                que = que.filter(SteelRecord.Steel.SteelID.like(f"%{steelNo}%"))
                return [[i_, j_] for i_, j_ in que.order_by(
                    SteelRecord.Steel.ID.desc())[0:500]]
            except:
                session.rollback()
                raise

    def getSteelByDate(self, fromDate, toDate):
        """
        Retrieves a list of steel records within the specified date range.

        Args:
            fromDate (datetime): The start date of the range.
            toDate (datetime): The end date of the range.

        Returns:
            list: A list of steel records.

        Raises:
            Exception: If an error occurs during the retrieval process.
        """
        with SteelRecord.Session() as session:
            try:
                que = session.query(SteelRecord.Steel,
                                                SteelRecord.SteelID).join(SteelRecord.SteelID,
                                                                          SteelRecord.SteelID.ID == SteelRecord.Steel.SteelID,
                                                                          isouter=True)
                que = que.filter(
                    and_(SteelRecord.Steel.TopDetectTime >= fromDate, SteelRecord.Steel.TopDetectTime <= toDate))
                llist = [[i_, j_] for i_, j_ in que.order_by(
                    SteelRecord.Steel.ID.desc())[0:500]]
                return llist
            except:
                session.rollback()
                raise

    def getDefectBySeqNo(self, seqNo):
        """
        Retrieves defect information based on the given sequence number.

        Args:
            seqNo (int): The sequence number of the defect.

        Returns:
            dict: A dictionary containing defect information, including counts and camera lists.
        """
        reInfo = {"upCount": 0, "downCount": 0, "upCameraList": ConfigCenter.upCameraIdList,
                  "downCameraList": ConfigCenter.underCameraIdList}
        for index, clientDefect in enumerate(ClientDefectDB.allCamera):
            with clientDefect.Session() as session:
                try:
                    reInfo[index + 1] = {}
                    reInfo[index + 1]["defect"] = session.query(ClientDefectDB.Defect).filter(
                        ClientDefectDB.Defect.SteelNo == seqNo).all()
                    reInfo[index + 1]["count"] = len(reInfo[index + 1]["defect"])
                    reInfo[index + 1]["is_up"] = clientDefect.is_up
                    if reInfo[index + 1]["is_up"]:
                        reInfo["upCount"] += reInfo[index + 1]["count"]
                    else:
                        reInfo["downCount"] += reInfo[index + 1]["count"]
                except:
                    session.rollback()
                    raise
        return reInfo

    def getDefectClass(self):
        with ConfigCenter.Session() as session:
            try:
                defectClass = session.query(ConfigCenter.DefectClass).all()
                return defectClass
            except:
                session.rollback()

    def getCameraList(self):
        return [ConfigCenter.upCameraIdList, ConfigCenter.underCameraIdList]

    def getDefectItem(self,cameraId,defectId):
        with ConfigCenter.Session() as session:
            try:
                item = session.query(ConfigCenter.DefectClass).all()
                return item
            except:
                session.rollback()

    def getGradeInfo(self,seqNo):
        gi = SteelRecord.getGradeInfoBy(seqNo)
        if gi:
            gi.SteelUse = gi.SteelUse.encode("latin-1").decode("GBK", "ignore")
            gi.Quality = gi.Quality.encode("latin-1").decode("GBK", "ignore")
        return gi

    def getSeqIdBySteelNo(self,steelNo:str, index=-1):
        """
        Retrieves the sequence ID of a steel record based on the steel number.

        Args:
            steelNo (str): The steel number to search for.
            index (int, optional): The index of the steel record to retrieve. Defaults to -1, which retrieves the last record.

        Returns:
            int or None: The sequence ID of the steel record if found, None otherwise.
        """
        with SteelRecord.Session() as session:
            try:
                steel = session.query(SteelRecord.Steel).filter(
                    SteelRecord.Steel.SteelID.like("%{}%".format(steelNo))).all()
                if steel:
                    if len(steel) > 1:
                        print(" ID {} 不唯一".format(steelNo))
                    steel = steel[index]
                    return steel.SequeceNo
                print("{} 无记录".format(steelNo))
                return None
            except:
                session.rollback()

    def getSteelInfo(self,steelNo):
        """
        Retrieves the information of a steel record based on the steel number.

        Args:
            steelNo (str): The steel number to search for.

        Returns:
            list: A list of dictionaries representing the steel records.
        """
        steels = SteelRecord.getSteelBySteelId(steelNo)
        return [SqlTool.to_dict(st) for st in steels]
