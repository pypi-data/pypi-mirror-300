from datetime import datetime
import pymssql
from timer import *
from package.logger import Logger
from dataFactory import *

class dbMssql(data_factory):

    def __init__(self, dictionnary: dict, logger: Logger):
        self.logger = logger
        self.__database = dictionnary['database']
        self.__user = dictionnary['user']
        self.__password = dictionnary['password']
        self.__port = dictionnary['port']
        self.__host = dictionnary['host']
        self.__batch_size = 10000

    @timer
    def connect(self):
        try:
            self.connection = pymssql.connect(
                server=f"{self.__host}:{self.__port}",
                user=self.__user,
                password=self.__password,
                database=self.__database
            )
            self.logger.info(f"Connexion établie avec la base de données.")
            return self.connection
        except Exception as e:
            self.logger.error(f"Échec de la connexion à la base de données: {e}")
            raise

    def sqlQuery(self, query):
        self.logger.debug(f"Exécution de la requête de lecture : {query}")
        start_time = datetime.now()
        try:
            timer_start = timeit.default_timer()
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                cols = [desc[0] for desc in cursor.description]
                self.logger.info("Requête exécutée avec succès, début de la lecture des résultats.")
                while True:
                    rows = cursor.fetchmany(self.__batch_size)
                    if not rows:
                        break
                    yield from rows
                    self.logger.info(f"{len(rows)} lignes lues.")
            end_time = datetime.now()
            self.logger.log_to_db(start_time, end_time, status='success', message="Requête de lecture exécutée.")
            if get_timer():
                elapsed_time = timeit.default_timer() - timer_start
                self.logger.info(f"Temps d'exécution de sqlQuery: {elapsed_time:.4f} secondes")
        except Exception as e:
            end_time = datetime.now()
            self.logger.error(f"Échec de la lecture des données: {e}")
            self.logger.log_to_db(start_time, end_time, status="failure", message=str(e))
            raise

    def exec(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
        except Exception as e:
            self.logger.error(f"Échec de l'exécution de la requête: {e}")
            raise

    def insert(self, table, cols=[], rows=[]):
        try:
            with self.connection.cursor() as cursor:
                placeholders = ", ".join(["%s"] * len(cols))
                query = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
                cursor.execute(query, rows)
                self.connection.commit()
                self.logger.info(f"{cursor.rowcount} lignes insérées avec succès dans la table {table}.")
        except Exception as e:
            self.logger.error(f"Échec de l'insertion des données: {e}")
            raise

    def insertBulk(self, table, cols=[], rows=[]):
        try:
            with self.connection.cursor() as cursor:
                placeholders = ", ".join(["%s"] * len(cols))
                query = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
                cursor.executemany(query, rows)
                self.connection.commit()
                self.logger.info(f"{cursor.rowcount} lignes insérées avec succès dans la table {table}.")
        except Exception as e:
            self.logger.error(f"Échec de l'insertion des données: {e}")
            raise