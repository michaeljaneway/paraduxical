from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, ListItem, ListView

from GameClientController import GameClientController
from shared.enums import MoveType


class MoveTypeListItem(ListItem):
    """A ListItem which contains a MoveType"""

    def __init__(self, *children, move_type: MoveType, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.move_type: MoveType = move_type


class MovementListWidget(Widget):
    move_type: reactive[MoveType] = reactive(MoveType.NULL)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)

        self._controller = controller
        self.move_type = self._controller.get_move_type()

        self.styles.height = "auto"
        self.display = self.move_type == MoveType.NULL

    def compose(self) -> ComposeResult:
        if not self.display:
            return

        # Movement Type
        move_type_group = ListView()
        move_type_group.styles.margin = (1, 1)
        with move_type_group:
            yield MoveTypeListItem(Label("Swap Tokens"), move_type=MoveType.SWAP)
            yield MoveTypeListItem(Label("Shift Tokens"), move_type=MoveType.SHIFT)

    """Callbacks"""

    @on(ListView.Selected)
    def on_list_item_sel(self, event: ListView.Selected) -> None:
        if not isinstance(event.item, MoveTypeListItem):
            return
        self._controller.set_move_type(event.item.move_type)
