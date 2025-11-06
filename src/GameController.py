from Coordinate import Coordinate
from Game import Game
from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType
from Board import Tile
from Move import Move
from TokenLine import TokenLine


class GameController:
    def __init__(self) -> None:
        self._game: Game | None = None

    def create_game(self, board_layout: BoardLayout) -> None:
        self._game = Game(board_layout)

    def clear_game(self) -> None:
        self._game = None

    def is_game_active(self) -> bool:
        return self._game != None

    def play_move(self, move: Move) -> None:
        if not self._game:
            raise Exception("No game is active")
        self._game.play_move(move)

    def get_board_array(self) -> list[list[Tile]]:
        if not self._game:
            raise Exception("No game is active")
        return self._game.board.get_2d_coord_list()

    def get_board_dict(self) -> dict[Coordinate, TokenType]:
        if not self._game:
            raise Exception("No game is active")
        return self._game.board.get_board_dict()

    def get_active_player(self) -> TokenType:
        if not self._game:
            raise Exception("No game is active")
        return self._game.current_player

    def get_winning_lines(self) -> list[TokenLine]:
        """Returns all lines which meet the requirements to win"""
        if not self._game:
            raise Exception("No game is active")
        return self._game.get_winning_lines()