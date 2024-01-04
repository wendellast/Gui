import logging

# Config logging
logging.basicConfig(filename="config/log/error.log", level=logging.ERROR)


def logging_error(error):
    logging.error(f"""Erro na sua_funcao: {error} """, exc_info=True)
