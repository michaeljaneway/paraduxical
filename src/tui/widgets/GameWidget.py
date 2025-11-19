from textual.app import ComposeResult
from textual.widget import Widget

from GameClientController import GameClientController
from tui.widgets.BoardWidget import BoardWidget
from tui.widgets.DirectionListWidget import DirectionListWidget
from tui.widgets.MovementListWidget import MovementListWidget


class GameWidget(Widget):
    """A widget for displaying the Game Board and accepting movement input"""

    def __init__(self, controller: GameClientController, **kwargs) -> None:
        super().__init__(**kwargs)

        self.styles.height = "auto"
        self._controller = controller

    def compose(self) -> ComposeResult:
        # Hex Board
        yield BoardWidget(self._controller)

        # Movement Type
        yield MovementListWidget(self._controller)

        # Shift Move Directions
        yield DirectionListWidget(self._controller)
