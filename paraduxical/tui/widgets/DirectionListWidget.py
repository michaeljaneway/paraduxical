from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.enums import Direction, MoveType
from tui.events.TuiGameEvents import TuiGameEvents


class DirectionListWidget(Widget):
    direction: reactive[Direction] = reactive(Direction.NoDirection, recompose=True)
    valid_directions: reactive[list[Direction]] = reactive([], recompose=True)
    move_type: reactive[MoveType] = reactive(MoveType.NULL, recompose=True)
    selected_piece_count: reactive[int] = reactive(0, recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.styles.height = "auto"
        self.app.call_after_refresh(self._on_game_state_updated)

    def compose(self) -> ComposeResult:
        self.display = self.move_type == MoveType.SHIFT

        # Instructions
        md_text = ""
        if self.selected_piece_count != 2:
            md_text = f"## Please select 2 tokens to select a movement direction"
        elif self.direction.is_valid_direction():
            md_text = f"## You selected {self.direction.name} as the move direction"
        else:
            md_text = f"## Please select a movement direction"
        yield Markdown(md_text)

        if self.selected_piece_count < 2:
            return

        # Shift Direction List
        direction_group: ListView = ListView()
        direction_group.styles.margin = (1, 1)

        with direction_group:
            # Give user option to clear their selection
            if self.direction.is_valid_direction():
                yield DirectionListItem(Label("Clear Shift Direction"), direction=Direction.NoDirection)

            # Display all valid movement directions
            else:
                for dir in self.valid_directions:
                    yield DirectionListItem(Label(dir.name), direction=dir)

            if len(self.valid_directions) == 0:
                self.notify("The selected pieces have no valid direction which they can move in, please select again", severity="warning")

    """Game State Callbacks"""

    @on(TuiGameEvents.GameStateUpdated)
    def _on_game_state_updated(self):
        self.move_type = self._controller.cache.move_type
        self.direction = self._controller.cache.direction
        self.valid_directions = self._controller.cache.valid_shift_directions
        self.selected_piece_count = len(self._controller.cache.selected_coords)

    """Menu Selection Callbacks"""

    @on(ListView.Selected)
    def on_list_item_sel(self, event: ListView.Selected) -> None:
        if not isinstance(event.item, DirectionListItem):
            return
        self._controller.set_shift_direction(event.item.direction)


class DirectionListItem(ListItem):
    """A ListItem which contains a Direction"""

    def __init__(self, *children, direction: Direction, **kwargs) -> None:
        super().__init__(*children, **kwargs)
        self.direction: Direction = direction
