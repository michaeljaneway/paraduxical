import tkinter as tk

from GameClientController import GameClientController
from gui.frames.MainMenuFrame import MainMenuFrame
from shared.enums.GameEvent import GameEvent


class ParaduxGui(tk.Tk):
    def __init__(self):
        super().__init__()

        # Set window metadata
        self.title("Paraduxical")
        self.geometry("800x600+100+50")
        # self.rowconfigure(0, weight=1)
        # self.columnconfigure(0, weight=1)

        # Load ttk theme
        # https://github.com/rdbende/Sun-Valley-ttk-theme
        self.call("source", "assets/sun-valley.tcl")
        self.call("set_theme", "dark")

        # Instantiate FastApi controller + event handling
        self._controller = GameClientController(self.on_err)
        self._controller.set_event_handler(self.event_generator)

        # Instantiate the Main Menu frame
        main_menu = MainMenuFrame(self, self._controller)
        main_menu.grid()

    def event_generator(self, event: GameEvent):
        print("BINDCHECK", self.bind())
        self.event_generate(f"<<{event}>>")

    def on_err(self, message: str):
        print(message)
        
    def unbind(self, sequence: str, funcid: str | None = None) -> None:
        print("CRAZY DEBUG UNBIND: ", sequence, funcid)
        return super().unbind(sequence, funcid)
