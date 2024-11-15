from PySide6.QtWidgets import QPushButton, QWidget, QVBoxLayout, QTextEdit, QLineEdit

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
            # Aqui você pode adicionar a resposta do bot ou qualquer outra funcionalidade
            self.chat_display.append("Bot: Mensagem recebida!")
            self.chat_input.clear()
