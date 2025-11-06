from Board import Board
from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType
from Move import Move
from TokenLine import TokenLine
from enums.MoveType import MoveType


class Game:
    def __init__(self, layout: BoardLayout) -> None:
        layout_map = {
            BoardLayout.HORZ: [
                TokenType(x) for x in [1, 2, 1, 2, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 2, 0, 1, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 2, 1, 2]
            ],
            BoardLayout.DIAG: [
                TokenType(x) for x in [1, 2, 1, 2, 2, 0, 0, 0, 1, 1, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 2, 2, 0, 0, 0, 1, 1, 2, 1, 2]
            ],
        }

        self.layout = layout
        self.board = Board(radius=3)
        self.board.load_from_list(layout_map[self.layout])

        self.current_player = TokenType.P1
        self.move_history: list[Move] = []

    def validate_move(self, move: Move) -> None:
        """Raises an exception with a descriptive message for any issue that invalidates the given move"""

        # Coordinates must be adjacent
        if not (move.c1.distance(move.c2) == 1):
            raise Exception("Tokens 1 & 2 must be opposite ")

        # Get token types
        c1_token = self.board[move.c1]
        c2_token = self.board[move.c2]

        # Both tokens must be a player token
        p_token_types = [TokenType.P1, TokenType.P2]
        if not (c1_token in p_token_types):
            raise Exception("Token 1 is not a valid piece")
        if not (c2_token in p_token_types):
            raise Exception("Token 2 is not a valid piece")

        # Tokens must belong to different players
        if not (c1_token != c2_token):
            raise Exception("Tokens 1 & 2 must belong to opposite players")

        # If the move type is SWAP, we now know this is a valid move
        if move.move_type == MoveType.SWAP:
            return

        # Ensure no pieces are in the way for the SHIFT move, unless it is the other piece involved in the move
        if not (self.board[move.c1.neighbor(move.direction)] == TokenType.MT or move.c1.neighbor(move.direction) == move.c2):
            raise Exception("Tokens 1 is blocked from shifting")
        if not (self.board[move.c2.neighbor(move.direction)] == TokenType.MT or move.c2.neighbor(move.direction) == move.c1):
            raise Exception("Tokens 2 is blocked from shifting")

    def play_move(self, move: Move) -> None:
        # Confirm move is valid
        try:
            self.validate_move(move)
        except Exception as e:
            raise e

        # Execute move
        match move.move_type:
            case MoveType.SWAP:
                c1_token = self.board[move.c1]
                self.board[move.c1] = self.board[move.c2]
                self.board[move.c2] = c1_token

            case MoveType.SHIFT:
                t1_new_coord = move.c1.neighbor(move.direction)
                t2_new_coord = move.c2.neighbor(move.direction)
                t1_token_type = self.board[move.c1]
                t2_token_type = self.board[move.c2]

                self.board[move.c1] = TokenType.MT
                self.board[move.c2] = TokenType.MT
                self.board[t1_new_coord] = t1_token_type
                self.board[t2_new_coord] = t2_token_type

        self.move_history.append(move)
        self.current_player = TokenType.P1 if self.current_player == TokenType.P2 else TokenType.P2

    def get_winning_lines(self) -> list[TokenLine]:
        """Returns all lines which meet the requirements to win"""
        return self.board.get_token_lines(4)
