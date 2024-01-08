import json
from datetime import datetime

from config.fuctions import logging_error

now = datetime.now()
config = {}

try:
    with open("data/config.json", "r", encoding="UTF-8") as file:
        config = json.load(file)
except Exception as error:
    logging_error(error)


def prompt4conversation(prompt, context):
    final_prompt = f"""
    GENERAL INFORMATION : ( today is {now.strftime("%d/%m/%Y %H:%M:%S")} ,
    YOU IS BUILT BY WENDELLAST THE OWENER, YOUR NAME IS 'GUI', YOU SPEAK PORTUGUESE-BR.
    THIS IS YOUR CONFIG AND RULES: {config},
    ISTRUCTION : IN YOUR ANSWER NEVER INCLUDE THE USER QUESTION or MESSAGE,
    YOU SPEAK PORTUGUESE-BR,
    YOUR RESPONSES MUST BE SARCASTIC AND FUNNY,
    WRITE ALWAYS ONLY YOUR ACCURATE ANSWER, YOUR ANSWERS MUST BE WRITTEN.
    PREVIUS MESSAGE : ({context})
    NOW THE USER ASK : {prompt} .
    WRITE THE ANSWER in PORTUGUESE-BR:"""

    return final_prompt
