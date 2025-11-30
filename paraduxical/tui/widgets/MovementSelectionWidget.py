from textual import on
from textual.app import ComposeResult
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Label, ListItem, ListView, Markdown

from GameClientController import GameClientController
from shared.enums.GameEvent import GameEvent
from tui.events.TuiGameEvents import TuiGameEvents
from tui.widgets.BoardWidget import BoardWidget
from tui.widgets.DirectionListWidget import DirectionListWidget
from tui.widgets.MovementListWidget import MovementListWidget


class MovementSelectionWidget(Widget):
    """A widget for displaying the Game Board and accepting movement input"""

    is_move_playable: reactive[bool] = reactive(False, recompose=True)

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)
        self._controller = controller
        self.styles.height = "auto"
        self.app.call_after_refresh(self.on_game_state_updated)

    def compose(self) -> ComposeResult:
        if self.is_move_playable:
            yield Markdown("## A move can now be played!")

            play_container = ListView()
            play_container.styles.margin = (1, 1)
            with play_container:
                yield ListItem(Label("Play Move"), id="play")

        # Movement Type
        yield MovementListWidget(self._controller)

        # Shift Move Directions
        yield DirectionListWidget(self._controller)

    """Game State Callbacks"""

    @on(TuiGameEvents.GameStateUpdated)
    def on_game_state_updated(self):
        self.is_move_playable = self._controller.cache.is_move_playable

    """Menu Selection Callbacks"""

    @on(ListView.Selected, item="#play")
    def on_list_item_sel(self) -> None:
        self._controller.play_move()
