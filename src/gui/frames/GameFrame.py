from tkinter import N, S, Misc, ttk
from typing import Callable

from shared.enums.BoardLayout import BoardLayout
from GameClientController import GameClientController


class GameFrame(ttk.Frame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self._controller = controller
