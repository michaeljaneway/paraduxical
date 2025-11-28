from functools import partial
from tkinter import Misc

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.GameFrame import GameFrame
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.GameEvent import GameEvent


class LoadGameFrame(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        # Bind callbacks
        event_callbacks: list[EventCallback] = [
            EventCallback(f"<<{GameEvent.GameSaved}>>", self.refresh),
            EventCallback(f"<<{GameEvent.GameCreated}>>", lambda _: self.switch_frame(GameFrame(self.master, self._controller))),
        ]
        self.bind_event_callbacks(event_callbacks)

        self.refresh()

    def refresh(self):
        from gui.frames.MainMenuFrame import MainMenuFrame

        for widget in self.winfo_children():
            widget.destroy()

        menu_options: list[MenuOption] = [MenuOption(f"{save}", partial(self._controller.load_game, save)) for save in self._model.game_saves]
        menu_options.append(MenuOption("Return to Main Menu", lambda: self.switch_frame(MainMenuFrame(self.master, self._controller))))
        self.menu_widget = MenuWidget(self, menu_options)
        self.menu_widget.grid()
