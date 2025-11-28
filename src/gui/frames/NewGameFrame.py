from functools import partial
from tkinter import Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.GameFrame import GameFrame
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.BoardLayout import BoardLayout
from shared.enums.GameEvent import GameEvent


class NewGameFrame(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)
        # from gui.frames.MainMenuFrame import MainMenuFrame

        # Bind callbacks
        self.bind_event_callbacks(
            [
                EventCallback(f"<<{GameEvent.GameCreated}>>", lambda _: self.switch_frame(GameFrame(self.master, self._controller))),
                EventCallback(f"<<{GameEvent.GameCreated}>>", lambda _: print("Hello")),
            ]
        )

        # Show instructions to the user
        instruction_str = f"Please select a board layout option"
        self.instruction_label = ttk.Label(self, text=instruction_str, justify="center")
        self.instruction_label.grid(row=0, column=0, pady=5)

        # Create Menu Options
        menu_options: list[MenuOption] = [
            MenuOption("/ Diagonal Layout /", lambda: self._controller.create_game(BoardLayout.DIAG)),
            MenuOption("- Horizontal Layout -", partial(self._controller.create_game, BoardLayout.HORZ)),
            # MenuOption("Return to Main Menu", lambda: self.switch_frame(MainMenuFrame(self.master, self._controller))),
        ]
        self.menu_widget = MenuWidget(self, menu_options)
        self.menu_widget.grid()
