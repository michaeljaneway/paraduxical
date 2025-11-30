from tkinter import Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.FrameType import FrameType
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from shared.enums.GameEvent import GameEvent


class MainMenuFrame(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        # Bind callbacks
        self._event_callbacks: list[EventCallback] = [
            EventCallback(f"<<{GameEvent.GameCreated}>>", lambda _: self._on_game_active_change()),
            EventCallback(f"<<{GameEvent.GameCleared}>>", lambda _: self._on_game_active_change()),
        ]
        self.bind_event_callbacks()

        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)

        # Title
        self.title_label = ttk.Label(self, text=f"Paraduxical", font=("Arial", 52))
        self.title_label.grid(row=0, column=0, pady=20, sticky="nsew")

        # Create menu
        menu_options: list[MenuOption] = [
            MenuOption("Resume Game", self._on_resume_game, is_enabled_lambda=lambda: self._cache.is_game_active),
            MenuOption("Clear Active Game", self._on_clear_game, is_enabled_lambda=lambda: self._cache.is_game_active),
            MenuOption("Start New Game", lambda: self.switch_frame(FrameType.NewGame)),
            MenuOption("Load Save Game", self._on_load_game),
            MenuOption("View Rules", self._on_view_rules),
            MenuOption("Exit Game", self._on_quit),
        ]
        self.menu_widget = MenuWidget(self, menu_options)
        self.menu_widget.grid(row=1, column=0)

    """Event Callbacks"""

    def _on_game_active_change(self):
        self.menu_widget.refresh_menu()

    """Menu Actions"""

    def _on_resume_game(self):
        self.switch_frame(FrameType.Game)

    def _on_clear_game(self):
        self._controller.clear_game()

    def _on_load_game(self):
        self.switch_frame(FrameType.LoadGame)

    def _on_view_rules(self):
        self.switch_frame(FrameType.Rules)

    def _on_quit(self):
        self.quit()
