from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.enums.GameEvent import GameEvent
from tui import screens


class LoadScreen(Screen[None]):
    """Allows the user to load a saved game"""

    BINDINGS = [("escape", "back", "Back to Main Menu")]

    save_game_names: reactive[list[str]] = reactive([], recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller

        self.app.call_after_refresh(self.update_save_game_names)
        self._controller.bind_callback(GameEvent.GameSaved, self.update_save_game_names)
        self._controller.bind_callback(GameEvent.GameCreated, self.on_game_loaded)

    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalScroll(classes="container middle"):
            yield Markdown(f"# Load a Game")
            yield Markdown(f"Select to save game to load from the list below:")

            with ListView():
                for save_name in self.save_game_names:
                    yield SaveGameListItem(Label(save_name), save_name=save_name)

        yield Footer()

    """Callbacks"""

    def update_save_game_names(self):
        self.save_game_names = self._controller.get_save_games()

    def on_game_loaded(self):
        self.app.pop_screen()
        self.app.push_screen(screens.GameScreen(self._controller))

    @on(ListView.Selected)
    def on_save_selected(self, event: ListView.Selected) -> None:
        if not isinstance(event.item, SaveGameListItem):
            return
        self._controller.load_game(event.item.save_name)

    """Actions"""

    def action_back(self) -> None:
        self.app.pop_screen()


class SaveGameListItem(ListItem):
    def __init__(self, *children, save_name, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.save_name: str = save_name
