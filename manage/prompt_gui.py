import json
from datetime import datetime
import os
from langchain.prompts import PromptTemplate
from typing import List, Tuple, Optional


now: datetime = datetime.now()

try:
    with open("data/config.json", "r", encoding="UTF-8") as file:
        config: dict = json.load(file)
except:
    raise "ERRO ao carrega config.json"




def extrair_dados_config(config: dict = config):
    try:

        regras: str = "\n".join([f"- {rule['rule_name']}: {rule['description']}" for rule in config["config"]["rules"]])

        desenvolvedor_name: str = config["config"]["developers Hublast"]["wendellast"]["name"]

        name_gui: str = config["config"]["name"]
        country: str = config["config"]["status"]["country"]


        desenvolvedor_description: dict = config["config"]["developers Hublast"]

        return regras, desenvolvedor_name, desenvolvedor_description, name_gui, country


    except KeyError as e:
        print(f"Erro ao acessar a chave: {e}")
        return None

def template_gui() -> str:

    template: str = """
        Descrição:
        - Seu nome é : '{name}'
        - Você é {name}, uma IA programada para responder de forma engraçada e sarcástica, mas evite usar as palavras "sarcástica" e "divertida" nas suas respostas.
        - Hoje é {data_atual}. Aqui estão algumas regras que você deve seguir:

        Regras:
        {regras}

        Configuração:
        - Nome do desenvolvedor: {desenvolvedor_name}
        - Descrição do desenvolvedor: {desenvolvedor_description}
        - País de origem: {pais}

        Histórico de conversa:
        {historico}

        Usuário: {mensagem}
        IA-GUI:
    """

    return template


def prompt_template_gui(template_gui: str) -> str:
    prompt_template: PromptTemplate = PromptTemplate(
        input_variables=["name", "data_atual", "regras", "desenvolvedor_name", "desenvolvedor_description",  "pais", "historico", "mensagem"],
        template = template_gui
    )

    return prompt_template
