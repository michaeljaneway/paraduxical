from tkinter import Misc, N, S, ttk
from typing import Callable

from GameClientController import GameClientController
from gui.frames.NewGameFrame import NewGameFrame


class MainMenuFrame(ttk.Frame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self._controller = controller

        menu_options: list[tuple[str, Callable]] = [
            ("Start New Game", self._on_start_new_game),
            ("Load Save Game", self._on_load_game),
            ("View Rules", self._on_view_rules),
            ("Exit Game", self.quit),
        ]

        for i, option in enumerate(menu_options):
            menu_button = ttk.Button(self, text=option[0], command=option[1], style="Accent.TButton")
            menu_button.grid(column=0, row=i + 1, ipady=10, ipadx=20, sticky=S)

    def _on_start_new_game(self):
        new_game_frame = NewGameFrame(self.master, self._controller)
        new_game_frame.grid(row=0, column=0, sticky="nsew")
        new_game_frame.tkraise()

    def _on_load_game(self):
        pass

    def _on_view_rules(self):
        print("HELp")
        pass
