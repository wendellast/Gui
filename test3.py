import sys
import subprocess
import speech_recognition as sr
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PySide6.QtGui import QMovie, QIcon
from PySide6.QtCore import Qt, QTimer, QDate, QTime, QThread, Signal
from config.api import response_gui
from chat import ChatWindow
import time


Thema = 'static/assets/img/gui.gif'
Versao = 'Versão Beta v2.0'


class SpeakThread(QThread):
    """Thread para sintetizar fala"""
    def __init__(self, texto):
        super().__init__()
        self.texto = texto


    def run(self):
        command = ["spd-say", "-o", "rhvoice", "-y", "leticia-f123", "-w", self.texto]
        subprocess.call(command)


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
                print("Ajustando ao ruído ambiente...")
                recognizer.adjust_for_ambient_noise(source)

                while self.running:
                    if not self.listening:
                        time.sleep(0.1)
                        continue

                    print("Ouvindo...")
                    try:
                        audio = recognizer.listen(source, timeout=10)
                        text = recognizer.recognize_google(audio, language="pt-BR").lower()
                        print(f"Texto reconhecido: {text}")
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
        #print("Thread de áudio parada.")

# Classe para requisição à API em uma thread separada
class BotResponseThread(QThread):
    """Thread para obter a resposta do bot da API"""
    bot_response_ready = Signal(str)  # Sinal para passar a resposta do bot

    def __init__(self, user_text):
        super().__init__()
        self.user_text = user_text

    def run(self):
        try:
            response = response_gui(self.user_text)
            self.bot_response_ready.emit(response)
        except Exception as e:
            print(f"Erro ao obter resposta da API: {e}")
            self.bot_response_ready.emit("Desculpe, não consegui processar a resposta no momento.")

# Classe principal da Janela
class Janela(QMainWindow):
    def __init__(self):
        super().__init__()

        # Configuração do GIF animado
        self.label_gif = QLabel(self)
        self.label_gif.setAlignment(Qt.AlignCenter)
        self.label_gif.setGeometry(0, 0, 400, 300)
        self.movie = QMovie(Thema)
        self.label_gif.setMovie(self.movie)
        self.movie.start()

        # Labels de informações
        self.label_version = QLabel(Versao, self)
        self.label_version.setAlignment(Qt.AlignCenter)
        self.label_version.setGeometry(265, 270, 131, 20)
        self.label_version.setStyleSheet('font-size:14px;color:#D971B4')

        data_hoje = QDate.currentDate().toString('dd/MM/yyyy')
        self.label_data = QLabel(data_hoje, self)
        self.label_data.setAlignment(Qt.AlignCenter)
        self.label_data.setGeometry(316, 25, 75, 20)
        self.label_data.setStyleSheet('font-size:14px;color:#D971B4')

        self.label_horas = QLabel(self)
        self.label_horas.setGeometry(0, 25, 71, 20)
        self.label_horas.setStyleSheet('font-size:14px;color:#D971B4')
        self.update_time()
        timer_horas = QTimer(self)
        timer_horas.timeout.connect(self.update_time)
        timer_horas.start(1000)

        # Botões
        self.botao_fechar = QPushButton("", self)
        self.botao_fechar.setGeometry(370, 5, 20, 20)
        self.botao_fechar.setStyleSheet("background-image:url(static/assets/img/closed.png);border-radius: 10px")
        self.botao_fechar.clicked.connect(self.fechartudo)

        self.botao_chat = QPushButton("Abrir Chat", self)
        self.botao_chat.setGeometry(170, 3, 80, 20)
        self.botao_chat.setStyleSheet("background-color: #D971B4; color: white; border-radius: 5px;")
        self.botao_chat.clicked.connect(self.abrir_chat)

        # Configuração da janela
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(50, 50, 400, 300)
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)
        self.setWindowIcon(QIcon('static/assets/img/sara_icon.png'))
        self.setWindowTitle("Assistente Virtual")
        self.show()

        # Inicializa o reconhecimento de voz
        self.audio_thread = AudioRecognitionThread()
        self.audio_thread.voice_recognized.connect(self.handle_voice_command)
        self.audio_thread.start()

    def update_time(self):
        self.label_horas.setText(QTime.currentTime().toString("HH:mm:ss"))

    def handle_voice_command(self, text):
        """Processa o comando de voz recebido e faz a chamada à API em uma thread separada"""
        #print(f"Comando de voz recebido: {text}")
        if text.startswith("oi") or text.startswith("gui"):
            print(f"Processando comando: {text}")
            self.bot_response_thread = BotResponseThread(text)
            self.bot_response_thread.bot_response_ready.connect(self.speak_response)
            self.bot_response_thread.start()


    def speak_response(self, response_text):
        """Fala a resposta do bot sem bloquear a interface"""
        self.speak_thread = SpeakThread(response_text)
        self.speak_thread.start()

    def abrir_chat(self):
        print("Abrindo chat...")
        if not hasattr(self, 'chat_window') or not self.chat_window:
            self.chat_window = ChatWindow()
            self.chat_window.show()

    def stop_speaking(self):
        """Interrompe a fala do bot imediatamente."""
        subprocess.call(["spd-say", "--stop"])


    def fechartudo(self):
        self.stop_speaking()
        self.audio_thread.stop()
        sys.exit()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.position().toPoint()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.position().toPoint() - self.dragPos)
            self.dragPos = event.position().toPoint()
            event.accept()

# Execução da aplicação
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Janela()
    sys.exit(app.exec())
