from functools import partial
from tkinter import Misc, Widget

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.widgets.DirectionSelectionWidget import DirectionSelectionWidget
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.Direction import Direction
from shared.enums.GameEvent import GameEvent
from shared.enums.MoveType import MoveType


class MovementSelectionWidget(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        self._event_callbacks = [
            EventCallback(f"<<{GameEvent.GameStateUpdated}>>", lambda _: self.refresh_options()),
        ]
        self.bind_event_callbacks()

        # Play move Menu
        play_move_options: list[MenuOption] = [
            MenuOption(
                "Play Move",
                self._controller.play_move,
                is_visible_lambda=lambda: self._model.is_move_playable,
            ),
        ]
        self.play_move_menu = MenuWidget(self, play_move_options)
        self.play_move_menu.grid(row=0, column=0)

        # MoveType Menu
        movetype_options: list[MenuOption] = [
            MenuOption(
                "Swap Tokens",
                partial(self._controller.set_move_type, MoveType.SWAP),
                is_enabled_lambda=lambda: self._model.move_type != MoveType.SWAP,
            ),
            MenuOption(
                "Shift Tokens",
                partial(self._controller.set_move_type, MoveType.SHIFT),
                is_enabled_lambda=lambda: self._model.move_type != MoveType.SHIFT,
            ),
        ]
        self.move_type_menu = MenuWidget(self, movetype_options)
        self.move_type_menu.grid(row=1, column=0)

        # Direction Menu
        self.direction_menu = DirectionSelectionWidget(self, self._controller)
        self.direction_menu.grid(row=2, column=0)

        self.refresh_options()

    def refresh_options(self):
        self.move_type_menu.refresh_menu()
        self.play_move_menu.refresh_menu()

        self.grid_toggle(self.direction_menu, self._model.move_type == MoveType.SHIFT)
        self.grid_toggle(self.play_move_menu, self._model.is_move_playable)

    def grid_toggle(self, widget: Widget, is_visible: bool):
        if is_visible:
            widget.grid()
        else:
            widget.grid_remove()
