from tkinter import Misc, ttk
from typing import Callable


class MenuOption:
    def __init__(
        self,
        label: str,
        callback: Callable,
        is_visible_lambda: Callable[[], bool] = lambda: True,
        is_enabled_lambda: Callable[[], bool] = lambda: True,
    ) -> None:
        self.label = label
        self.callback = callback
        self._is_visible_lambda = is_visible_lambda
        self._is_enabled_lambda = is_enabled_lambda

    @property
    def is_visible(self):
        return self._is_visible_lambda()

    @property
    def is_enabled(self):
        return self._is_enabled_lambda()


class MenuWidget(ttk.Frame):
    def __init__(self, root: Misc, menu_options: list[MenuOption], **kwargs) -> None:
        super().__init__(root, **kwargs)
        self.menu_options = menu_options
        self.menu_buttons: list[ttk.Button] = []

        for option_index, option in enumerate(self.menu_options):
            option_button = ttk.Button(self, text=option.label, command=option.callback, style="Accent.TButton")
            option_button.grid(column=0, row=option_index, padx=20, pady=5, sticky="nsew")
            self.menu_buttons.append(option_button)

        self.refresh_menu()

    def refresh_menu(self):
        for option_index, option in enumerate(self.menu_options):
            option_button = self.menu_buttons[option_index]

            # Visible / Invisible
            if option.is_visible:
                option_button.grid()
            else:
                option_button.grid_remove()

            # Enabled / Disabled
            if option.is_enabled:
                option_button.configure(state="active")
            else:
                option_button.configure(state="disabled")
