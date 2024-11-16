from langchain.prompts import PromptTemplate


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
        input_variables=[
            "name",
            "data_atual",
            "regras",
            "desenvolvedor_name",
            "desenvolvedor_description",
            "pais",
            "historico",
            "mensagem",
        ],
        template=template_gui,
    )

    return prompt_template
