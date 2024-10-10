from .timer import timer
from .logger import Logger
import polars as pl

class pipeline:
    def __init__(self, dictionnary: dict, logger: Logger):
        self.logger = logger
        self.__db_source = dictionnary.get('db_source')
        self.__query_source = dictionnary.get('query_source')
        self.__tableau = dictionnary.get('tableau')
        self.__db_destination = dictionnary.get('db_destination')
        self.__table = dictionnary.get('table')
        self.__cols = dictionnary.get('cols')
        self.__batch_size = dictionnary.get('batch_size', 1)

    @timer
    def _load_data(self):
        self.logger.info("Chargement des données...")
        self.logger.disable()
        if self.__tableau:
            res = self.__tableau
        elif self.__db_source and self.__query_source:
            self.__db_source.connect()
            data = list(self.__db_source.sqlQuery(self.__query_source))
            res = data
        else:
            raise ValueError("Source de données non supportée")
        return pl.DataFrame(res, schema=self.__cols, orient='row', strict=False)

    @timer
    def run(self):
        res = []
        try:
            df = self._load_data()
            self.__db_destination.connect()
            self.logger.enable()
            self.logger.info("Connexion établies avec les bases de données.")
            self.logger.info(f"{df.shape[0]} lignes récupérées.")
            for start in range(0, df.shape[0], self.__batch_size):
                end = start + self.__batch_size
                batch = df[start:end].rows()
                insert_result = self.__db_destination.insertBulk(
                    table=self.__table,
                    cols=self.__cols,
                    rows=list(batch)
                )
                if insert_result[0] == "ERROR":
                    res.append(batch)
        except Exception as e:
            self.logger.enable()
            self.logger.error(f"Échec de l'exécution du pipeline: {e}")
            raise
        return res
