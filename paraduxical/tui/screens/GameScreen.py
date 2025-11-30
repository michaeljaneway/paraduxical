from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown

from GameClientController import GameClientController
from shared.enums import GameEvent, TokenType
from tui import screens
from tui.events.TuiGameEvents import TuiGameEvents
from tui.widgets.CellButton import CellButton
from tui.widgets.GameWidget import GameWidget


class GameScreen(Screen[None]):
    """Displays the active game to the user"""

    BINDINGS = [
        ("escape", "back", "Back to Main Menu"),
        ("s", "save", "Save Game"),
    ]

    active_player: reactive[TokenType] = reactive(TokenType.P1, recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.app.call_after_refresh(self._on_game_state_updated)

    def compose(self) -> ComposeResult:
        yield Header()

        # Player Turn Text
        token_color_name = CellButton.token_color[self.active_player].title()
        self.header_markdown: Markdown = Markdown(f"# Player {self.active_player.value} ({token_color_name}), it's your turn!")
        yield self.header_markdown

        # Board
        yield GameWidget(self._controller)

        yield Footer()

    """Game State Callbacks"""

    @on(TuiGameEvents.GameStateUpdated)
    def _on_game_state_updated(self):
        self.active_player = self._controller.model.active_player

    @on(TuiGameEvents.GameCleared)
    def _on_game_cleared(self):
        self.app.switch_screen(screens.MainMenuScreen(self._controller))

    """Keybindings Actions"""

    def action_back(self) -> None:
        """Returns to the Main Menu screen"""
        self.app.switch_screen(screens.MainMenuScreen(self._controller))

    def action_save(self) -> None:
        """Brings the player to the save game screen"""
        self.app.switch_screen(screens.SaveScreen(self._controller))
