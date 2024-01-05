import os
import sqlite3

import dotenv

from api.apple import HuggingChat
from api.brain import prompt4conversation
from config.fuctions import logging_error

dotenv.load_dotenv(dotenv.find_dotenv())


import json
from datetime import datetime

now = datetime.now()
context = {}

email = os.getenv("email")
password = os.getenv("password")
cookie_path_dir = "./cookies_snapshot"

with open("data/config.json", "r", encoding="UTF-8") as file:
    config = json.load(file)
# MEMORY
if os.path.exists("memory.db"):
    try:
        conn = sqlite3.connect("memory.db")
        cursor = conn.cursor()

        cursor.execute("SELECT user_ask, gui_response FROM mind")
        dados = cursor.fetchmany(300)

        user_ask = []
        gui_response = []

        for pergunta in dados:
            user_ask.append(pergunta[0])
            gui_response.append(pergunta[1])

        cursor.close()

    except Exception as error:
        logging_error(error)


# Msg history
if os.path.exists("memory.db"):
    context = {"User:": user_ask, "Gui:": gui_response}
    #context = {}


def response_gui(input_text):
    resp = prompt4conversation(input_text, context=context)
    llm = HuggingChat(email=email, psw=password, log=False, use_cache=True, model=0)

    return llm(resp)
