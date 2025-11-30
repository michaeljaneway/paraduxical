from tkinter import Misc, messagebox, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.FrameType import FrameType
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.GameEvent import GameEvent


class SaveGameFrame(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        self._event_callbacks = [
            EventCallback(f"<<{GameEvent.GameSaved}>>", lambda _: self.switch_frame(FrameType.Game)),
            EventCallback(f"<<{GameEvent.GameCleared}>>", lambda _: self.switch_frame(FrameType.MainMenu)),
        ]
        self.bind_event_callbacks()

        # Savefile name entry
        self.save_entry = ttk.Entry(self)
        self.save_entry.grid(pady=5, sticky="nsew")

        # Menu buttons
        self.menu_widget = MenuWidget(
            self,
            [
                MenuOption("Save", lambda: self.save()),
                MenuOption("Return to Main Menu", lambda: self.switch_frame(FrameType.MainMenu)),
            ],
        )
        self.menu_widget.grid()

    def save(self):
        save_name = self.save_entry.get()

        if save_name in self._cache.game_saves:
            messagebox.showerror(f"The savefile '{save_name}' already exists, please delete it or enter another name")
            return

        self._controller.save_game(save_name)
