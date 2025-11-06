from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView, Markdown
from textual.widgets import Header, Footer

from view import screens


class RulesScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def compose(self) -> ComposeResult:
        yield Header()

        # Load rules from markdown file
        rules_path = Path("./assets/rules.md")
        rules_content = rules_path.read_text("utf-8")

        with VerticalScroll(classes="container middle"):
            yield Markdown(rules_content)
            

        yield Footer()

    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen())
