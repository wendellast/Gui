from gradio_client import Client

#  ==========TEST API==========


def response_gui(input_text) -> str:
    client = Client("wendellast/GUI")
    result = client.predict(
        message=input_text,
        max_tokens=212,
        temperature=0.7,
        top_p=0.95,
        api_name="/chat",
    )

    return result
