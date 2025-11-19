from textual import on
from textual.app import App
from textual.events import Mount

import tui.screens as screens
from GameClientController import GameClientController
from shared.enums.EventType import GameEvent


class ParaduxTui(App[None]):
    """Application for the Paraduxical game program"""

    TITLE = "Paraduxical"
    BINDINGS = [("q", "quit_app", "Quit")]
    CSS_PATH = "styles.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controller = GameClientController(self.on_err)
        self._controller.callback_wrapper = self.call_from_thread

    """Callbacks"""

    @on(Mount)
    def mount_home_screen(self) -> None:
        """On mounting the app, immediately switch to the MainMenu screen"""
        self.push_screen(screens.MainMenuScreen(self._controller))

    def on_err(self, message) -> None:
        self.notify(message, severity="error")

    """Actions"""

    def action_quit_app(self) -> None:
        """Action that quits the app."""
        self._controller.should_websocket_be_active = False
        self.exit()
