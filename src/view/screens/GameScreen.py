from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView, Markdown
from textual.widget import Widget
from textual.widgets import Header, Footer, Button
from textual.containers import HorizontalGroup, VerticalGroup
from textual.message import Message

from view.widgets.CellButton import CellButton
from view.widgets.BoardWidget import BoardWidget
from view import screens
from GameController import GameController


class GameScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def __init__(self, controller: GameController, **kwargs) -> None:
        super().__init__(**kwargs)

        self._controller = controller
        self._board_widget = BoardWidget(self._controller)
        self.active_player = self._controller.get_active_player()

    def compose(self) -> ComposeResult:
        yield Header()

        # Header
        token_color_name = CellButton.token_color[self.active_player].title()
        self.header_markdown: Markdown = Markdown(f"# Player {self.active_player.value} ({token_color_name}), it's your turn!")
        yield self.header_markdown

        # Board
        yield self._board_widget
        yield Footer()

    @on(BoardWidget.MoveMade)
    def on_move_made(self, event: BoardWidget.MoveMade) -> None:
        self._controller.play_move(event.move)
        self.app.switch_screen(screens.GameScreen(self._controller))

    def action_back(self) -> None:
        """Returns to the Main Menu screen"""
        self.app.switch_screen(screens.MainMenuScreen(self._controller))
