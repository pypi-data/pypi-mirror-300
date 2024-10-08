from abc import ABC, abstractmethod


class data_factory(ABC):

    @abstractmethod
    def connect(self):
        pass
    @abstractmethod
    def insert(self,table,cols=[],rows=[]):
        pass

    @abstractmethod
    def insertBulk(self,table,cols=[],rows=[]):
        pass
    @abstractmethod
    def sqlQuery(self,query):
        pass

    @abstractmethod
    def exec(self, query: str, params=None):
        pass