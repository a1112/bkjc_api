from abc import ABC, abstractmethod


class DataBaseInterFace(ABC):

    @abstractmethod
    def isSqlServer(self):
        ...

    @abstractmethod
    def getSteelByNum(self,number, defectOnly, startID=None):
        ...

    @abstractmethod
    def getSteelById(self,steelId):
        ...

    @abstractmethod
    def getSteelBySeqNo(self,seqNo):
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
    def getDefectItem(self,cameraId,defectId):
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
