from shared.enums import BoardLayout
from textual import on
from textual.app import ComposeResult
from textual.containers import Container, VerticalScroll
from textual.screen import Screen
from textual.widgets import (Digits, Footer, Header, Label, ListItem, ListView,
                             Markdown)
from tui import screens
from tui.widgets.GameWidget import GameWidget

from GameClientController import GameClientController


class WinScreen(Screen[BoardLayout]):
    """Shows the winner of the active game"""

    AUTO_FOCUS = "#menu_list"

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller

        self.winning_lines = self._controller.get_winning_lines()
        self.winners = list(set([line.token_type for line in self.winning_lines]))

    def compose(self) -> ComposeResult:
        yield Header()

        with VerticalScroll():
            if len(self.winners) == 1:
                yield Markdown(f"# Congratulations to Player")
                with Container():
                    yield Digits(f"{self.winners[0].value}")
                yield Markdown(f"# for winning the game!")

            else:
                yield Markdown(f"# Congratulations to Players")
                with Container():
                    yield Digits(f"1 + 2")
                yield Markdown(f"# Its a Tie!")

            yield GameWidget(self._controller)

            with ListView(id="menu_list"):
                yield ListItem(Label("Back to Main Menu"), id="back")

        yield Footer()

    @on(ListView.Selected, item="#back")
    def action_diagonal_selected(self) -> None:
        self._controller.clear_game()
        self.action_back()

    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen(self._controller))
