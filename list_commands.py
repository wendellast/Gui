import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QLabel,
    QListWidget,
    QMainWindow,
    QPushButton,
)


class JanelaC(QMainWindow):
    def __init__(self):
        super().__init__()


        self.label_JG = QLabel(self)
        self.label_JG.setText("COMANDOS")
        self.label_JG.setAlignment(Qt.AlignRight)
        self.label_JG.move(5, 5)
        self.label_JG.setStyleSheet(
            "QLabel {font-size:18px; color: #DB7399; font:bold}"
        )
        self.label_JG.resize(195, 20)

        # Lista de comandos
        self.ListaC = QListWidget(self)
        self.ListaC.setGeometry(5, 30, 290, 370)
        self.ListaC.setStyleSheet(
            """
            QListWidget::item {
                color: #9E6778;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #F2B8B1;
                width: 3px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #F2BFB1;
                min-height: 0px;
            }
            QScrollBar::add-line:vertical {
                background: #F2D3CD;
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
            QScrollBar::sub-line:vertical {
                background: #F2D3CD;
                height: 0px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }
        """
        )

        # Lista de comandos disponíveis
        ls = [
            "....",

        ]
        self.ListaC.addItems(ls)

        # Botão para fechar a janela
        self.botao_fechar = QPushButton("", self)
        self.botao_fechar.move(270, 5)
        self.botao_fechar.resize(20, 20)
        self.botao_fechar.setStyleSheet(
            "background-image: url(static/assets/img/closed.png); border-radius: 15px;"
        )
        self.botao_fechar.clicked.connect(self.fechartudo)

        # Carregar configurações da janela
        self.CarregarJanela()

    def CarregarJanela(self):
        """Configurações da Janela"""
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setGeometry(50, 50, 300, 410)
        self.setMinimumSize(300, 410)
        self.setMaximumSize(300, 410)
        self.setWindowOpacity(0.95)
        self.setStyleSheet("background-color: #F2B8B1")
        self.setWindowIcon(QIcon("static/assets/img/sara_icon.png"))
        self.setWindowTitle("COMANDOS")
        self.show()

    def fechartudo(self):
        """Fechar a aplicação"""
        print("botão fechar pressionado")
        sys.exit()

    def mousePressEvent(self, event):
        """Função para mover a janela ao clicar e arrastar"""
        if event.buttons() == Qt.LeftButton:
            self.dragPos = event.globalPos()
            event.accept()

    def mouseMoveEvent(self, event):
        """Função para mover a janela ao clicar e arrastar"""
        if event.buttons() == Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()


if __name__ == "__main__":
    aplicacao = QApplication(sys.argv)
    janela = JanelaC()
    sys.exit(aplicacao.exec())
