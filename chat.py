from PySide6.QtWidgets import (
    QLineEdit,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from config.threads import ApiRequestThread


class ChatWindow(QWidget):
    """Janela de Chat"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mini Chat")
        self.setGeometry(460, 50, 300, 400)

        layout = QVBoxLayout()


        self.chat_display = QTextEdit()
        self.chat_display.setReadOnly(True)
        layout.addWidget(self.chat_display)


        self.chat_input = QLineEdit()
        layout.addWidget(self.chat_input)


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


            self.thread = ApiRequestThread(message)
            self.thread.response_received.connect(
                self.display_response
            )
            self.thread.start()

    def display_response(self, response):
        """Exibe a resposta do bot após a requisição"""
        self.chat_display.append(f"Bot: {response}")
