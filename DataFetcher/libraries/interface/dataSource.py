from abc import ABC, abstractmethod

class dataSource(ABC):

    """
    Fetches the initial data from the source
    """
    @abstractmethod
    def fetchAllData(self):
        pass

    @abstractmethod
    def fetchFile(self, fileId):
        pass
      
