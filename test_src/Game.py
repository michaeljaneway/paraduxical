from Board import Board
from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType
from Move import Move
from TokenLine import TokenLine


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

    def play_move(self, move: Move) -> None:
        pass

    def does_winner_exist(self) -> bool:
        return len(self.board.get_token_lines(4)) > 0

    def get_winning_lines(self) -> list[TokenLine]:
        return self.board.get_token_lines(4)


if __name__ == "__main__":
    g = Game(BoardLayout.DIAG)
    print(g.board)
