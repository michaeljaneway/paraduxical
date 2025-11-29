from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from tui import screens


class RulesScreen(Screen[None]):
    """Displays Paradux rules to the user"""

    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller

    def compose(self) -> ComposeResult:
        yield Header()

        # Load rules from markdown file
        rules_path = Path("./assets/rules.md")
        rules_content = rules_path.read_text("utf-8")

        with VerticalScroll(classes="container middle"):
            yield Markdown(rules_content)
            with ListView():
                yield ListItem(Label("Back to Main Menu"), id="back")

        yield Footer()

    @on(ListView.Selected, item="#back")
    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen(self._controller))
