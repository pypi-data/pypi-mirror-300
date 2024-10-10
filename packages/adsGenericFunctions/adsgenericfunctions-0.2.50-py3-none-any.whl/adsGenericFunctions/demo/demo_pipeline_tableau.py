from adsGenericFunctions.logger import Logger
from adsGenericFunctions.dbPgsql import dbPgsql
from adsGenericFunctions.global_config import set_timer
from adsGenericFunctions.pipeline import pipeline

from to_sort.env import *
import logging

logger_connection = dbPgsql({'database': pg_dwh_db
                          , 'user': pg_dwh_user
                          , 'password': pg_dwh_pwd
                          , 'port': pg_dwh_port
                          , 'host': pg_dwh_host},
                      None)
logger_connection.connect()
logger = Logger(logger_connection, logging.INFO, "AdsLogger", "LOGS", "LOGS_details")
logger.info("Début de la démonstration...")
set_timer(True)
logger.disable()

# Déclarons une source base de données, mais cette fois ce sera un tableau
source = [
    ('ADS', 120.5, 'Mo', 'test1'),
    ('ADS', 130.7, 'Mo', 'test2'),
    ('ADS', 15.5, 'Mo', 'test3'),
    ('ADS', 100.0, 'Mo', 'test4')
]
destination = dbPgsql({'database':pg_dwh_db
                    , 'user':pg_dwh_user
                    , 'password':pg_dwh_pwd
                    , 'port':pg_dwh_port
                    , 'host':pg_dwh_host}, logger)

# Créons la table de réception de nos données
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
logger.enable()

# Premier pipeline
pipeline_1 = pipeline({
    'tableau': source, # Le tableau qui sert de source
    'db_destination': destination, # La destination du pipeline
    'table': 'demo_pipeline', # La table de destination
    'cols': ['tenantname', 'taille', 'unite', 'fichier'] # Les colonnes où nous allons insérer
}, logger)

rejects = pipeline_1.run()
print(f"Rejets : {rejects}")

# Comme pour l'autre démo, un batch_size plus grand implique un traitement plus rapide
# Second pipeline
pipeline_2 = pipeline({
    'tableau': source, # Le tableau qui sert de source
    'db_destination': destination, # La destination du pipeline
    'table': 'demo_pipeline', # La table de destination
    'cols': ['tenantname', 'taille', 'unite', 'fichier'], # Les colonnes où nous allons insérer
    'batch_size': 50
}, logger)

rejects = pipeline_2.run()
print(f"Rejets : {rejects}")

# Voyons les rejets justement, redefinissons une source qui générera une erreur
source = [
    ('ADS', 120.5, 'Mo', 'test1'),
    ('ADS', 130.7, 'Mo', 'test2'),
    ('ADS', "Cela va créer une erreur", 'Mo', 'test3'),
    ('ADS', 100.0, 'Mo', 'test4')
]

# Premier pipeline, avec un batch_size de 1, seules les lignes qui posent problème ne seront pas insérées et
# seront dans rejets, les autres seront bien insérées
pipeline_1 = pipeline({
    'tableau': source, # Le tableau qui sert de source
    'db_destination': destination, # La destination du pipeline
    'table': 'demo_pipeline', # La table de destination
    'cols': ['tenantname', 'taille', 'unite', 'fichier'] # Les colonnes où nous allons insérer
}, logger)

rejects = pipeline_1.run()
print(f"Rejets : {rejects}")

# Avec un batch_size plus grand, c'est le batch entier qui ne sera pas inséré et mis dans les rejets
# Second pipeline
pipeline_2 = pipeline({
    'tableau': source, # Le tableau qui sert de source
    'db_destination': destination, # La destination du pipeline
    'table': 'demo_pipeline', # La table de destination
    'cols': ['tenantname', 'taille', 'unite', 'fichier'], # Les colonnes où nous allons insérer
    'batch_size': 2
}, logger)

rejects = pipeline_2.run()
print(f"Rejets : {rejects}")

logger.info("Fin de la démonstration")