import json

try:
    with open("data/config.json", "r", encoding="UTF-8") as file:
        config: dict = json.load(file)
except:
    raise "ERROR ao carregar config.json"


def extrair_dados_config(config: dict = config):
    try:

        regras: str = "\n".join(
            [
                f"- {rule['rule_name']}: {rule['description']}"
                for rule in config["config"]["rules"]
            ]
        )

        desenvolvedor_name: str = config["config"]["developers Hublast"]["wendellast"][
            "name"
        ]

        name_gui: str = config["config"]["name"]
        country: str = config["config"]["status"]["country"]
        version: str = config["config"]["version"]

        desenvolvedor_description: dict = config["config"]["developers Hublast"]

        return regras, desenvolvedor_name, desenvolvedor_description, name_gui, country, version

    except KeyError as e:
        print(f"Erro ao acessar a chave: {e}")
        return None
