import tkinter as tk
from tkinter import ttk

from gui.MainMenuFrame import MainMenuFrame


class ParaduxGui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Paraduxical")
        
        main_menu = MainMenuFrame(self)
        main_menu.pack()
