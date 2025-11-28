from tkinter import Misc, ttk

from GameClientController import GameClientController
from gui.frames.BaseFrame import BaseFrame, EventCallback
from gui.widgets.BoardWidget import BoardWidget
from gui.widgets.MenuWidget import MenuOption, MenuWidget
from gui.widgets.MovementSelectionWidget import MovementSelectionWidget
from shared.enums import GameEvent


class GameFrame(BaseFrame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, controller, **kwargs)
        from gui.frames.MainMenuFrame import MainMenuFrame

        self.bind_event_callbacks(
            [
                EventCallback(f"<<{GameEvent.GameStateUpdated}>>", lambda _: self.refresh()),
                EventCallback(f"<<{GameEvent.GameCleared}>>", lambda _: self.switch_frame(MainMenuFrame(self.master, self._controller))),
            ]
        )

        # Player's turn
        self.player_turn_label = ttk.Label(self, text=f"Player {self._model.active_player.value}, it's your turn!")
        self.player_turn_label.grid(row=0, column=0, pady=20)

        # Game Board
        self.board_widget = BoardWidget(self, self._controller)
        self.board_widget.grid(row=1, column=0)

        # Movement Selection
        self.movement_widget = MovementSelectionWidget(self, self._controller)
        self.movement_widget.configure(borderwidth=5, highlightbackground="gray")
        self.movement_widget.grid(row=1, column=1, pady=20)

        self.exit_menu = MenuWidget(
            self, [MenuOption("Return to Main Menu", lambda: self.switch_frame(MainMenuFrame(self.master, self._controller)))]
        )
        self.exit_menu.grid(row=2, column=0)

    def refresh(self):
        if self._model.winning_lines:
            self.player_turn_label.configure(text=f"Player {self._model.active_player.value}, ")
            self.movement_widget.grid_remove()
        else:
            self.player_turn_label.configure(text=f"Player {self._model.active_player.value}, it's your turn!")
