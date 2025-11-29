from tkinter import Misc, ttk
import tkinter as tk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.widgets.BoardWidget import BoardWidget
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from gui.widgets.MovementSelectionWidget import MovementSelectionWidget
from shared.enums import GameEvent
from gui.frames.FrameType import FrameType


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
        info_frame.grid(row=0, column=0)

        # Player's turn
        self.player_turn_label = ttk.Label(info_frame, text=f"Player {self._model.active_player.value}, it's your turn!", font=("Arial", 15))
        self.player_turn_label.grid(row=0, column=0, pady=20)

        # Movement Selection
        self.movement_widget = MovementSelectionWidget(info_frame, self._controller)
        self.movement_widget.configure(borderwidth=5, highlightbackground="gray")
        self.movement_widget.grid(row=2, column=0)

        # Return to main menu button
        self.exit_menu = MenuWidget(info_frame, [MenuOption("Return to Main Menu", lambda: self.switch_frame(FrameType.MainMenu))])
        self.exit_menu.grid(row=3, column=0)

        """Board"""

        # Game Board
        self.board_widget = BoardWidget(self, self._controller)
        self.board_widget.grid(row=0, column=1)

    def refresh(self):
        # Inform the players of who's turn it is
        if not self._model.winning_lines:
            self.player_turn_label.configure(text=f"Player {self._model.active_player.value}, it's your turn!")
            return

        # Inform the players of who won the game
        winners = set([line.token_type for line in self._model.winning_lines])
        if len(winners) == 1:
            self.player_turn_label.configure(text=f"Player {self._model.active_player.value}, you have won! Congradulations!")
        else:
            self.player_turn_label.configure(text=f"It's a tie! Congradulations to both players!")
