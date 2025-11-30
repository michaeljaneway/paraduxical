import tkinter as tk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame
from gui.frames.FrameType import FrameType
from gui.frames.GameFrame import GameFrame
from gui.frames.LoadGameFrame import LoadGameFrame
from gui.frames.MainMenuFrame import MainMenuFrame
from gui.frames.NewGameFrame import NewGameFrame
from gui.frames.RulesFrame import RulesFrame
from gui.frames.SaveGameFrame import SaveGameFrame
from shared.enums.GameEvent import GameEvent


class ParaduxGui(tk.Tk):
    """Graphical UI frontend application for the Paraduxical game"""

    def __init__(self, port: int):
        super().__init__()

        # Set window metadata
        self.title("Paraduxical")
        self.geometry("800x600+100+50")

        # Turn on centering
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Load ttk theme
        # https://github.com/rdbende/Sun-Valley-ttk-theme
        self.call("source", "assets/sun-valley.tcl")
        self.call("set_theme", "dark")

        # Instantiate FastApi controller + event handling
        self._controller = GameClientController(port)
        self._controller.set_event_handler(self.event_generator)
        self._controller.set_error_callback(lambda message: print(message))

        # Instantiate the Main Menu frame
        self.active_frame: BaseFrame | None = None
        self.switch_frame(FrameType.MainMenu)

    def event_generator(self, event: GameEvent):
        """Propogates the given GameEvent to all widgets"""
        self.event_generate(f"<<{event}>>")

    def switch_frame(self, frame: FrameType):
        """Switches the active window frame"""

        if self.active_frame:
            self.active_frame.unbind_event_callbacks()
            self.active_frame.destroy()

        match frame:
            case FrameType.Rules:
                self.active_frame = RulesFrame(self, self._controller)
            case FrameType.SaveGame:
                self.active_frame = SaveGameFrame(self, self._controller)
            case FrameType.LoadGame:
                self.active_frame = LoadGameFrame(self, self._controller)
            case FrameType.NewGame:
                self.active_frame = NewGameFrame(self, self._controller)
            case FrameType.Game:
                self.active_frame = GameFrame(self, self._controller)
            case FrameType.MainMenu | _:
                self.active_frame = MainMenuFrame(self, self._controller)

        self.active_frame.grid()
