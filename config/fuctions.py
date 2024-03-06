import logging
import os

import dotenv

dotenv.load_dotenv(dotenv.find_dotenv())


debug = os.getenv("DEBUG")
language = os.getenv("language")

debug = bool(debug)

# Config logging
logging.basicConfig(filename="config/log/error.log", level=logging.ERROR)


def logging_error(error):
    logging.error(f"""Erro na sua_funcao: {error} """, exc_info=True)

    if debug == True:
        raise (error)
    else:
        return
