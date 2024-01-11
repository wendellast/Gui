import json
import os
from datetime import datetime

import dotenv

from config.fuctions import logging_error

dotenv.load_dotenv(dotenv.find_dotenv())


now = datetime.now()
config = {}
language = os.getenv("language")

try:
    with open("data/config.json", "r", encoding="UTF-8") as file:
        config = json.load(file)
except Exception as error:
    logging_error(error)


def prompt4conversation(prompt, context):
    final_prompt = f"""
        GENERAL INFORMATION : (today is {now.strftime("%d/%m/%Y %H:%M:%S")} ,
        YOU IS BUILT BY GROUP LAST THE OWENER, YOUR NAME IS 'GUI',
        THIS IS YOUR CONFIG AND RULES: {config},
        ISTRUCTION : IN YOUR ANSWER NEVER INCLUDE THE USER QUESTION or MESSAGE,
        YOUR RESPONSES MUST BE SARCASTIC AND FUNNY,
        WRITE ALWAYS ONLY YOUR ACCURATE ANSWER, YOUR ANSWERS MUST BE WRITTEN.
        PREVIUS MESSAGE : ({context})
        NOW THE USER ASK : {prompt} .
        WRITE THE ANSWER IN {language}:"""

    return final_prompt
