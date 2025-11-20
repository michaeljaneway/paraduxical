from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.enums import BoardLayout
from shared.enums.GameEvent import GameEvent
from tui import screens


class NewGameScreen(Screen[BoardLayout]):
    """Allows the user to select the initial board layout before beginning a new game"""

    AUTO_FOCUS = "#menu_list"
    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self._controller.bind_callback(GameEvent.GameCreated, self.on_game_start)

    def compose(self) -> ComposeResult:
        yield Header()

        # Load rules from markdown file
        rules_path = Path("./assets/newgame.md")
        rules_content = rules_path.read_text("utf-8")

        with VerticalScroll():
            yield Markdown(rules_content)
            with ListView(id="menu_list"):
                yield ListItem(Label("/ Diagonal Layout /"), id="diag")
                yield ListItem(Label("— Horizontal Layout —"), id="horz")

        yield Footer()

    @on(ListView.Selected, item="#diag")
    def action_diagonal_selected(self) -> None:
        self.create_game(BoardLayout.DIAG)

    @on(ListView.Selected, item="#horz")
    def action_horizontal_selected(self) -> None:
        self.create_game(BoardLayout.HORZ)

    def create_game(self, board_type: BoardLayout) -> None:
        self._controller.create_game(board_type)

    def on_game_start(self):
        self.app.pop_screen()
        self.app.push_screen(screens.GameScreen(self._controller))

    def action_back(self) -> None:
        self.app.pop_screen()
