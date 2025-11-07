from textual import on
from textual.app import ComposeResult
from textual.widgets import Label, ListItem, ListView, Markdown
from textual.widget import Widget
from textual.containers import HorizontalGroup, VerticalGroup
from textual.message import Message

from enums.TokenType import TokenType
from enums.Direction import Direction
from enums.MoveType import MoveType

from Move import Move
from GameController import GameController
from Coordinate import Coordinate
from view.widgets.CellButton import CellButton


class BoardWidget(Widget):
    class MoveMade(Message):
        def __init__(self, move: Move) -> None:
            self.move: Move = move
            super().__init__()

    def __init__(self, controller: GameController, **kwargs) -> None:
        super().__init__(**kwargs)
        self.styles.height = "auto"

        self._controller = controller

        self.board_2d = self._controller.get_board_array()
        self.board_dict = self._controller.get_board_dict()
        self.winners = self._controller.get_winning_lines()

        self.move_type: MoveType | None = None
        self.move_direction: Direction = Direction.NoDirection
        self.selected_cells: list[CellButton] = []
        self.cell_buttons: dict[Coordinate, CellButton] = {}

        self.direction_group: ListView = ListView()
        self.direction_group.styles.margin = (1, 1)
        self.direction_group.display = False

        self.move_type_group: ListView = ListView()
        self.move_type_group.styles.margin = (1, 1)
        self.move_type_group.display = False

        self.board_group: VerticalGroup = VerticalGroup()
        self.board_group.styles.margin = (1, 1)

    def compose(self) -> ComposeResult:

        # Instructional Header
        self.header_markdown: Markdown = Markdown("")
        yield self.header_markdown

        # Cell Generation
        with self.board_group:
            for row in self.board_2d:
                with HorizontalGroup(classes="row"):
                    for tile in row:
                        cell_button = CellButton(tile.coord, tile.token, classes="board_cell")
                        self.cell_buttons[tile.coord] = cell_button
                        yield cell_button
        self.deactivate_all_cells()

        # Show winners selected if there are winning lines
        if len(self.winners) > 0:
            for win_line in self.winners:
                for coord in win_line.coords:
                    self.cell_buttons[coord].select()

        # Movement Type List Selection
        with self.move_type_group:
            yield MoveTypeListItem(Label("Swap Tokens"), move_type=MoveType.SWAP)
            yield MoveTypeListItem(Label("Shift Tokens"), move_type=MoveType.SHIFT)

        # Direction Options List Selection
        yield self.direction_group

    """Moving"""

    def start_move(self) -> None:
        self.move_type_group.display = True

    def set_move_type(self, move_type: MoveType) -> None:
        """Instructs the board to begin accepting input for a move, which will be returned async through a posted MoveMade Message"""
        self.move_type = move_type
        self.move_type_group.display = False
        # self.header_markdown.set
        self.activate_player_cells()

    def update_state(self) -> None:
        """Update the options displayed to the user based on the current state of the selected cells"""

        # If the cell is the first to be selected
        if len(self.selected_cells) == 1:
            adjacent_cell_count = self.activate_adjacent_cells()

            # If the selected cell has no valid adjacent pieces, reset and reprompt for first cell
            if adjacent_cell_count == 0:
                self.activate_player_cells()
                self.selected_cells[0].deselect()
                self.selected_cells = []
                self.notify("The selected piece has no valid adjacent tokens, please select another", severity="warning")

        # If the token is the selected to be selected
        elif len(self.selected_cells) == 2:
            if self.move_type == MoveType.SWAP:
                self.post_move()
            else:
                self.deactivate_all_cells()
                self.generate_direction_options()

    def generate_direction_options(self) -> None:
        """Create a list of options based on the valid movement directions for shift move"""
        valid_directions = self._controller.get_valid_shift_directions(self.selected_cells[0].coord, self.selected_cells[1].coord)

        # Handle no valid movement directions for the selected pieces
        if len(valid_directions) == 0:
            self.activate_player_cells()
            self.selected_cells[0].deselect()
            self.selected_cells = []
            self.notify("The selected pieces have no valid direction which they can move in, please select again", severity="warning")

        # Display the selections
        self.direction_group.display = True
        self.direction_group.clear()
        for dir in valid_directions:
            new_item = DirectionListItem(Label(dir.name), direction=dir)
            self.direction_group.append(new_item)

    def post_move(self) -> None:
        """Post a MoveMade message composed from the current movement option selections"""
        if not self.move_type:
            return

        b0 = self.selected_cells[0]
        b1 = self.selected_cells[1]
        move = Move(self.move_type, b0.coord, b1.coord, self.move_direction)
        self.post_message(self.MoveMade(move))

    """Set Header"""

    def set_header_text(self, text: str) -> None:
        pass

    """Cell Activation/Deactivation"""

    def activate_player_cells(self) -> None:
        """Activate all tokens owned by the player"""
        for button in self.cell_buttons.values():
            if button.is_player_token():
                button.disabled = False

    def deactivate_all_cells(self) -> None:
        """Deactivate every cell on the board"""
        for button in self.cell_buttons.values():
            button.disabled = True

    def activate_adjacent_cells(self) -> int:
        """Activates all valid adjacent cells of the currently selected cell"""
        self.deactivate_all_cells()
        c1 = self.selected_cells[0].coord
        c1_token = self.board_dict[c1]

        adjacent_count = 0
        for dir in [Direction.NE, Direction.E, Direction.SE, Direction.SW, Direction.W, Direction.NW]:
            neighbor = c1.neighbor(dir)
            neighbor_token = self.board_dict.get(neighbor)
            if not neighbor_token or c1_token == neighbor_token or neighbor_token not in [TokenType.P1, TokenType.P2]:
                continue

            self.cell_buttons[neighbor].disabled = False
            adjacent_count += 1

        return adjacent_count

    """Callbacks"""

    @on(ListView.Selected)
    def on_list_item_sel(self, event: ListView.Selected) -> None:
        if isinstance(event.item, MoveTypeListItem):
            self.set_move_type(event.item.move_type)
        elif isinstance(event.item, DirectionListItem):
            self.move_direction = event.item.direction
            self.post_move()

    @on(CellButton.Pressed)
    def on_cell_pressed(self, event: CellButton.Pressed) -> None:
        cell = event.button
        if not isinstance(cell, CellButton):
            return

        cell.select()
        self.selected_cells.append(cell)
        self.update_state()


class MoveTypeListItem(ListItem):
    def __init__(self, *children, move_type: MoveType, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.move_type: MoveType = move_type


class DirectionListItem(ListItem):
    def __init__(self, *children, direction: Direction, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.direction: Direction = direction
