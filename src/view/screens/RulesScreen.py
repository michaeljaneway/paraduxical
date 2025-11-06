from textual import on
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView, Markdown
from textual.widgets import Header, Footer

from view import screens

RULES_MD = """
# Paraduxical Rules

***

## Objective

Be the first player to line up FOUR of your tokens in a row along the horizontal or vertical axes.
"""


class RulesScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def compose(self) -> ComposeResult:
        yield Header()

        with Container(classes="container middle"):
            yield Markdown(RULES_MD)

        yield Footer()

    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen())
