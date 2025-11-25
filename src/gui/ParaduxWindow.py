import tkinter as tk

from gui.frames.MainMenuFrame import MainMenuFrame
from shared.enums.GameEvent import GameEvent
from GameClientController import GameClientController


class ParaduxGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paraduxical")
        
        self._controller = GameClientController(self.on_err)
        self._controller.set_event_handler(self.event_handler)

        # Load ttk theme
        # https://github.com/rdbende/Sun-Valley-ttk-theme
        self.call("source", "assets/sun-valley.tcl")
        self.call("set_theme", "dark")

        # Instantiate the Main Menu
        main_menu = MainMenuFrame(self, self._controller)
        main_menu.grid()

    def event_handler(self, event: GameEvent):
        self.event_generate(f"<<{event}>>")

    def on_err(self, message: str):
        print(message)