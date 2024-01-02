import os

import dotenv
from hugchat import hugchat
from hugchat.login import Login

from api.brain import prompt4conversation

dotenv.load_dotenv(dotenv.find_dotenv())

# Get email and passoword
email = os.getenv("email")
password = os.getenv("password")

# Log in to huggingface and grant authorization to huggingchat
sign = Login(email, password)
cookies = sign.login()

# Save cookies to the local directory
cookie_path_dir = "./cookies_snapshot"
sign.saveCookiesToDir(cookie_path_dir)

# Create a ChatBot
chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
temperature = 0.1
top_p = min_value = 0.1
repetition_penalty = 1.0
top_k = 1
max_new_tokens = min_value = 1


def generate_response(prompt):
    final_prompt = ""
    make_better = True
    source = ""

    context = {""}

    final_prompt = prompt4conversation(prompt, context)

    if make_better:
        #        print(final_prompt)
        response = chatbot.chat(
            final_prompt,
            temperature=temperature,
            top_p=top_p,
            repetition_penalty=repetition_penalty,
            top_k=top_k,
            max_new_tokens=max_new_tokens,
        )
        response += source
    else:
        print(final_prompt)
        response = final_prompt

    return response


def response_gui(input_text):
    response = generate_response(input_text)
    return response
