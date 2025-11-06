from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView, Markdown, Button
from textual.widgets import Header, Footer

from enums.BoardLayout import BoardLayout
from view import screens

NEW_GAME_MD = """
# Starting a New Game


"""


class NewGameScreen(Screen[BoardLayout]):
    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def compose(self) -> ComposeResult:
        yield Header()
        
        with VerticalScroll():
            yield Markdown(NEW_GAME_MD)
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
        self.app.switch_screen(screens.MainMenuScreen())

    def create_game(self, board_type: BoardLayout) -> None:
        pass
