from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.enums import GameEvent, MoveType
from tui.events.TuiGameEvents import TuiGameEvents


class MovementListWidget(Widget):
    move_type: reactive[MoveType] = reactive(MoveType.NULL, recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.styles.height = "auto"
        self.app.call_after_refresh(self._on_game_state_updated)

    def compose(self) -> ComposeResult:
        # Instructions
        md_text = ""
        if self.move_type.is_valid_movetype():
            md_text = f"## You selected the {self.move_type} move type"
        else:
            md_text = f"## Please select a move type"
        yield Markdown(md_text)

        # Movement Type Selection
        move_type_group = ListView()
        move_type_group.styles.margin = (1, 1)
        with move_type_group:
            if not self.move_type.is_valid_movetype():
                yield MoveTypeListItem(Label("Swap Tokens"), move_type=MoveType.SWAP)
                yield MoveTypeListItem(Label("Shift Tokens"), move_type=MoveType.SHIFT)
            else:
                yield MoveTypeListItem(Label("Clear Movement Type"), move_type=MoveType.NULL)

    """Game State Callbacks"""

    @on(TuiGameEvents.GameStateUpdated)
    def _on_game_state_updated(self):
        self.move_type = self._controller.model.move_type

    """Menu Selection Callbacks"""

    @on(ListView.Selected)
    def on_list_item_sel(self, event: ListView.Selected) -> None:
        if not isinstance(event.item, MoveTypeListItem):
            return
        self._controller.set_move_type(event.item.move_type)


class MoveTypeListItem(ListItem):
    """A ListItem which contains a MoveType"""

    def __init__(self, *children, move_type: MoveType, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.move_type: MoveType = move_type
