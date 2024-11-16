import sys

import psutil
from PySide6.QtCore import QDate, QProcess, Qt, QTime, QTimer
from PySide6.QtGui import QIcon, QMovie
from PySide6.QtWidgets import QApplication, QLabel, QMainWindow, QPushButton

from chat import ChatWindow
from config.threads import (
    AudioRecognitionThread,
    BotResponseThread,
    SpeakThread,
)
from util.data_config import extrair_dados_config

THEME = "static/assets/img/gui.gif"
_, _, _, _, _, VERSION = extrair_dados_config()




class Janela(QMainWindow):
    """Janela Principal"""

    def __init__(self):
        super().__init__()

        # Label para o GIF
        self.label_gif = QLabel(self)
        self.label_gif.setAlignment(Qt.AlignCenter)
        self.label_gif.move(0, 0)
        self.label_gif.resize(400, 300)
        self.movie = QMovie(THEME)
        self.label_gif.setMovie(self.movie)
        self.movie.start()

        self.label_gui = QLabel(self)
        self.label_gui.setText("GUI")
        self.label_gui.setAlignment(Qt.AlignCenter)
        self.label_gui.move(0, 0)
        self.label_gui.setStyleSheet("QLabel {font:bold;font-size:16px;color:#D9B8B8}")
        self.label_gui.resize(400, 300)

        self.label_cpu = QLabel(self)
        self.label_cpu.setText("CPU: 32%")
        self.label_cpu.setAlignment(Qt.AlignCenter)
        self.label_cpu.move(10, 270)
        self.label_cpu.setStyleSheet("QLabel {font:bold;font-size:14px;color:#D971B4}")
        self.label_cpu.resize(131, 20)

        cpu_timer = QTimer(self)
        cpu_timer.timeout.connect(self.MostrarCPU)
        cpu_timer.start(1000)

        self.label_assv = QLabel(self)
        self.label_assv.setText("Assistente Virtual")
        self.label_assv.move(5, 5)
        self.label_assv.setStyleSheet("QLabel {font:bold;font-size:14px;color:#D971B4}")
        self.label_assv.resize(200, 20)

        # Label para a versão
        self.label_version = QLabel(self)
        self.label_version.setText("versão: " + str(VERSION))
        self.label_version.setAlignment(Qt.AlignCenter)
        self.label_version.move(265, 270)
        self.label_version.setStyleSheet("QLabel {font-size:14px;color:#D971B4}")
        self.label_version.resize(131, 20)

        # Label para a data atual
        data_atual = QDate.currentDate()
        data_hoje = data_atual.toString("dd/MM/yyyy")
        self.label_data = QLabel(self)
        self.label_data.setText(data_hoje)
        self.label_data.setAlignment(Qt.AlignCenter)
        self.label_data.move(316, 25)
        self.label_data.setStyleSheet("QLabel {font-size:14px;color:#D971B4}")
        self.label_data.resize(75, 20)


        self.label_horas = QLabel(self)
        self.label_horas.setText("22:36:09")
        self.label_horas.setAlignment(Qt.AlignCenter)
        self.label_horas.move(0, 25)
        self.label_horas.setStyleSheet("QLabel {font-size:14px;color:#D971B4}")
        self.label_horas.resize(71, 20)

        horas_timer = QTimer(self)
        horas_timer.timeout.connect(self.MostrarHorras)
        horas_timer.start(1000)


        botao_fechar = QPushButton("", self)
        botao_fechar.move(370, 5)
        botao_fechar.resize(20, 20)
        botao_fechar.setStyleSheet(
            "background-image : url(static/assets/img/closed.png);border-radius: 15px"
        )
        botao_fechar.clicked.connect(self.fechartudo)


        botao_chat = QPushButton("Abrir Chat", self)
        botao_chat.move(170, 3)
        botao_chat.resize(80, 20)
        botao_chat.setStyleSheet(
            "background-color: #D971B4; color: white; border-radius: 5px;"
        )
        botao_chat.clicked.connect(self.abrir_chat)


        botao_lista = QPushButton("", self)
        botao_lista.move(330, 3)
        botao_lista.resize(20, 20)
        botao_lista.setStyleSheet(
            "background-image : url(static/assets/img/list_icon.png);border-radius: 0px;"
        )
        botao_lista.clicked.connect(self.MostrarLista)


        self.CarregarJanela()
        self.audio_thread = AudioRecognitionThread()
        self.audio_thread.voice_recognized.connect(self.handle_voice_command)
        self.audio_thread.start()
        self.chat_window = None

    def handle_voice_command(self, text):
        """Processa o comando de voz recebido e faz a chamada à API em uma thread separada"""
        # print(f"Comando de voz recebido: {text}")
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
        """Abre a janela de chat"""
        if self.chat_window is None:
            self.chat_window = ChatWindow()
        self.chat_window.show()

    def MostrarLista(self):
        self.listac = QProcess()
        self.listac.start("python3", ["list_commands.py"])

    def CarregarJanela(self):
        self.setWindowFlag(Qt.FramelessWindowHint)  # Sem botões e título
        self.setGeometry(50, 50, 400, 300)
        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)
        self.setWindowOpacity(0.98)
        self.setWindowIcon(QIcon("static/assets/img/sara_icon.png"))
        self.setWindowTitle("Assistente Virtual")
        self.show()

    def fechartudo(self):
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

    def MostrarHorras(self):
        hora_atual = QTime.currentTime()
        label_time = hora_atual.toString("hh:mm:ss")
        self.label_horas.setText(label_time)

    def MostrarCPU(self):
        usocpu = str(psutil.cpu_percent())
        self.label_cpu.setText(f"Uso da CPU: {usocpu}%")


# Execução da aplicação
if __name__ == "__main__":
    aplicacao = QApplication(sys.argv)
    j = Janela()
    sys.exit(aplicacao.exec())
