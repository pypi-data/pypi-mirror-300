from .timer import timer
from .logger import Logger

class pipeline:
    def __init__(self, dictionnary : dict, logger: Logger):
        self.logger = logger
        self.__db_source=dictionnary['db_source']
        self.__query_source=dictionnary['query_source']
        self.__db_destination=dictionnary['db_destination']
        self.__table=dictionnary['table']
        self.__cols=dictionnary['cols']

    @timer
    def run(self):
        res = []
        self.logger.disable_logging()
        self.__db_source.connect()
        self.__db_destination.connect()
        self.logger.enable_logging()
        self.logger.info(f"Connexions établies avec les bases de données.")
        data = list(self.__db_source.sqlQuery(self.__query_source))
        self.logger.info(f"{len(data)} récupérées depuis la source.")
        for row in data:
            result = self.__db_destination.insert(table=self.__table, cols=self.__cols, rows=row)
            if result[0] == "ERROR":
                res.append(result)
        return res

class pipelineBulk:
    def __init__(self, dictionnary : dict, logger: Logger):
        self.logger = logger
        self.__db_source=dictionnary['db_source']
        self.__query_source=dictionnary['query_source']
        self.__db_destination=dictionnary['db_destination']
        self.__table=dictionnary['table']
        self.__cols=dictionnary['cols']

    @timer
    def run(self):
        try:
            self.logger.disable_logging()
            self.__db_source.connect()
            self.__db_destination.connect()
            self.logger.enable_logging()
            self.logger.info(f"Connexions établies avec les bases de données.")
            data=[]
            [data.append(element) for element in self.__db_source.sqlQuery(self.__query_source)]
            self.__db_destination.insertBulk(table=self.__table, cols=self.__cols,rows=data)

        except Exception as e:
            self.logger.enable_logging()
            self.logger.error(f"Échecs des connexions aux bases de données : {e}")
            raise

class pipelineTableau:
    def __init__(self, dictionnary : dict, logger: Logger):
        self.logger = logger
        self.__tableau = dictionnary['tableau']
        self.__db_destination = dictionnary['db_destination']
        self.__table = dictionnary['table']
        self.__cols = dictionnary['cols']

    @timer
    def run(self):
        res = []
        try:
            self.__db_destination.connect()
        except Exception as e:
            raise
        for row in self.__tableau:
            result = self.__db_destination.insert(table=self.__table, cols=self.__cols, rows=row)
            if result[0] == "ERROR":
                res.append(result)
        return res

class pipelineTableauBulk:
    def __init__(self, dictionnary : dict, logger: Logger):
        self.logger = logger
        self.__tableau=dictionnary['tableau']
        self.__db_destination=dictionnary['db_destination']
        self.__table=dictionnary['table']
        self.__cols=dictionnary['cols']

    @timer
    def run(self):
        try:
            self.__db_destination.connect()
            data = [list(row) for row in self.__tableau]
            self.__db_destination.insertBulk(table=self.__table, cols=self.__cols,rows=data)
        except Exception:
            raise