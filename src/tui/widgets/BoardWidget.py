from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.widget import Widget

from GameClientController import GameClientController
from shared.Coordinate import Coordinate
from shared.enums import Direction, MoveType
from tui import screens
from tui.widgets.CellButton import CellButton


class BoardWidget(Widget):
    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)

        self._controller = controller

        self.board_2d = self._controller.get_board_array()
        self.board_dict = self._controller.get_board_dict()
        self.selected_coords = self._controller.get_selected_coords()
        self.selectable_coords = self._controller.get_selectable_coords()

        self.move_type: MoveType = self._controller.get_move_type()
        self.move_direction: Direction = self._controller.get_shift_direction()

        self.cell_buttons: dict[Coordinate, CellButton] = {}
        self.styles.height = "auto"

    def compose(self) -> ComposeResult:
        ### Cell Generation
        board_group: VerticalGroup = VerticalGroup()
        board_group.styles.margin = (1, 1)

        with board_group:
            for row in self.board_2d:
                with HorizontalGroup(classes="row"):
                    for tile in row:
                        cell_button = CellButton(tile.coord, tile.token, classes="board_cell")
                        self.cell_buttons[tile.coord] = cell_button

                        if not tile.coord in self.selectable_coords:
                            cell_button.disabled = True

                        if tile.coord in self.selected_coords:
                            cell_button.select()

                        yield cell_button

        # Winning Lines
        self.winners = self._controller.get_winning_lines()
        for win_line in self.winners:
            for coord in win_line.coords:
                self.cell_buttons[coord].select()

    """Callbacks"""

    @on(CellButton.Pressed)
    def on_cell_pressed(self, event: CellButton.Pressed) -> None:
        if not isinstance(event.button, CellButton):
            return
        self._controller.select_coord(event.button.coord)
        self.app.switch_screen(screens.GameScreen(self._controller))
