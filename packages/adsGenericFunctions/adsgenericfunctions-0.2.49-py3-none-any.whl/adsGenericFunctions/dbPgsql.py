from datetime import datetime
import psycopg2
import timeit
from .timer import timer, get_timer
from .dataFactory import data_factory
from .logger import Logger


class dbPgsql(data_factory):

    def __init__(self, dictionnary: dict, logger: Logger | None):
        self.connection = None
        self.logger = logger
        self.__database = dictionnary['database']
        self.__user = dictionnary['user']
        self.__password = dictionnary['password']
        self.__port = dictionnary['port']
        self.__host = dictionnary['host']
        self.__batch_size = 10_000

    @timer
    def connect(self):
        self.logger.info("Tentative de connexion avec la base de données")
        try:
            self.connection = psycopg2.connect(
                database=self.__database,
                user=self.__user,
                password=self.__password,
                port=self.__port,
                host=self.__host
            )
            self.logger.info(f"Connexion établie avec la base de données.")
            return self.connection
        except Exception as e:
            self.logger.error(f"Échec de la connexion à la base de données.")
            raise

    def sqlQuery(self, query: str):
        self.logger.debug(f"Exécution de la requête de lecture: {query}")
        start_time = datetime.now()
        try:
            timer_start = timeit.default_timer()
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                cols = [desc for desc in cursor.description]
                self.logger.info("Requête exécutée avec succès, début de la lecture des résultats.")
                while True:
                    rows = cursor.fetchmany(self.__batch_size)
                    if not rows:
                        break
                    yield from rows
                    self.logger.info(f"{len(rows)} ligne(s) lue(s).")
            end_time = datetime.now()
            self.logger.log_to_db(start_time, end_time, status='success', message='Requête de lecture exécutée')
            if get_timer():
                elapsed_time = timeit.default_timer() - timer_start
                self.logger.info(f"Temps d'exécution de sqlQuery: {elapsed_time:.4f} secondes")
        except Exception as e:
            end_time = datetime.now()
            self.logger.error(f"Échec de la lecture des données: {e}")
            self.logger.log_to_db(start_time, end_time, status="failure", message=str(e))
            raise

    @timer
    def sqlExec(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.logger.info(f"Requête exécutée avec succès.")
                self.connection.commit()
        except Exception as e:
            self.logger.error(f"Échec de l'exécution de la requête: {e}")
            raise

    @timer
    def sqlScalaire(self, query):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.logger.info(f"Requête exécutée avec succès.")
                data = cursor.fetchmany()
                if len(data)>1:
                    self.logger.error(f"La requête a retourné plus d'une valeur")
                    raise "La requête a retourné plus d'une valeur"
                else:
                    return data

        except Exception as e:
            self.logger.error(f"Échec de l'exécution de la requête: {e}")


    @timer
    def insertBulk(self, table, cols=[], rows=[]):
        start_time = datetime.now()
        try:
            with self.connection.cursor() as cursor:
                placeholders = ", ".join(["%s"] * len(cols))
                query = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
                cursor.executemany(query, rows)
                self.connection.commit()
                self.logger.info(f"{cursor.rowcount} lignes insérées avec succès dans la table {table}.")
                end_time = datetime.now()
                self.logger.log_to_db(start_time, end_time, status="success", message="Insertion en masse réussie.")
        except Exception as e:
            end_time = datetime.now()
            self.logger.error(f"Échec de l'insertion des données: {e}")
            self.logger.log_to_db(start_time, end_time, status='failure', message=str(e))
            raise

    @timer
    def insert(self, table, cols=[], rows=[]):
        start_time = datetime.now()
        try:
            with self.connection.cursor() as cursor:
                placeholders = ", ".join(["%s"] * len(cols))
                query = f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({placeholders})"
                cursor.execute(query, rows)
                self.connection.commit()
                self.logger.info(f"{cursor.rowcount} ligne insérée avec succès dans la table {table}.")
                end_time = datetime.now()
                self.logger.log_to_db(start_time, end_time, status='success', message="Insertion réussie.")
                return "SUCCESS", rows
        except Exception as e:
            end_time = datetime.now()
            self.logger.error(f"Échec de l'insertion des données: {e}")
            self.logger.log_to_db(start_time, end_time, status='failure', message=str(e))
            self.connection.rollback()
            return "ERROR", str(e), rows

