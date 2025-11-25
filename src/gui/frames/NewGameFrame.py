from tkinter import Event, Misc, N, S, ttk
from typing import Callable

from GameClientController import GameClientController
from gui.frames.GameFrame import GameFrame
from shared.enums.BoardLayout import BoardLayout
from shared.enums.GameEvent import GameEvent


class NewGameFrame(ttk.Frame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self._controller = controller

        self.bind(f"<<{GameEvent.GameCreated}>>", self._on_game_created)

        # Create Menu Options

        menu_options: list[tuple[str, Callable]] = [
            ("/ Diagonal Layout /", lambda: self._on_select_layout(BoardLayout.DIAG)),
            ("- Horizontal Layout -", lambda: self._on_select_layout(BoardLayout.HORZ)),
        ]

        for i, option in enumerate(menu_options):
            menu_button = ttk.Button(self, text=option[0], command=lambda: option[1](), style="Accent.TButton")
            menu_button.grid(column=0, row=i + 1, ipady=10, ipadx=20, sticky=S)

    def _on_select_layout(self, layout: BoardLayout):
        self._controller.create_game(layout)

    def _on_game_created(self, event: Event):

        print("HELLO EGGS")
        game_frame = GameFrame(self.master, self._controller)
        game_frame.grid(row=0, column=0, sticky="nsew")
        game_frame.tkraise()
