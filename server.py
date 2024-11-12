import gradio as gr
from huggingface_hub import InferenceClient
from datasets import load_dataset
import dotenv
import os
from langchain.prompts import PromptTemplate
from typing import List, Tuple, Optional
from manage.prompt_gui import prompt_template_gui, template_gui, extrair_dados_config
from datetime import datetime
from util.token_access import load_token
regras, desenvolvedor_name, country, name_gui, desenvolvedor_description = extrair_dados_config()

dotenv.load_dotenv(dotenv.find_dotenv())

token: Optional[str] = load_token()
now: datetime = datetime.now()


template_gui = template_gui()
prompt_template = prompt_template_gui(template_gui)


client: InferenceClient = InferenceClient(
    model="meta-llama/Llama-3.2-3B-Instruct",
    token=token
)


dataset = load_dataset("wendellast/GUI-Ban")



def get_response_from_huggingface_dataset(
    message: str,
    dataset
) -> Optional[str]:
    for data in dataset["train"]:
        if "dialog" in data and len(data["dialog"]) > 1:
            input_text: str = data["dialog"][0].lower()
            response_text: str = data["dialog"][1]

            if input_text == message.lower():
                return response_text
    return None


def respond(
    message: str,
    history: List[Tuple[str, str]],
    system_message: str,
    max_tokens: int,
    temperature: float,
    top_p: float,
) -> any:

    response: Optional[str] = get_response_from_huggingface_dataset(message, dataset)
    if response:
        yield response
        return


    historico: str = ""
    for user_msg, bot_reply in history:
        if user_msg:
            historico += f"Usuário: {user_msg}\n"
        if bot_reply:
            historico += f"IA: {bot_reply}\n"


    prompt: str = prompt_template.format(
        name=name_gui,
        data_atual=now.strftime("%d/%m/%Y %H:%M:%S"),
        regras=regras,
        desenvolvedor_name=desenvolvedor_name,
        desenvolvedor_description=desenvolvedor_description,
        pais=country,
        historico=historico.strip(),
        mensagem=message
                )


    messages: List[dict] = [{"role": "system", "content": prompt}]
    response: str = ""


    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token: str = message.choices[0].delta.content
        response += token
        yield response


demo: gr.ChatInterface = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value='', label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(minimum=0.1, maximum=1.0, value=0.95, step=0.05, label="Top-p (nucleus sampling)"),
    ],
    title="GUI",
    theme='gstaff/xkcd'
)

# Inicializar a aplicação
if __name__ == "__main__":
    demo.launch()
