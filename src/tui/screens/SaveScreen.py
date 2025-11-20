from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Input, Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.enums import GameEvent


class SaveScreen(Screen[None]):
    """Allows the user to save the active game"""

    BINDINGS = [("escape", "back", "Back to Game")]

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
            yield Markdown(f"# Saving game")
            yield Markdown(f"Enter the desired savefile name in the input box below. Press *Enter* when complete")

            yield Input(placeholder="Savefile Name", restrict=r"^[\w\-. ]+$")

            with ListView():
                yield ListItem(Label("Cancel"), id="cancel")

        yield Footer()

    """Callbacks"""

    def update_save_game_names(self):
        self.save_game_names = self._controller.get_save_games()

    def on_game_loaded(self):
        self.app.pop_screen()

    @on(Input.Submitted)
    def on_save_name_submitted(self, event: Input.Submitted) -> None:
        """Ensure the save doesn't already exist, then save the active game"""
        save_name = event.value
        if save_name in self.save_game_names:
            self.notify(f"The savefile '{save_name}' already exists, please delete it or enter another name", severity="error")
            return

        self._controller.save_game(save_name)
        self.app.pop_screen()

    @on(ListView.Selected, item="#cancel")
    def action_back(self):
        self.app.pop_screen()
