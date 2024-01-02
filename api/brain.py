from datetime import datetime

now = datetime.now()


def prompt4conversation(prompt, context):
    final_prompt = f""" GENERAL INFORMATION : ( today is {now.strftime("%d/%m/%Y %H:%M:%S")} ,
    YOU IS BUILT BY WENDELLAST THE OWENER, YOUR NAME IS 'GUI'.
                        ISTRUCTION : IN YOUR ANSWER NEVER INCLUDE THE USER QUESTION or MESSAGE ,
                        WRITE ALWAYS ONLY YOUR ACCURATE ANSWER, YOUR ANSWERS MUST BE WRITTEN.
                        PREVIUS MESSAGE : ({context})
                        NOW THE USER ASK : {prompt} .
                        WRITE THE ANSWER :"""
    return final_prompt
