from Board import HexBoard
# from Coordinate import Coordinate
from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType
from Move import Move
from TokenLine import TokenLine

class Game:
    def __init__(self, layout: BoardLayout) -> None:
        horz_layout = [TokenType(x) for x in
                       [1, 2, 1, 2,
                       2, 0, 0, 0, 1,
                       1, 0, 0, 0, 0, 2,
                       2, 0, 1, 0, 2, 0, 1,
                       1, 0, 0, 0, 0, 2,
                       2, 0, 0, 0, 1,
                       1, 2, 1, 2]]

        diag_layout = [TokenType(x) for x in
                       [1, 2, 1, 2,
                       2, 0, 0, 0, 1,
                       1, 0, 0, 1, 0, 2,
                       2, 0, 0, 0, 0, 0, 1,
                       1, 0, 2, 0, 0, 2,
                       2, 0, 0, 0, 1,
                       1, 2, 1, 2]]

        self.layout = layout
        self.board = HexBoard(radius=3)
        self.board.load_from_list(
            horz_layout if layout == BoardLayout.HORZ else diag_layout)

        self.current_player = TokenType.P1
        self.move_history: list[Move] = []

    def does_winner_exist(self) -> bool:
        return len(self.board.get_token_lines(4)) > 0

    def get_winning_lines(self) -> list[TokenLine]:
        return self.board.get_token_lines(4)

    def play_move(self, move: Move) -> None:
        pass


if __name__ == "__main__":
    g = Game(BoardLayout.HORZ)
    print(g.board)
