import tkinter as tk
from tkinter import N, S, ttk
from typing import Callable


class MainMenuFrame(ttk.Frame):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.artLabel = ttk.Label(self, text="Random Art Generator")
        self.artLabel.grid(column=0, row=0, sticky=N)

        menu_options: list[tuple[str, Callable]] = [
            ("Create New Game", lambda: self.select("New Game")),
            ("Load Save Game", lambda: self.select("Load Game")),
            ("Exit Game", lambda: self.select("Exit Game")),
        ]

        for i, option in enumerate(menu_options):
            new_button = ttk.Button(self, text=option[0], command=lambda: option[1](), style="Accent.TButton")
            new_button.grid(column=0, row=i+1, ipady=10, ipadx=20, sticky=S)

    def select(self, selection: str):
        print(selection)
