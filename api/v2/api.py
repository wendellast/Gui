from gradio_client import Client

import json

from datetime import datetime

now = datetime.now()
with open("data/config.json", "r", encoding="UTF-8") as file:
    config = json.load(file)



system_message = f"""
  # INFORMAÇÕES GERAIS: (hoje é {now.strftime("%d/%m/%Y %H:%M:%S")},
    # VOCÊ FOI CRIADO PELO  GRUPO Last, O SEU NOME É 'GUI',
    # ESTAS SÃO SUAS CONFIGURAÇÕES E REGRAS: {config},
    # SUAS RESPOSTAS DEVEM SER SARCASTICAMENTE DIVERTIDAS :),
"""



def response_gui(input_text):
    client = Client("wendellast/GUI")
    result = client.predict(
        message=input_text,
        system_message=system_message,
        max_tokens=512,
        temperature=0.7,
        top_p=0.95,
        api_name="/chat"
    )

    return result
