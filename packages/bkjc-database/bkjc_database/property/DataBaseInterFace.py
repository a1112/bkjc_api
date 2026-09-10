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
    """A lazily opened database. Schema creation is an explicit operation."""

    def __init__(self, databaseName):
        import threading
        self.engine = self.Base = self.inspector = None
        self._session_factory = None
        self._init_lock = threading.RLock()
        self.table_names = []
        self.databaseName = databaseName

    def _ensure_initialized(self):
        with self._init_lock:
            if self._session_factory is None:
                self.dbInit()

    def dbInit(self):
        self.engine, self.Base, self._session_factory, self.inspector = init(self.databaseName)

    def Session(self, *args, **kwargs):
        self._ensure_initialized()
        return self._session_factory(*args, **kwargs)

    def createDatabase(self, metadata=None):
        self._ensure_initialized()
        if metadata is None:
            metadata = self.Base.metadata
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
        metadata.create_all(self.engine)
        self.table_names = self.inspector.get_table_names()
