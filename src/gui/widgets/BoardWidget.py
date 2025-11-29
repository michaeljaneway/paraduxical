import tkinter as tk
from functools import partial
from tkinter import Misc, ttk
from typing import Any

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from shared.Coordinate import Coordinate
from shared.enums.GameEvent import GameEvent
from shared.enums.TokenType import TokenType


class BoardWidget(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)
        self.blank_image = tk.PhotoImage()

        self.active_button_styles: dict[TokenType, dict[str, Any]] = {
            TokenType.MT: {"bg": "gray16", "activebackground": "gray"},
            TokenType.P1: {"bg": "red", "activebackground": "red"},
            TokenType.P2: {"bg": "blue", "activebackground": "blue"},
        }

        self.disabled_button_styles: dict[TokenType, dict[str, Any]] = {
            TokenType.MT: {"bg": "gray16", "activebackground": "gray"},
            TokenType.P1: {"bg": "red4", "activebackground": "red"},
            TokenType.P2: {"bg": "medium blue", "activebackground": "blue"},
        }

        self._event_callbacks = [EventCallback(f"<<{GameEvent.GameStateUpdated}>>", lambda _: self.refresh_board())]
        self.bind_event_callbacks()

        # Build Board
        self.board_dict: dict[Coordinate, tk.Button] = {}
        for row_i, row in enumerate(self._model.board_2d):
            row_frame = ttk.Frame(self)
            row_frame.grid(column=0, row=row_i)

            # Create buttons
            for tile_i, tile in enumerate(row):
                self.board_dict[tile.coord] = tk.Button(row_frame, image=self.blank_image, command=partial(self._on_cell_pressed, tile.coord))
                self.board_dict[tile.coord].configure(width=30, height=30)
                self.board_dict[tile.coord].grid(column=tile_i, row=0, padx=3, pady=3, sticky="nsew")

        self.refresh_board()

    def refresh_board(self):
        # Update individual cells
        for cell_coord, cell_token in self._model.board_dict.items():
            cell_button = self.board_dict[cell_coord]
            cell_button.config(state="disabled", relief="flat", **self.disabled_button_styles[cell_token])

            # Enable selectable cells
            if cell_coord in self._model.selectable_coords + self._model.selected_coords:
                cell_button.config(state="active", relief="raised", **self.active_button_styles[cell_token])

            # Select actively selected cells
            if cell_coord in self._model.selected_coords:
                cell_button.config(relief="groove")

        # We're done if there's winning lines
        if not self._model.winning_lines:
            return

        # Disable all cell buttons if there's winning lines
        for cell_coord, cell_token in self._model.board_dict.items():
            cell_button = self.board_dict[cell_coord]
            cell_button.configure(state="disabled", **self.disabled_button_styles[cell_token])

        # Highlight winning lines
        for line in self._model.winning_lines:
            for coord in line.coords:
                self.board_dict[coord].configure(**self.active_button_styles[line.token_type], relief="groove")

    def _on_cell_pressed(self, coord: Coordinate):
        if coord in self._model.selected_coords:
            self._controller.deselect_coord(coord)
        else:
            self._controller.select_coord(coord)
