from GameClientController import GameClientController
from shared.enums import TokenType
from shared.TokenLine import TokenLine
from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Markdown, ListView, ListItem, Label
from tui import screens
from tui.events.TuiGameEvents import TuiGameEvents
from tui.widgets.BoardWidget import BoardWidget
from tui.widgets.CellButton import CellButton
from tui.widgets.MovementSelectionWidget import MovementSelectionWidget


class GameScreen(Screen[None]):
    """Displays the active game to the user"""

    BINDINGS = [
        ("escape", "back", "Back to Main Menu"),
        ("s", "save", "Save Game"),
    ]

    active_player: reactive[TokenType] = reactive(TokenType.P1, recompose=True)
    winning_lines: reactive[list[TokenLine]] = reactive([], recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.app.call_after_refresh(self._on_game_state_updated)

    def compose(self) -> ComposeResult:
        yield Header()

        # Markdown Header
        header_md = ""

        if not self.winning_lines:
            # Inform the players of who's turn it is
            token_color_name = CellButton.token_color[self.active_player].title()
            header_md = f"Player {self.active_player.value} ({token_color_name}), it's your turn!\n# Select 2 opposite tokens and how you would like to move them!\n# "
        else:
            # Inform the players of who won the game
            winners = set([line.token_type for line in self.winning_lines])
            if len(winners) == 1:
                header_md = f"Player {winners.pop().value}, you have won! Congratulations!"
            else:
                header_md = f"It's a tie! Congratulations to both players!"

        self.header_markdown = Markdown("# " + header_md)
        yield self.header_markdown

        # Hex Board
        yield BoardWidget(self._controller)

        # Movement Selection
        if not self.winning_lines:
            yield MovementSelectionWidget(self._controller)
        else:
            back_container = ListView()
            back_container.styles.margin = (1, 1)
            with back_container:
                yield ListItem(Label("Back to Main Menu"), id="back")

        yield Footer()

    """Game State Callbacks"""

    @on(TuiGameEvents.GameStateUpdated)
    def _on_game_state_updated(self):
        self.active_player = self._controller.cache.active_player
        self.winning_lines = self._controller.cache.winning_lines

    @on(TuiGameEvents.GameCleared)
    def _on_game_cleared(self):
        self.app.switch_screen(screens.MainMenuScreen(self._controller))

    """Keybindings Actions"""

    @on(ListView.Selected, item="#back")
    def action_back(self) -> None:
        """Returns to the Main Menu screen"""
        self.app.switch_screen(screens.MainMenuScreen(self._controller))

    def action_save(self) -> None:
        """Brings the player to the save game screen"""
        self.app.switch_screen(screens.SaveScreen(self._controller))
