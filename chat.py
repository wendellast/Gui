from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QTextEdit, QLineEdit
from config.api import response_gui



class ApiRequestThread(QThread):
    """Thread para fazer a requisição à API sem bloquear a UI"""
    response_received = Signal(str)  # Sinal para passar a resposta de volta

    def __init__(self, message):
        super().__init__()
        self.message = message

    def run(self):
        """Executa a requisição à API em segundo plano"""
        response = response_gui(self.message)
        self.response_received.emit(response)

class ChatWindow(QWidget):
    """Janela de Chat"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Chat")
        self.setGeometry(460, 50, 300, 400)

        # Layout do chat
        layout = QVBoxLayout()

        # Campo de exibição de mensagens
        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)

        # Campo de entrada de texto
        self.chat_input = QLineEdit()
        layout.addWidget(self.chat_input)

        # Botão para enviar mensagem
        send_button = QPushButton("Enviar")
        send_button.clicked.connect(self.send_message)
        layout.addWidget(send_button)

        self.setLayout(layout)

    def send_message(self):
        """Envia mensagem do campo de texto para o display do chat"""
        message = self.chat_input.text().strip()
        if message:
            self.chat_display.append(f"Você: {message}")
            self.chat_input.clear()

            # Cria e inicia a thread para a requisição da API
            self.thread = ApiRequestThread(message)
            self.thread.response_received.connect(self.display_response)  # Conecta o sinal
            self.thread.start()

    def display_response(self, response):
        """Exibe a resposta do bot após a requisição"""
        self.chat_display.append(f"Bot: {response}")
