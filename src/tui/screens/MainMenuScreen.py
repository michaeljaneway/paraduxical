import asyncio
from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.reactive import reactive
from textual.screen import Screen
from textual.events import Mount
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.enums.EventType import GameEvent
from tui import screens


class MainMenuScreen(Screen[None]):
    """Main menu for Paraduxical, allows user to navigate between all available program options"""

    AUTO_FOCUS = "#menu_list"

    is_game_active: reactive[bool] = reactive(False, recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        
        self.app.call_after_refresh(self.update_is_game_active)
        self._controller.bind_callback(GameEvent.GameCreated, self.update_is_game_active)
        self._controller.bind_callback(GameEvent.GameCleared, self.update_is_game_active)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        # Load rules from markdown file
        rules_path = Path("./assets/mainmenu.md")
        rules_content = rules_path.read_text("utf-8")

        with VerticalScroll(classes="container middle"):
            yield Markdown(rules_content)

            with ListView(id="menu_list"):
                if self.is_game_active:
                    yield ListItem(Label("Resume Active Game"), id="resumegame")
                    yield ListItem(Label("Clear Active Game"), id="deletegame")
                yield ListItem(Label("Start New Game"), id="startnewgame")
                yield ListItem(Label("Load Save Game"), id="loadgame")
                yield ListItem(Label("View Rules"), id="viewrules")
                yield ListItem(Label("Exit Game"), id="exitgame")

        yield Footer()

    """Callbacks"""

    def update_is_game_active(self):
        self.is_game_active = self._controller.is_game_active()

    @on(ListView.Selected, item="#resumegame")
    def on_resume_game(self) -> None:
        self.app.push_screen(screens.GameScreen(self._controller))

    @on(ListView.Selected, item="#deletegame")
    def on_delete_game(self) -> None:
        self._controller.clear_game()

    @on(ListView.Selected, item="#startnewgame")
    def on_start_new_game(self) -> None:
        self.app.push_screen(screens.NewGameScreen(self._controller))

    @on(ListView.Selected, item="#loadgame")
    def on_load_save_game(self) -> None:
        self.app.push_screen(screens.LoadScreen(self._controller))

    @on(ListView.Selected, item="#viewrules")
    def on_view_rules(self) -> None:
        self.app.push_screen(screens.RulesScreen(self._controller))

    @on(ListView.Selected, item="#exitgame")
    def on_exit_game(self) -> None:
        self.app.exit()
