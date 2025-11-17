from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from tui import screens


class LoadScreen(Screen[None]):
    """Allows the user to load a saved game"""
    
    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.save_names = self._controller.get_save_games()

    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalScroll(classes="container middle"):
            yield Markdown(f"# Saving game")
            yield Markdown(f"Select to load a save game from the list below:")

            with ListView():
                for save_name in self.save_names:
                    yield SaveGameListItem(Label(save_name), save_name=save_name)

        yield Footer()

    """Callbacks"""

    @on(ListView.Selected)
    def on_save_selected(self, event: ListView.Selected) -> None:
        if not isinstance(event.item, SaveGameListItem):
            return

        self._controller.load_game(event.item.save_name)
        self.app.switch_screen(screens.GameScreen(self._controller))

    """Actions"""

    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen(self._controller))


class SaveGameListItem(ListItem):
    def __init__(self, *children, save_name, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.save_name: str = save_name
