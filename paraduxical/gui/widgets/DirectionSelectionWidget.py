import tkinter as tk
from functools import partial
from tkinter import Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from shared.enums.MoveType import MoveType
from shared.enums.Direction import Direction
from shared.enums.GameEvent import GameEvent


class DirectionSelectionWidget(BaseFrame):
    """Compass-shaped menu allowing selection of the SHIFT movement direction"""

    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)
        self.blank_image = tk.PhotoImage()
        self.dir_buttons: dict[Direction, tk.Button] = {}

        # Setup callbacks
        self._event_callbacks = [
            EventCallback(f"<<{GameEvent.GameStateUpdated}>>", lambda _: self.refresh()),
        ]
        self.bind_event_callbacks()

        self.instruction_label = ttk.Label(self)
        self.instruction_label.grid(row=0, column=0, pady=5)

        # Create directional buttons
        dir_layout = [[Direction.NW, Direction.NE], [Direction.W, Direction.NoDirection, Direction.E], [Direction.SW, Direction.SE]]
        for row_i, row in enumerate(dir_layout):
            row_frame = ttk.Frame(self)
            row_frame.grid(column=0, row=row_i + 1)

            for dir_i, dir in enumerate(row):
                self.dir_buttons[dir] = tk.Button(
                    row_frame, image=self.blank_image, compound="center", command=partial(self.set_shift_direction, dir)
                )
                self.dir_buttons[dir].config(state="disabled", relief="flat", width=20, height=20, activebackground="black", bg="black", fg="white")

                if dir.is_valid_direction():
                    self.dir_buttons[dir].configure(text=dir.name)

                self.dir_buttons[dir].grid(column=dir_i, row=0, padx=3, pady=3, sticky="nsew")

        self.refresh()

    def set_shift_direction(self, dir: Direction):
        """Allow toggling the shift direction to match the token selection"""
        if self._cache.direction == dir:
            self._controller.set_shift_direction(Direction.NoDirection)
        else:
            self._controller.set_shift_direction(dir)

    def refresh(self):
        # Update instructional labels
        if self._cache.direction.is_valid_direction():
            self.instruction_label.configure(text=f"Selected [{self._cache.direction.name}] as the shift direction")
        else:
            self.instruction_label.configure(text=f"Select a direction")

        # Update all the direction buttons
        for dir in self.dir_buttons:
            # Set selectability
            if dir in self._cache.valid_shift_directions and self._cache.move_type == MoveType.SHIFT:
                self.dir_buttons[dir].configure(state="active")
            else:
                self.dir_buttons[dir].configure(state="disabled")

            # Highlight active selection
            if dir == self._cache.direction and dir.is_valid_direction():
                self.dir_buttons[dir].configure(activebackground="red", bg="red")
            else:
                self.dir_buttons[dir].configure(activebackground="black", bg="black")
