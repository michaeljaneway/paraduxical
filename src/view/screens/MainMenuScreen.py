from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView, Markdown
from textual.widgets import Header, Footer

from view import screens
from GameController import GameController


class MainMenuScreen(Screen[None]):
    def __init__(self, controller: GameController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller

    def compose(self) -> ComposeResult:
        yield Header()

        # Load rules from markdown file
        rules_path = Path("./assets/mainmenu.md")
        rules_content = rules_path.read_text("utf-8")

        with VerticalScroll(classes="container middle"):
            yield Markdown(rules_content)

            with ListView():
                yield ListItem(Label("🎮 Start New Game 🎮"), id="startnewgame")
                yield ListItem(Label("📂 Load Save Game 📂"), id="loadgame")
                yield ListItem(Label("🔍 View Rules 🔍"), id="viewrules")
                yield ListItem(Label("❌ Exit Game ❌"), id="exitgame")

        yield Footer()

    @on(ListView.Selected, item="#startnewgame")
    def action_start_new_game(self) -> None:
        self.app.switch_screen(screens.NewGameScreen(self._controller))

    @on(ListView.Selected, item="#loadgame")
    def action_load_save_game(self) -> None:
        pass

    @on(ListView.Selected, item="#viewrules")
    def action_view_rules(self) -> None:
        self.app.switch_screen(screens.RulesScreen(self._controller))

    @on(ListView.Selected, item="#exitgame")
    def action_exit_game(self) -> None:
        self.app.exit()
