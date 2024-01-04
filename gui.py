import sqlite3

from textual import on
from textual.app import App
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Label

from api.orange import response_gui
from config.fuctions import logging_error


class MyApp(App):
    TITLE = "GUI"

    CSS_PATH = "style/gui.tcss"

    def compose(self):
        with Container():
            yield Header(show_clock=True)
            yield Footer()
            with VerticalScroll():
                self.label = Label()
                yield self.label
                self.input = Input(valid_empty=False, placeholder="Digite Aqui!")

                with Horizontal():
                    yield self.input
                    yield Button("Enter", id="button1")

    @on(Button.Pressed, "#button1")
    def resposta(self):
        try:
            gui_resp = response_gui(self.input.value)
        except:
            print("Erro ao gera a resposta")

        try:
            conn = sqlite3.connect("memory.db")
            cursor = conn.cursor()

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS mind (user_ask TEXT, gui_response TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)"
            )

            # Insere vários registros na tabela
            cursor.executemany(
                "INSERT INTO mind (user_ask, gui_response) VALUES (?, ?)",
                [(f"{self.input.value}", f"{gui_resp}")],
            )

            conn.commit()
            # Fecha a conexão com o banco de dados
            conn.close()
        except Exception as error:
            logging_error(error)

        try:
            self.label.update(
                f"""
                [yellow b] User: [/] [yellow] {self.input.value} [/] \n
                [green b] GUI: [/] [green] {gui_resp} [/]
                """
            )
            self.input.value = ""
        except Exception as error:
            logging_error(error)
            self.exit()


MyApp().run()
