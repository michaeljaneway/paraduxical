from tkinter import Misc, messagebox, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.FrameType import FrameType
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.GameEvent import GameEvent


class SaveGameFrame(BaseFrame):
    """Frame to allow saving the game"""
    
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        self._event_callbacks = [
            EventCallback(f"<<{GameEvent.GameSaved}>>", lambda _: self.switch_frame(FrameType.Game)),
            EventCallback(f"<<{GameEvent.GameCleared}>>", lambda _: self.switch_frame(FrameType.MainMenu)),
        ]
        self.bind_event_callbacks()

        # Title
        self.title_label = ttk.Label(self, text=f"Saving Game", justify="center", font=("Arial", 40))
        self.title_label.grid(row=0, column=0, pady=10, sticky="nsew")

        # Show instructions to the user
        self.instruction_label = ttk.Label(self, text=f"Please enter a savefile name:", justify="center")
        self.instruction_label.grid(row=1, column=0, pady=10)

        # Savefile name entry
        self.save_entry = ttk.Entry(self)
        self.save_entry.grid(pady=5, sticky="nsew")

        # Menu buttons
        self.menu_widget = MenuWidget(
            self,
            [
                MenuOption("Save", lambda: self.save()),
                MenuOption("Return without Saving", lambda: self.switch_frame(FrameType.Game)),
            ],
        )
        self.menu_widget.grid()

    def save(self):
        save_name = self.save_entry.get()

        if save_name in self._cache.game_saves:
            messagebox.showerror(f"The savefile '{save_name}' already exists, please delete it or enter another name")
            return

        self._controller.save_game(save_name)
