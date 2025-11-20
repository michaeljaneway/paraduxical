from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.reactive import reactive
from textual.widget import Widget

from backend.Board import Cell
from GameClientController import GameClientController
from shared.Coordinate import Coordinate
from shared.enums import GameEvent, TokenType
from tui.widgets.CellButton import CellButton


class BoardWidget(Widget):
    board_2d: reactive[list[list[Cell]]] = reactive([], recompose=True)
    board_dict: reactive[dict[Coordinate, TokenType]] = reactive({}, recompose=True)
    selected_coords: reactive[list[Coordinate]] = reactive([], recompose=True)
    selectable_coords: reactive[list[Coordinate]] = reactive([], recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.styles.height = "auto"
        self.cell_buttons: dict[Coordinate, CellButton] = {}

        self.app.call_after_refresh(self.on_game_state_updated)
        self._controller.bind_callback(GameEvent.GameStateUpdated, self.on_game_state_updated)

    def compose(self) -> ComposeResult:
        # Cell Generation
        board_group: VerticalGroup = VerticalGroup()
        board_group.styles.margin = (1, 1)

        with board_group:
            for row in self.board_2d:
                with HorizontalGroup(classes="row"):
                    for tile in row:
                        cell_button = CellButton(tile.coord, tile.token, classes="board_cell")
                        self.cell_buttons[tile.coord] = cell_button

                        # Disable non-selectable cells
                        if not tile.coord in self.selectable_coords + self.selected_coords:
                            cell_button.disabled = True

                        # Select actively selected cells
                        if tile.coord in self.selected_coords:
                            cell_button.select()

                        yield cell_button

        # Winning Lines
        self.winners = self._controller.get_winning_lines()
        for win_line in self.winners:
            for coord in win_line.coords:
                self.cell_buttons[coord].select()

    """Callbacks"""

    def on_game_state_updated(self):
        self.board_2d = self._controller.get_board_array()
        self.board_dict = self._controller.get_board_dict()
        self.selected_coords = self._controller.get_selected_coords()
        self.selectable_coords = self._controller.get_selectable_coords()

    @on(CellButton.Pressed)
    def on_cell_pressed(self, event: CellButton.Pressed) -> None:
        if not isinstance(event.button, CellButton):
            return

        c = event.button.coord
        if c in self.selected_coords:
            self._controller.deselect_coord(event.button.coord)
        else:
            self._controller.select_coord(event.button.coord)
