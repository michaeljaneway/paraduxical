from tkinter import Misc, ttk
from typing import Callable


class MenuOption:
    def __init__(self, label: str, callback: Callable, is_visible_lambda: Callable[[], bool] = lambda: True) -> None:
        self.label = label
        self.callback = callback
        self._is_visible_lambda = is_visible_lambda

    @property
    def is_visible(self):
        return self._is_visible_lambda()


class MenuWidget(ttk.Frame):
    def __init__(self, root: Misc, menu_options: list[MenuOption], **kwargs) -> None:
        super().__init__(root, **kwargs)
        self.menu_options = menu_options
        self.refresh_menu()

    def refresh_menu(self):
        for widget in self.winfo_children():
            widget.destroy()

        option_index = 0
        for option in self.menu_options:
            if not option.is_visible:
                continue

            menu_button = ttk.Button(self, text=option.label, command=option.callback, style="Accent.TButton")
            menu_button.grid(column=0, row=option_index, padx=20, pady=5, sticky="nsew")
            option_index += 1
