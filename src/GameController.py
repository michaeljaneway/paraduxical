from datetime import datetime
from Game import Game
from enums.BoardLayout import BoardLayout

class GameController:
    def __init__(self) -> None:
        self._game: Game | None = None
        
    def create_game(self, board_layout: BoardLayout) -> None:
        self._game = Game(board_layout)
        
    
