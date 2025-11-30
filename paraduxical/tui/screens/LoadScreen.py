from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.enums.GameEvent import GameEvent
from tui.events.TuiGameEvents import TuiGameEvents
from tui import screens


class LoadScreen(Screen[None]):
    """Allows the user to load a saved game"""

    BINDINGS = [("escape", "back", "Back to Main Menu")]

    game_saves: reactive[list[str]] = reactive([], recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.app.call_after_refresh(self._on_game_saved)

    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalScroll(classes="container middle"):
            yield Markdown(f"# Load a Game")
            yield Markdown(f"Select to save game to load from the list below:")

            with ListView():
                for save_name in self.game_saves:
                    yield SaveGameListItem(Label(save_name), save_name=save_name)

        yield Footer()

    """Game State Callbacks"""

    @on(TuiGameEvents.GameSaved)
    def _on_game_saved(self):
        self.game_saves = self._controller.model.game_saves

    @on(TuiGameEvents.GameCreated)
    def _on_game_created(self):
        self.app.switch_screen(screens.GameScreen(self._controller))

    """Menu Selection Callbacks"""

    @on(ListView.Selected)
    def on_save_selected(self, event: ListView.Selected) -> None:
        if not isinstance(event.item, SaveGameListItem):
            return
        self._controller.load_game(event.item.save_name)

    """Keybondings Actions"""

    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen(self._controller))


class SaveGameListItem(ListItem):
    def __init__(self, *children, save_name, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.save_name: str = save_name
