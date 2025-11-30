from tkinter import Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.FrameType import FrameType
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.GameEvent import GameEvent


class MainMenuFrame(BaseFrame):
    """Frame containing the main menu"""

    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        # Bind callbacks
        self._event_callbacks: list[EventCallback] = [
            EventCallback(f"<<{GameEvent.GameCreated}>>", lambda _: self._on_game_active_change()),
            EventCallback(f"<<{GameEvent.GameCleared}>>", lambda _: self._on_game_active_change()),
        ]
        self.bind_event_callbacks()

        # Title
        self.title_label = ttk.Label(self, text=f"Paraduxical", font=("Arial", 52))
        self.title_label.grid(row=0, column=0, pady=20, sticky="nsew")

        # Create menu
        menu_options: list[MenuOption] = [
            MenuOption("Resume Game", lambda: self.switch_frame(FrameType.Game), is_enabled_lambda=lambda: self._cache.is_game_active),
            MenuOption("Clear Active Game", lambda: self._controller.clear_game(), is_enabled_lambda=lambda: self._cache.is_game_active),
            MenuOption("Start New Game", lambda: self.switch_frame(FrameType.NewGame)),
            MenuOption("Load Save Game", lambda: self.switch_frame(FrameType.LoadGame)),
            MenuOption("View Rules", lambda: self.switch_frame(FrameType.Rules)),
            MenuOption("Exit Game", lambda: self.quit()),
        ]
        self.menu_widget = MenuWidget(self, menu_options)
        self.menu_widget.grid(row=1, column=0)

    """Event Callbacks"""

    def _on_game_active_change(self):
        self.menu_widget.refresh_menu()
