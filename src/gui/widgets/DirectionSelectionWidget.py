import tkinter as tk
from functools import partial
from tkinter import Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from shared.enums.Direction import Direction
from shared.enums.GameEvent import GameEvent


class DirectionSelectionWidget(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)
        self.blank_image = tk.PhotoImage()
        self.dir_buttons: dict[Direction, tk.Button] = {}

        # Setup callbacks
        self._event_callbacks = [
            EventCallback(f"<<{GameEvent.GameStateUpdated}>>", lambda _: self.refresh_options()),
        ]
        self.bind_event_callbacks()

        self.instruction_label = ttk.Label(self, text=f"Select a direction")
        self.instruction_label.grid(row=0, column=0, pady=5)

        # Create directional buttons
        dir_layout = [[Direction.NW, Direction.NE], [Direction.W, Direction.NoDirection, Direction.E], [Direction.SW, Direction.SE]]
        for row_i, row in enumerate(dir_layout):
            row_frame = ttk.Frame(self)
            row_frame.grid(column=0, row=row_i + 1)

            for dir_i, dir in enumerate(row):
                self.dir_buttons[dir] = tk.Button(
                    row_frame, image=self.blank_image, compound="center", command=partial(self._controller.set_shift_direction, dir)
                )
                self.dir_buttons[dir].config(state="disabled", relief="flat", width=20, height=20, bg="black", fg="white")

                if dir.is_valid_direction():
                    self.dir_buttons[dir].configure(text=dir.name)

                self.dir_buttons[dir].grid(column=dir_i, row=0, padx=3, pady=3, sticky="nsew")

        self.refresh_options()

    def refresh_options(self):
        for dir in self.dir_buttons:
            # Set selectability
            if dir in self._model.valid_shift_directions:
                self.dir_buttons[dir].configure(state="active")
            else:
                self.dir_buttons[dir].configure(state="disabled")

            if dir == self._model.direction and dir.is_valid_direction():
                self.dir_buttons[dir].configure(bg="red")
            else:
                self.dir_buttons[dir].configure(bg="black")
