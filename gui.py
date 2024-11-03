import sqlite3

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Label
from api.v2.api import response_gui
from config.logger import logging_error


class MyApp(App):
    TITLE = "GUI"

    CSS_PATH = "static/assets/style/gui.tcss"

    BINDINGS = [("enter", "response()", "Pronto"), ("ctrl+c", "exit_app()", "kill")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

        with Container():
            with VerticalScroll():
                self.label = Label()
                yield self.label
                self.input = Input(valid_empty=True, placeholder="Digite Aqui!")

                with Horizontal():
                    yield self.input
                    yield Button("Enter", id="button1")

    def action_exit_app(self):
        self.exit()

    @on(Button.Pressed, "#button1")
    def action_response(self):
        try:
            gui_resp = response_gui(self.input.value)
        except:
            logging_error("Response Error")

        try:
            conn = sqlite3.connect("memory.db")
            cursor = conn.cursor()

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS mind (user_ask TEXT, gui_response TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)"
            )

            cursor.executemany(
                "INSERT INTO mind (user_ask, gui_response) VALUES (?, ?)",
                [(f"{self.input.value}", f"{gui_resp}")],
            )

            conn.commit()

            conn.close()
        except Exception as error:
            logging_error(error)

        try:
            msg_temp = []
            msg_temp.append(self.input.value)

            msg_user = f"""[yellow b] User: [/] [yellow] {msg_temp[0]} [/]"""

            msg_gui = f"""[purple b] Gui: [/] [purple] {gui_resp} [/]"""

            self.label.update(f"""{msg_user.strip()}\n{msg_gui.strip()}""")

            self.input.value = " "
            msg_temp.clear()

        except Exception as error:
            logging_error(error)
            self.exit()


MyApp().run()
