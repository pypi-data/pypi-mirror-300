from package.logger import logger

def writeFile(path, contenu,encoding='utf-8'):
    try:
        logger.info(f"Création du fichier {path}")
        with open(path, 'w', encoding=encoding) as fichier:
            fichier.write(contenu)
        logger.info(f"Contenu écrit avec succès dans {path}")
    except Exception as e:
        logger.error(f"Une erreur s'est produite : {e}")