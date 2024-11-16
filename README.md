# GUI IA

Welcome! The GUI is a virtual assistant designed to answer your questions in a friendly, fun, and interactive way. Created to be your digital companion, it provides engaging responses to make your experience more enjoyable.

- **Model Used**: By default, we use the **meta-llama/Llama-3.2-3B-Instruct** model, but you can easily change it to any other model of your choice.

## Recommended

- Python 3.11.0 or higher
- A Hugging Face account to obtain your API token

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/wendellast/Gui.git
   cd Gui
   ```

2. **Install the dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the `.env` file**:
   - Rename the `.env-example` file to `.env`:
     ```bash
     mv .env-example .env
     ```
   - Edit the `.env` file and add your Hugging Face token:
     ```
     HUGGINGFACEHUB_API_TOKEN=your_token_here
     ```
   > **Note**: You can get your Hugging Face API token at [Hugging Face Tokens](https://huggingface.co/settings/tokens).

## How to Run


### option 1: Running via Server
To start the server, run:

```bash
python server.py
```

Open your browser and go to `http://localhost:7860` to interact with the AI chatbot.


### Option 2: Running via Graphical Interface

To start the server and open the graphical interface, simply run the following command:

```bash
python gui.py
```

This will launch the application with the virtual assistant interface, where you can interact using voice or buttons.

---

## Speech Configuration

The virtual assistant uses speech synthesis to respond to the user. jWe recommend using the **Letícia** voice, a high-quality Brazilian voice, for the best experience.

### 1. Using the **Letícia** Voice

We recommend using the **Letícia** voice. jTo set it up, follow these steps:

- Visit the [Louderpages - Letícia](https://louderpages.org/leticia) website.
- Github [Rhvoices](https://github.com/RHVoice/RHVoice)
- Follow the instructions to configure the **Letícia** voice.

### 2. Other Alternatives

If you prefer, you can also use other speech synthesis options:

- **Espeak**: jAn open-source alternative.
- **SAPI5 (Windows)**: jThe native speech synthesis API for Windows.

## API

### Example Usage via API:

```python
from gradio_client import Client

# ==========TEST API==========

def response_gui(input_text):
    client = Client("wendellast/GUI")
    result = client.predict(
        message=input_text,
        max_tokens=512,
        temperature=0.7,
        top_p=0.95,
        api_name="/chat",
    )
    return result

# Example call:
input_text = "Hello, how are you?"
response = response_gui(input_text)
print("AI Response:", response)
```

### Usage via LangChain Model

You can also use the model directly via LangChain:

- **Define the model** you want to use, such as `meta-llama/Llama-3.2-3B-Instruct`.
- Configure your access token in the `.env` file.
- Instantiate the wrapper for the model using the `GuiChat` class.

### Supported Parameters:
- `temperature`: Controls the randomness of the response.
- `top_p`: Controls the diversity of the responses.
- `repetition_penalty`: Penalizes repetitions for more varied answers.
- `max_new_tokens`: Maximum number of tokens generated in the response.

**Example usage**:
```python
from util.token_access import load_token
from your_package import GuiChat

token = load_token()
chatbot = GuiChat(auth_token=token)

while True:
    question = input("Ask here: ")
    answer = chatbot._call(question)
    print(f"Response: {answer}")
```
