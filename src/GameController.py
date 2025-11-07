import os

from Board import Tile
from Coordinate import Coordinate
from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType
from Game import Game
from Move import Move
from TokenLine import TokenLine


class GameController:
    def __init__(self) -> None:
        self._game: Game | None = None

    """Game Initialization & Destruction"""

    def create_game(self, board_layout: BoardLayout) -> None:
        self._game = Game(board_layout)

    def clear_game(self) -> None:
        self._game = None

    """Game Saving & Loading"""

    def save_game(self, save_name: str) -> None:
        """Create a save with the given name for the active game"""
        if not self._game:
            raise Exception("No game is active")
        
        os.makedirs("saves", exist_ok=True)
        self._game.save_to_file(f"saves/{save_name}")

    def get_save_games(self) -> list[str]:
        """Returns a list of the save games in the 'saves' folder"""
        os.makedirs("saves", exist_ok=True)
        return [os.fsdecode(save_files) for save_files in os.listdir("saves")]

    def load_game(self, save_name: str) -> None:
        """Load a game save from the saves folder"""
        self._game = Game.load_from_file(f"saves/{save_name}")

    """Movement"""

    def play_move(self, move: Move) -> None:
        if not self._game:
            raise Exception("No game is active")
        self._game.play_move(move)

    def get_valid_shift_directions(self, c1: Coordinate, c2: Coordinate):
        if not self._game:
            raise Exception("No game is active")
        return self._game.valid_shift_directions(c1, c2)

    """Game State"""

    def is_game_active(self) -> bool:
        return self._game != None

    def get_active_player(self) -> TokenType:
        if not self._game:
            raise Exception("No game is active")
        return self._game.current_player

    def get_board_array(self) -> list[list[Tile]]:
        if not self._game:
            raise Exception("No game is active")
        return self._game.board.get_2d_coord_list()

    def get_board_dict(self) -> dict[Coordinate, TokenType]:
        if not self._game:
            raise Exception("No game is active")
        return self._game.board.get_board_dict()

    def get_winning_lines(self) -> list[TokenLine]:
        """Returns all lines which meet the requirements to win"""
        if not self._game:
            raise Exception("No game is active")
        return self._game.get_winning_lines()
