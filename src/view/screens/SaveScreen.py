from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, Label, ListItem, ListView, Markdown

from GameController import GameController
from view import screens


class SaveScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Back to Game")]

    def __init__(self, controller: GameController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller

    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalScroll(classes="container middle"):
            yield Markdown(f"# Saving game")

            yield Input(placeholder="Savefile Name", restrict=r"^[\w\-. ]+$")

            with ListView():
                yield ListItem(Label("Cancel"), id="cancel")

        yield Footer()

    """Callbacks"""

    @on(Input.Submitted)
    def on_save_name_submitted(self, event: Input.Submitted) -> None:
        self._controller.save_game(event.value)
        self.app.switch_screen(screens.GameScreen(self._controller))

    @on(ListView.Selected, item="#cancel")
    def action_back(self):
        self.app.switch_screen(screens.GameScreen(self._controller))
