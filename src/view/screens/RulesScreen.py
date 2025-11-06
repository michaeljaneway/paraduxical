from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView, Markdown
from textual.widgets import Header, Footer, Button

from GameController import GameController
from view import screens


class RulesScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Back to Main Menu")]
    
    def __init__(self, controller: GameController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller

    def compose(self) -> ComposeResult:
        yield Header()

        # Load rules from markdown file
        rules_path = Path("./assets/rules.md")
        rules_content = rules_path.read_text("utf-8")

        with VerticalScroll(classes="container middle"):
            yield Markdown(rules_content)
            yield Button("Back to Main Menu", id="back")

        yield Footer()

    @on(Button.Pressed, "#back")
    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen(self._controller))
