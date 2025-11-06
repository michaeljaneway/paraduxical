from pathlib import Path
from textual import on
from textual.app import ComposeResult
from textual.containers import VerticalScroll
from textual.screen import Screen
from textual.widgets import Label, ListItem, ListView, Markdown
from textual.widgets import Header, Footer, Button
from textual.containers import HorizontalGroup, VerticalGroup

from Game import Game
from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType
from enums.Direction import Direction
from enums.MoveType import MoveType

from Move import Move
from view import screens
from Coordinate import Coordinate
from GameController import GameController


class CellButton(Button):
    token_color: dict[TokenType, str] = {
        TokenType.MT: "gray",
        TokenType.P1: "red",
        TokenType.P2: "blue",
    }

    def __init__(self, coord: Coordinate, token: TokenType, **kwargs):
        super().__init__(**kwargs)
        self.label = ""
        self.coord: Coordinate = coord
        self.token: TokenType = token
        self.disabled = True
        self.styles.background = self.token_color[token]

    def is_player_token(self) -> bool:
        return self.token in [TokenType.P1, TokenType.P2]


class GameScreen(Screen[None]):
    BINDINGS = [("escape", "back", "Back to Main Menu")]

    def __init__(self, controller: GameController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller

        self.move_type: MoveType | None = None
        self.move_direction: Direction = Direction.NoDirection

        self.board_2d = self._controller.get_board_array()
        self.board_dict = self._controller.get_board_dict()

        self.cell_buttons: list[CellButton] = []
        self.selected_cells: list[CellButton] = []

    def compose(self) -> ComposeResult:
        # Board
        yield Header()

        self.header_markdown: Markdown = Markdown()
        yield self.header_markdown

        self.board_group: VerticalGroup = VerticalGroup()
        self.board_group.styles.margin = (1, 1)

        with self.board_group:
            for row in self.board_2d:
                with HorizontalGroup(classes="row"):
                    for tile in row:
                        cell_button = CellButton(tile.coord, tile.token, classes="board_cell")
                        self.cell_buttons.append(cell_button)
                        yield cell_button

        # Options
        self.options_group: ListView = ListView()
        self.options_group.styles.margin = (1, 1)

        with self.options_group:
            yield ListItem(Label("Swap Tokens"), id="swapmove")
            yield ListItem(Label("Shift Tokens"), id="shiftmove")
            yield ListItem(Label("Save Game"), id="savegame")

        yield Footer()

    @on(ListView.Selected, item="#swapmove")
    def action_swap_move(self) -> None:
        self.move_type = MoveType.SWAP
        for button in self.cell_buttons:
            if button.is_player_token():
                button.disabled = False
        self.options_group.visible = False

    @on(CellButton.Pressed)
    def action_cell_pressed(self, event: CellButton.Pressed) -> None:
        cell = event.button
        if not isinstance(cell, CellButton):
            return

        cell.disabled = True
        cell.styles.border = ("outer", "white")
        self.selected_cells.append(cell)

        if len(self.selected_cells) >= 2:
            self.play_move()

    def play_move(self) -> None:
        if not self.move_type:
            raise Exception("No movement type selected")

        b0 = self.selected_cells[0]
        b1 = self.selected_cells[1]

        move = Move(self.move_type, b0.coord, b1.coord, self.move_direction)
        self._controller.play_move(move)

        if len(self._controller.get_winning_lines()) > 0:
            self.app.switch_screen(screens.MainMenuScreen(self._controller))
        else:
            self.app.switch_screen(screens.GameScreen(self._controller))

    def action_back(self) -> None:
        self.app.switch_screen(screens.MainMenuScreen(self._controller))
