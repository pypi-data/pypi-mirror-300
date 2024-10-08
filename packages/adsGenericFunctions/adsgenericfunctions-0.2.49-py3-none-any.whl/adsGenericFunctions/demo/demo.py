from adsGenericFunctions.logger import Logger

from to_sort.env import *
import logging
import psycopg2

# On établit une connexion pour le logger pour qu'il puisse écrire en base
logger_connection = psycopg2.connect(database=pg_dwh_db, user=pg_dwh_user, password=pg_dwh_pwd, port=pg_dwh_port,
                                     host=pg_dwh_host)
logger = Logger(logger_connection, logging.DEBUG, "AdsLogger", "LOGS", "LOGS_details")
logger.info("Début de la démonstration...")
logger.error("ERREUR")
logger.warning("WARNING")
logger.debug("DEBUG")