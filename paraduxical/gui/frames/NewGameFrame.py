from functools import partial
from tkinter import Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.FrameType import FrameType
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.BoardLayout import BoardLayout
from shared.enums.GameEvent import GameEvent


class NewGameFrame(BaseFrame):
    """Frame for initializing a new board with a selected layout"""

    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        # Bind callbacks
        self._event_callbacks = [
            EventCallback(f"<<{GameEvent.GameCreated}>>", lambda _: self.switch_frame(FrameType.Game)),
        ]
        self.bind_event_callbacks()

        # Title
        self.title_label = ttk.Label(self, text=f"New Game", justify="center", font=("Arial", 40))
        self.title_label.grid(row=0, column=0, pady=10, sticky="nsew")

        # Show instructions to the user
        self.instruction_label = ttk.Label(self, text=f"Please select a board layout option:", justify="center")
        self.instruction_label.grid(row=1, column=0, pady=10)

        # Board layout Options
        self.layout_menu = MenuWidget(
            self,
            [
                MenuOption("/ Diagonal Layout /", partial(self._controller.create_game, BoardLayout.DIAG)),
                MenuOption("- Horizontal Layout -", partial(self._controller.create_game, BoardLayout.HORZ)),
            ],
        )
        self.layout_menu.grid(row=2, column=0)

        # Back to main menu
        self.main_menu_selection = MenuWidget(
            self,
            [
                MenuOption("Return to Main Menu", lambda: self.switch_frame(FrameType.MainMenu)),
            ],
        )
        self.main_menu_selection.grid(row=3, column=0, pady=30)
