import tkinter as tk
from tkinter import Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.frames.FrameType import FrameType
from gui.widgets.BoardWidget import BoardWidget
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from gui.widgets.MovementSelectionWidget import MovementSelectionWidget
from shared.enums import GameEvent


class GameFrame(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)

        self._event_callbacks = [
            EventCallback(f"<<{GameEvent.GameStateUpdated}>>", lambda _: self.refresh()),
            EventCallback(f"<<{GameEvent.GameCleared}>>", lambda _: self.switch_frame(FrameType.MainMenu)),
        ]
        self.bind_event_callbacks()

        """Info + Movement"""

        # Info containter
        info_frame = tk.Frame(self)
        info_frame.grid(row=0, column=0, padx=20)

        # Player's turn
        self.player_turn_label = ttk.Label(info_frame, justify="center", font=("Arial", 15))
        self.player_turn_label.grid(row=0, column=0, pady=20)

        self.instruction_label = ttk.Label(info_frame, justify="center", font=("Arial", 10))
        self.instruction_label.grid(row=1, column=0, pady=5)

        # Movement Selection
        self.movement_widget = MovementSelectionWidget(info_frame, self._controller)
        self.movement_widget.configure(borderwidth=5, highlightbackground="gray")
        self.movement_widget.grid(row=2, column=0)

        # Return to main menu button
        self.exit_menu = MenuWidget(
            info_frame,
            [
                MenuOption("Save Game", lambda: self.switch_frame(FrameType.SaveGame), is_visible_lambda=lambda: len(self._cache.winning_lines) == 0),
                MenuOption("Return to Main Menu", lambda: self.switch_frame(FrameType.MainMenu)),
            ],
        )
        self.exit_menu.grid(row=3, column=0)

        """Board"""

        # Game Board
        self.board_widget = BoardWidget(self, self._controller)
        self.board_widget.grid(row=0, column=1)

        self.refresh()

    def refresh(self):
        # Refresh menus
        self.exit_menu.refresh_menu()

        # Update instructions
        if self._cache.is_move_playable:
            self.instruction_label.configure(text="Move can now be played!")
        elif len(self._cache.selected_coords) == 2:
            self.instruction_label.configure(text="Select how to move the 2 tokens")
        else:
            self.instruction_label.configure(text="Select 2 opposite tokens")

        # Inform the players of who's turn it is
        if not self._cache.winning_lines:
            self.player_turn_label.configure(text=f"Player {self._cache.active_player.value}, it's your turn!")
            return

        # Remove movement selection widget as the game is won
        self.movement_widget.grid_remove()
        self.instruction_label.grid_remove()

        # Inform the players of who won the game
        winners = set([line.token_type for line in self._cache.winning_lines])
        if len(winners) == 1:
            self.player_turn_label.configure(text=f"Player {winners.pop().value}, you have won! Congratulations!")
        else:
            self.player_turn_label.configure(text=f"It's a tie! Congratulations to both players!")
