from textual import on
from textual.app import ComposeResult
from textual.containers import HorizontalGroup, VerticalGroup
from textual.message import Message
from textual.widget import Widget
from textual.widgets import Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.Coordinate import Coordinate
from shared.enums import Direction, MoveType, TokenType
from shared.Move import Move
from tui.widgets.CellButton import CellButton


class DirectionListItem(ListItem):
    """A ListItem which contains a Direction"""

    def __init__(self, *children, direction: Direction, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.direction: Direction = direction


class DirectionListWidget(Widget):
    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)

        self._controller = controller

        self.move_type: MoveType = self._controller.get_move_type()
        self.move_direction: Direction = self._controller.get_shift_direction()

        self.styles.height = "auto"
        self.display = self.move_type == MoveType.SHIFT and self.move_direction == Direction.NoDirection

    def compose(self) -> ComposeResult:
        if not self.display:
            return
        
        # Shift Move Directions
        direction_group: ListView = ListView()
        direction_group.styles.margin = (1, 1)

        valid_directions = self._controller.get_valid_shift_directions()
        with direction_group:
            for dir in valid_directions:
                yield DirectionListItem(Label(dir.name), direction=dir)

            if len(valid_directions) == 0:
                self.notify("The selected pieces have no valid direction which they can move in, please select again", severity="warning")
                self._controller.deselect_coord()

    """Callbacks"""

    @on(ListView.Selected)
    def on_list_item_sel(self, event: ListView.Selected) -> None:
        if not isinstance(event.item, DirectionListItem):
            return
        self._controller.set_shift_direction(event.item.direction)
