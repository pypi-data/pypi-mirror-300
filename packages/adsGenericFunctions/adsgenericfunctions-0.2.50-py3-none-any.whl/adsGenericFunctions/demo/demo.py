import psycopg2

from adsGenericFunctions.logger import Logger
from adsGenericFunctions.dbPgsql import dbPgsql

from to_sort.env import *
import logging

# On établit une connexion pour le logger pour qu'il puisse écrire en base

logger_connection = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, None)
logger_connection.connect()
'''
logger_connection = psycopg2.connect(database=pg_dwh_db, user=pg_dwh_user, password=pg_dwh_pwd, port=pg_dwh_port,
                                     host=pg_dwh_host)
'''
logger = Logger(logger_connection, logging.INFO, "AdsLogger", "LOGS", "LOGS_details")
logger.info("Début de la démonstration...")

destination = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger)
destination.connect()

destination.sqlExec(''' DROP TABLE IF EXISTS demo_insert ''')
destination.sqlExec('''
CREATE TABLE IF NOT EXISTS demo_insert (
    id SERIAL PRIMARY KEY,
    tenantname VARCHAR(255),
    fichier VARCHAR(255)
);
''')
logger.info("Table créee avec succès.")
destination.insert('demo_insert', ['tenantname', 'fichier'], ['tenant_example', 'file_example'])

logger.info("Fin de la démonstration.")
