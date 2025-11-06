from pathlib import PurePath
from textual import on
from textual.app import App
from textual.driver import Driver
from textual.events import Mount

from view.screens.MainMenuScreen import MainMenuScreen


class ParaduxApp(App[None]):
    TITLE = "Paraduxical"
    BINDINGS = [("q", "quit_app", "Quit")]

    CSS_PATH = "styles.tcss"

    def __init__(
        self,
        driver_class: type[Driver] | None = None,
        css_path: str | PurePath | list[str | PurePath] | None = None,
        watch_css: bool = False,
        ansi_color: bool = False,
    ):
        super().__init__(driver_class, css_path, watch_css, ansi_color)

    @on(Mount)
    def mount_home_screen(self) -> None:
        self.push_screen(MainMenuScreen())

    def action_quit_app(self) -> None:
        """An action to quit the app."""
        self.exit()


if __name__ == "__main__":
    app = ParaduxApp()
    app.run()
