import os
import time
from package.logger import logger
def waitForFile(path,retry=20):
    i=1
    while not os.path.isfile(path) and i==retry:
        time.sleep(1)
        logger.info("waiting for file ..."+str(i))
        i+=1
    if i==retry:
        logger.error("Aucun fichier trouvé (nombre de tentative dépassé)")
    else:
        logger.info("Fichier trouvé")