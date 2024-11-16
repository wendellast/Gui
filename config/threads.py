from PySide6.QtCore import  QThread, Signal
from util.command_actions import command_resp
from config.api import response_gui

import speech_recognition as sr
import subprocess
import time
import subprocess
import platform
import pyttsx3


class SpeakThread(QThread):
    """Thread para sintetizar fala"""

    def __init__(self, texto):
        super().__init__()
        self.texto = texto

    def run(self):
        system = platform.system()

        if system == "Windows":
            # Usar pyttsx3 no Windows
            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            leticia_found = False
            for voice in voices:
                if "Letícia" in voice.name:
                    engine.setProperty('voice', voice.id)
                    leticia_found = True
                    break
            if not leticia_found:
                engine.setProperty('voice', voices[0].id)

            engine.say(self.texto)
            engine.runAndWait()

        elif system == "Linux":

            engine = pyttsx3.init()
            voices = engine.getProperty('voices')
            leticia_found = False
            for voice in voices:
                if "Letícia" in voice.name:
                    engine.setProperty('voice', voice.id)
                    leticia_found = True
                    break
            if not leticia_found:

                command = ["spd-say", "-o", "rhvoice", "-y", "leticia-f123", "-w", self.texto]
                try:
                    subprocess.call(command)
                    return
                except FileNotFoundError:

                    engine.setProperty('voice', 'english-us')
                    engine.say(self.texto)
                    engine.runAndWait()
                    return

            # Se achou a voz Letícia no pyttsx3
            engine.say(self.texto)
            engine.runAndWait()



class AudioRecognitionThread(QThread):
    """Thread para reconhecimento de áudio"""

    voice_recognized = Signal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.listening = True

    def run(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                # print("Ajustando ao ruído ambiente...")
                recognizer.adjust_for_ambient_noise(source)

                while self.running:
                    if not self.listening:
                        time.sleep(0.1)
                        continue

                    print("Ouvindo...")
                    try:
                        audio = recognizer.listen(source, timeout=10)
                        text = recognizer.recognize_google(
                            audio, language="pt-BR"
                        ).lower()
                        # print(f"Texto reconhecido: {text}")
                        self.voice_recognized.emit(text)

                    except sr.UnknownValueError:
                        print("Não foi possível entender o áudio.")
                    except sr.RequestError as e:
                        print(f"Erro no serviço de reconhecimento: {e}.")
                    except Exception as e:
                        print(f"Erro inesperado: {e}.")

        except Exception as e:
            print(f"Erro ao iniciar o microfone: {e}")

    def stop(self):
        """Para a execução da thread"""
        self.running = False
        # print("Thread de áudio parada.")


class BotResponseThread(QThread):
    """Thread para obter a resposta do bot da API"""

    bot_response_ready = Signal(str)

    def __init__(self, user_text):
        super().__init__()
        self.user_text = user_text

    def run(self):
        try:
            command_pc = command_resp(self.user_text)
            if command_pc == None:
                response = response_gui(self.user_text)
            else:
                response = command_pc
            self.bot_response_ready.emit(response)
        except Exception as e:
            print(f"Erro ao obter resposta da API: {e}")
            self.bot_response_ready.emit(
                "Desculpe, não consegui processar a resposta no momento."
            )


#CHAT
class ApiRequestThread(QThread):
    """Thread para fazer a requisição à API sem bloquear a UI"""

    response_received = Signal(str)

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        """Executa a requisição à API em segundo plano"""
        response = response_gui(self.message)
        self.response_received.emit(response)
