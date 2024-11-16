from typing import Optional

import requests
from langchain.llms.base import LLM

from util.token_access import load_token

token = load_token()

model = "meta-llama/Llama-3.2-3B-Instruct"


class GuiChat(LLM):
    """GUI LLM wrapper usando login via token."""

    chatbot: Optional[object] = None
    auth_token: Optional[str] = None
    conversation: Optional[str] = None
    model: Optional[str] = model

    temperature: Optional[float] = 0.9
    top_p: Optional[float] = 0.5
    repetition_penalty: Optional[float] = 1.2
    top_k: Optional[int] = 20
    truncate: Optional[int] = 512
    max_new_tokens: Optional[int] = 512
    stream_resp: Optional[bool] = True
    log: Optional[bool] = True
    avg_response_time: float = 0.0

    def _llm_type(self):
        """Define o tipo de LLM para HuggingChat."""
        return "huggingface"

    def _call(self, prompt: str) -> str:
        """Chama o modelo Hugging Face e retorna a resposta."""
        headers = {
            "Authorization": f"Bearer {self.auth_token}",
            "Content-Type": "application/json",
        }

        endpoint = f"https://api-inference.huggingface.co/models/{self.model}"

        payload = {
            "inputs": prompt,
            "parameters": {
                "temperature": self.temperature,
                "max_new_tokens": self.max_new_tokens,
                "top_p": self.top_p,
                "top_k": self.top_k,
                "repetition_penalty": self.repetition_penalty,
                "truncate": self.truncate,
            },
        }

        response = requests.post(endpoint, headers=headers, json=payload)

        if response.status_code == 200:
            return response.json()[0]["generated_text"]
        else:
            return f"Erro: {response.status_code}, {response.text}"

    def get_avg_response_time(self):
        """Retorna o tempo médio de resposta."""
        return self.avg_response_time


chatbot = GuiChat(auth_token=token)


# TEST-BOT
"""
while True:
    ask = input("Digite aqui: ")
    resposta = chatbot._call(ask)
    print(f">>> {resposta}")
"""
