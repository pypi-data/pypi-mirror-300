from adsGenericFunctions.logger import Logger
from adsGenericFunctions.dbPgsql import dbPgsql
from adsGenericFunctions.global_config import set_timer
from adsGenericFunctions.pipeline import pipelineTableau, pipelineTableauBulk

from to_sort.env import *
import logging
import psycopg2

# On établit une connexion pour le logger pour qu'il puisse écrire en base
logger_connection = psycopg2.connect(database=pg_dwh_db, user=pg_dwh_user, password=pg_dwh_pwd, port=pg_dwh_port,
                                     host=pg_dwh_host)
logger = Logger(logger_connection, logging.INFO, "AdsLogger", "LOGS", "LOGS_details")
logger.info("Début de la démonstration...")
logger.disable_logging()

# On active le timer, les requêtes seront chronométrées
set_timer(True)
destination = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger)
destination.connect()
destination.sqlExec(''' DROP TABLE IF EXISTS demo_pipeline; ''')
destination.sqlExec('''
CREATE TABLE IF NOT EXISTS demo_pipeline (
    id SERIAL PRIMARY KEY,
    tenantname VARCHAR(255),
    taille FLOAT(8),
    unite VARCHAR(10),
    fichier VARCHAR(255)
);
''')

query = '''
SELECT tenantname, taille, unite, fichier
FROM onyx_qs."diskcheck" LIMIT 10
'''

logger.enable_logging()

logger.info("Et si la source est un tableau ?")
source = [
    ('ADS', 120.5, 'Mo', 'test1'),
    ('ADS', 130.7, 'Mo', 'test2'),
    ('ADS', "OUI", 'Mo', 'test3'),
    ('ADS', 100.0, 'Mo', 'test4')
]

# Attention si on passe une liste de lignes à insérer à un pipelineTableau simple, elles seront insérées une par
# une, loguée une par une et timée une par une, mais on garde les rejets
pipeline = pipelineTableau({'tableau': source, 'db_destination': destination, 'table': 'demo_pipeline',
                 'cols': ['tenantname', 'taille', 'unite', 'fichier']}, logger)
rejects = pipeline.run()
print(rejects)

logger.info("Fin de la démonstration")