from textual import on
from textual.app import App
from textual.events import Mount

from GameController import GameController
from view.screens.MainMenuScreen import MainMenuScreen


class ParaduxApp(App[None]):
    TITLE = "Paraduxical"
    BINDINGS = [("q", "quit_app", "Quit")]
    CSS_PATH = "styles.tcss"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._controller = GameController()

    @on(Mount)
    def mount_home_screen(self) -> None:
        self.push_screen(MainMenuScreen(self._controller))

    def action_quit_app(self) -> None:
        """An action to quit the app."""
        self.exit()


if __name__ == "__main__":
    app = ParaduxApp()
    app.run()
