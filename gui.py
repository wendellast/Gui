from textual import on
from textual.app import App
from textual.containers import Container, Horizontal, VerticalScroll
from textual.widgets import Button, Footer, Header, Input, Label

from api.orange import response_gui


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
                self.input = Input("Digite aqui")

                with Horizontal():
                    yield self.input
                    yield Button("Enter", id="button1")

    @on(Button.Pressed, "#button1")
    def resposta(self):
        gui_resp = response_gui(self.input.value)
        self.label.update(
            f"""
            [yellow b] User: [/] [yellow] {self.input.value} [/] \n
            [green b] GUI: [/] [green] {gui_resp} [/]
            """
        )


MyApp().run()
