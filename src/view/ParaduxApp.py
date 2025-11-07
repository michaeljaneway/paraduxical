from textual import on
from textual.app import App
from textual.events import Mount

from GameController import GameController
from view.screens.MainMenuScreen import MainMenuScreen


class ParaduxApp(App[None]):
    """Application for the Paraduxical game program"""
    
    TITLE = "Paraduxical"
    BINDINGS = [("q", "quit_app", "Quit")]
    CSS_PATH = "styles.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controller = GameController()

    """Callbacks"""

    @on(Mount)
    def mount_home_screen(self) -> None:
        """On mounting the app, immediately switch to the MainMenu screen"""
        self.push_screen(MainMenuScreen(self._controller))

    """Actions"""
    
    def action_quit_app(self) -> None:
        """Action that quits the app."""
        self.exit()
