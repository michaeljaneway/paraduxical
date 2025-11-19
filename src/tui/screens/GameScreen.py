from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown

from GameClientController import GameClientController
from shared.enums.EventType import GameEvent
from tui import screens
from tui.widgets.CellButton import CellButton
from tui.widgets.GameWidget import GameWidget


class GameScreen(Screen[None]):
    """Displays the active game to the user"""

    BINDINGS = [
        ("escape", "back", "Back to Main Menu"),
        ("s", "save", "Save Game"),
    ]

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)

        self._controller = controller
        self._board_widget = GameWidget(self._controller)
        self.active_player = self._controller.get_active_player()

        self._controller.bind_callback(GameEvent.GameCleared, self.action_back)

    def compose(self) -> ComposeResult:
        yield Header()

        # Player Turn Text
        token_color_name = CellButton.token_color[self.active_player].title()
        self.header_markdown: Markdown = Markdown(f"# Player {self.active_player.value} ({token_color_name}), it's your turn!")
        yield self.header_markdown

        # Board
        yield self._board_widget

        yield Footer()

    """Actions"""

    def action_back(self) -> None:
        """Returns to the Main Menu screen"""
        self.app.pop_screen()

    def action_save(self) -> None:
        """Brings the player to the save game screen"""
        self.app.push_screen(screens.SaveScreen(self._controller))
