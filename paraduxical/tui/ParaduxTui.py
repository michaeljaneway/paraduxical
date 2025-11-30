from textual import on
from textual.app import App
from textual.dom import DOMNode
from textual.events import Mount
from textual.message import Message

import tui.screens as screens
from GameClientController import GameClientController
from shared.enums.GameEvent import GameEvent
from tui.events.TuiGameEvents import TuiGameEvents


class ParaduxTui(App[None]):
    """Terminal UI frontend application for the Paraduxical game"""

    TITLE = "Paraduxical"
    BINDINGS = [("q", "quit_app", "Quit")]
    CSS_PATH = "styles.tcss"

    def __init__(self, port: int, **kwargs):
        super().__init__(**kwargs)
        self._controller = GameClientController(port)
        self._controller.set_error_callback(lambda message: self.notify(message, severity="error"))
        self._controller.set_event_handler(lambda event: self.app.call_from_thread(self.generate_event, event))

    """Event handling"""

    def generate_event(self, event: GameEvent):
        """Posts the given game event to all nodes"""

        # Create the correct message for the event
        match event:
            case GameEvent.GameCreated:
                message = TuiGameEvents.GameCreated()
            case GameEvent.GameSaved:
                message = TuiGameEvents.GameSaved()
            case GameEvent.GameStateUpdated:
                message = TuiGameEvents.GameStateUpdated()
            case GameEvent.GameCleared:
                message = TuiGameEvents.GameCleared()

        self._propogate_message_down(self, message)

    def _propogate_message_down(self, mp: DOMNode, message: Message) -> None:
        """Posts an event to the given node and its children recursively"""
        mp.post_message(message)
        for child in mp.children:
            self._propogate_message_down(child, message)

    """Callbacks"""

    @on(Mount)
    def mount_home_screen(self) -> None:
        """On mounting the app, immediately switch to the MainMenu screen"""
        self.push_screen(screens.MainMenuScreen(self._controller))

    """Keybindings Actions"""

    def action_quit_app(self) -> None:
        """Quits the app"""
        self._controller.should_websocket_be_active = False
        self.exit()
