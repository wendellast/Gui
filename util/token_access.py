import os

from dotenv import load_dotenv


def load_token():

    load_dotenv()

    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")

    if token is None:
        raise ValueError("Token não encontrado no arquivo .env")

    return str(token)
