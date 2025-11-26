from tkinter import Event, Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.GameFrame import GameFrame
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.BoardLayout import BoardLayout
from shared.enums.GameEvent import GameEvent


class NewGameFrame(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        # Bind callbacks
        event_callbacks: list[EventCallback] = [EventCallback(f"<<{GameEvent.GameCreated}>>", self._on_game_created)]
        self.bind_event_callbacks(event_callbacks)

        # Show instructions to the user
        instruction_str = f"Please select a board layout option"
        self.instruction_label = ttk.Label(self, text=instruction_str, justify="center")
        self.instruction_label.grid(row=0, column=0, pady=5)

        # Create Menu Options
        menu_options: list[MenuOption] = [
            MenuOption("/ Diagonal Layout /", lambda: self._on_select_layout(BoardLayout.DIAG)),
            MenuOption("- Horizontal Layout -", lambda: self._on_select_layout(BoardLayout.HORZ)),
        ]
        self.menu_widget = MenuWidget(self, menu_options)
        self.menu_widget.grid()

    def _on_select_layout(self, layout: BoardLayout):
        self._controller.create_game(layout)

    def _on_game_created(self, event: Event):
        self.switch_frame(GameFrame(self.master, self._controller))
