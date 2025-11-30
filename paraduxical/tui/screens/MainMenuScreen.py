import asyncio
from pathlib import Path

from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.events import Mount
from textual.reactive import reactive
from textual.screen import Screen
from textual.widgets import Footer, Header, Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from tui import screens
from tui.events.TuiGameEvents import TuiGameEvents


class MainMenuScreen(Screen[None]):
    """Main menu for Paraduxical, allows user to navigate between all available program options"""

    AUTO_FOCUS = "#menu_list"

    is_game_active: reactive[bool] = reactive(False, recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.app.call_after_refresh(self.update_is_game_active)

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)

        # Load rules from markdown file
        main_menu_md_path = Path("./assets/mainmenu.md")
        main_menu_md = main_menu_md_path.read_text("utf-8")

        with VerticalScroll(classes="container middle"):
            yield Markdown(main_menu_md)

            with ListView(id="menu_list"):
                if self.is_game_active:
                    yield ListItem(Label("Resume Active Game"), id="resumegame")
                    yield ListItem(Label("Clear Active Game"), id="deletegame")
                yield ListItem(Label("Start New Game"), id="startnewgame")
                yield ListItem(Label("Load Save Game"), id="loadgame")
                yield ListItem(Label("View Rules"), id="viewrules")
                yield ListItem(Label("Exit Game"), id="exitgame")

        yield Footer()

    def update_is_game_active(self):
        """Updates the active game state"""
        self.is_game_active = self._controller.model.is_game_active

    """Game State Callbacks"""

    @on(TuiGameEvents.GameCreated)
    def _on_game_created(self):
        self.update_is_game_active()

    @on(TuiGameEvents.GameCleared)
    def _on_game_cleared(self):
        self.update_is_game_active()

    """Menu Callbacks"""

    @on(ListView.Selected, item="#resumegame")
    def on_resume_game(self) -> None:
        self.app.switch_screen(screens.GameScreen(self._controller))

    @on(ListView.Selected, item="#deletegame")
    def on_delete_game(self) -> None:
        self._controller.clear_game()

    @on(ListView.Selected, item="#startnewgame")
    def on_start_new_game(self) -> None:
        self.app.switch_screen(screens.NewGameScreen(self._controller))

    @on(ListView.Selected, item="#loadgame")
    def on_load_save_game(self) -> None:
        self.app.switch_screen(screens.LoadScreen(self._controller))

    @on(ListView.Selected, item="#viewrules")
    def on_view_rules(self) -> None:
        self.app.switch_screen(screens.RulesScreen(self._controller))

    @on(ListView.Selected, item="#exitgame")
    def on_exit_game(self) -> None:
        self.app.exit()
