import os
import time

def wait_for_file(path, logger, retry=20):
    i=1
    while not os.path.isfile(path) and i<=retry:
        time.sleep(1)
        logger.info("Waiting for file... "+str(i))
        i+=1
    if i>retry:
        logger.error("Aucun fichier trouvé (nombre de tentatives dépassé).")
    else:
        logger.info("Fichier trouvé.")