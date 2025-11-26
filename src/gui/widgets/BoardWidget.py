import tkinter as tk
from functools import partial
from tkinter import Misc, ttk
from typing import Any

from backend.Board import Cell
from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from shared.Coordinate import Coordinate
from shared.enums.GameEvent import GameEvent
from shared.enums.TokenType import TokenType


class BoardWidget(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)
        self.blank_image = tk.PhotoImage()

        self.button_styles: dict[TokenType, dict[str, Any]] = {
            TokenType.MT: {"bg": "gray", "activebackground": "gray"},
            TokenType.P1: {"bg": "red", "activebackground": "red"},
            TokenType.P2: {"bg": "blue", "activebackground": "blue"},
        }

        self.bind_event_callbacks([EventCallback(f"<<{GameEvent.GameStateUpdated}>>", lambda _: self.refresh_board())])
        self.refresh_board()

    def refresh_board(self):
        for widget in self.winfo_children():
            widget.destroy()

        for row_i, row in enumerate(self._model.board_2d):
            row_frame = ttk.Frame(self)
            row_frame.grid(column=0, row=row_i)

            for tile_i, tile in enumerate(row):
                # Create button
                cell_button = tk.Button(row_frame, image=self.blank_image, command=partial(self._on_cell_pressed, tile.coord))
                cell_button.config(state="disabled", relief="flat", width=30, height=30, **self.button_styles[tile.token])

                # Enable selectable cells
                if tile.coord in self._model.selectable_coords + self._model.selected_coords:
                    cell_button.config(state="active", relief="raised")

                # Select actively selected cells
                if tile.coord in self._model.selected_coords:
                    cell_button.config(relief="groove")

                cell_button.grid(column=tile_i, row=0, padx=3, pady=3, sticky="nsew")

    def _on_cell_pressed(self, coord: Coordinate):
        if coord in self._model.selected_coords:
            self._controller.deselect_coord(coord)
        else:
            self._controller.select_coord(coord)
