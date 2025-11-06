from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView, Markdown, Button
from textual.widgets import Header, Footer

from GameController import GameController
from enums.BoardLayout import BoardLayout
from view import screens

class NewGameScreen(Screen[BoardLayout]):
    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def __init__(self, controller: GameController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller

    def compose(self) -> ComposeResult:
        yield Header()

        # Load rules from markdown file
        rules_path = Path("./assets/newgame.md")
        rules_content = rules_path.read_text("utf-8")
        
        with VerticalScroll():
            yield Markdown(rules_content)
            with ListView():
                yield ListItem(Label("\\/ Diagonal Layout \\/"), id="diag")
                yield ListItem(Label("-- Horizontal Layout --"), id="horz")

        yield Footer()

    @on(ListView.Selected, item="#diag")
    def action_diagonal_selected(self) -> None:
        self.create_game(BoardLayout.DIAG)

    @on(ListView.Selected, item="#horz")
    def action_horizontal_selected(self) -> None:
        self.create_game(BoardLayout.HORZ)

    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen(self._controller))

    def create_game(self, board_type: BoardLayout) -> None:
        pass
