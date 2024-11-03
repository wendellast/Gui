import gradio as gr
import dotenv
import os
import json

from datetime import datetime

from huggingface_hub import InferenceClient

dotenv.load_dotenv(dotenv.find_dotenv())

now = datetime.now()

token = os.getenv("token")

with open("data/config.json", "r", encoding="UTF-8") as file:
    config = json.load(file)

client = InferenceClient(
    model="meta-llama/Llama-3.2-3B-Instruct",
    token=token
)


system_messages = f"""
  # INFORMAÇÕES GERAIS: (hoje é {now.strftime("%d/%m/%Y %H:%M:%S")},
    # VOCÊ FOI CRIADO PELO  GRUPO Last, O SEU NOME É 'GUI',
    # ESTAS SÃO SUAS CONFIGURAÇÕES E REGRAS: {config},
    # SUAS RESPOSTAS DEVEM SER SARCASTICAMENTE DIVERTIDAS :),
"""


def respond(
    message,
    history: list[tuple[str, str]],
    system_message,
    max_tokens,
    temperature,
    top_p,
):
    messages = [{"role": "system", "content": system_message}]

    for val in history:
        if val[0]:
            messages.append({"role": "user", "content": val[0]})
        if val[1]:
            messages.append({"role": "assistant", "content": val[1]})

    messages.append({"role": "user", "content": message})

    response = ""

    for message in client.chat_completion(
        messages,
        max_tokens=max_tokens,
        stream=True,
        temperature=temperature,
        top_p=top_p,
    ):
        token = message.choices[0].delta.content

        response += token
        yield response


demo = gr.ChatInterface(
    respond,
    additional_inputs=[
        gr.Textbox(value=system_messages, label="System message"),
        gr.Slider(minimum=1, maximum=2048, value=512, step=1, label="Max new tokens"),
        gr.Slider(minimum=0.1, maximum=4.0, value=0.7, step=0.1, label="Temperature"),
        gr.Slider(
            minimum=0.1,
            maximum=1.0,
            value=0.95,
            step=0.05,
            label="Top-p (nucleus sampling)",
        ),
    ],
)


if __name__ == "__main__":
    demo.launch()
