from pathlib import Path
from tkinter import Misc

import markdown
import tkhtmlview

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame
from gui.widgets.MenuWidget import MenuOption, MenuWidget


class RulesFrame(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        from gui.frames.MainMenuFrame import MainMenuFrame

        # Load rules from markdown file
        rules_md = Path("./assets/rules.md").read_text("utf-8")
        rules_html = '<p style="color: white">' + markdown.markdown(rules_md) + "</p>"
        
        print(rules_html)

        # Rules
        self.md_text = tkhtmlview.HTMLScrolledText(self, html=rules_html, background=None)
        self.md_text.configure(bd=0, width=100)
        self.md_text.grid(sticky="nsew")

        # Create menu
        menu_options: list[MenuOption] = [
            MenuOption("Return to Main Menu", lambda: self.switch_frame(MainMenuFrame(self.master, self._controller))),
        ]
        self.menu_widget = MenuWidget(self, menu_options)
        self.menu_widget.grid(pady=20)
