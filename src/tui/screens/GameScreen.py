from textual import on
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown

from GameClientController import GameClientController
from tui import screens
from tui.widgets.GameWidget import GameWidget
from tui.widgets.CellButton import CellButton


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
        self.app.switch_screen(screens.MainMenuScreen(self._controller))

    def action_save(self) -> None:
        """Brings the player to the save game screen"""
        self.app.switch_screen(screens.SaveScreen(self._controller))
