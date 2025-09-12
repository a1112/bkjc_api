from abc import ABC, abstractmethod
from sqlalchemy_utils import database_exists, create_database

from bkjc_database.SqlBase import init
from bkjc_database.BaseImport import *
class DataBaseInterFace(ABC):

    @abstractmethod
    def isSqlServer(self):
        ...

    @abstractmethod
    def getSteelByNum(self, number, defectOnly=False, startID=None,desc=True):
        ...

    @abstractmethod
    def getSteelById(self, steelId):
        ...

    @abstractmethod
    def getSteelBySeqNo(self, seqNo):
        ...

    @abstractmethod
    def getSteelBySteelNo(self, steelNo):
        ...

    @abstractmethod
    def getSteelByDate(self, fromDate, toDate):
        ...

    @abstractmethod
    def getDefectBySeqNo(self, seqNo):
        ...

    @abstractmethod
    def getDefectClass(self):
        ...

    @abstractmethod
    def getCameraList(self):
        ...

    @abstractmethod
    def getDefectItem(self, cameraId, defectId):
        ...

    @abstractmethod
    def getGradeInfo(self, seqNo):
        """
        获取分级

        Args:
            seqNo (int): The sequence number of the grade.

        Returns:
            None

        Raises:
            None
        """
        ...


class DbItem:

    def __init__(self,databaseName):
        self.engine: Engine = None
        self.Base: automap_base = None
        self.Session: sessionmaker = None
        self.inspector: Inspector = None
        self.table_names: list = []
        self.databaseName = databaseName
        self.dbInit()

    def dbInit(self):
        self.engine, self.Base, self.Session, self.inspector = init(self.databaseName)

    def createDatabase(self, metadata=None):
        if not metadata:
            metadata = self.Base.metadata
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        metadata.create_all(self.engine)
        self.table_names = self.inspector.get_table_names()
