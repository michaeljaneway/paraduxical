from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType
from Board import Board
from GameView import GameView
from options.Option import ExitGameOption


class GameController:
    def __init__(self) -> None:
        self.gameView = GameView()
        self.menu_options = [ExitGameOption()]

    def mainLoop(self) -> None:
        board = Board(BoardLayout.DIAG)

        while True:
            print(board)
            move = self.gameView.getPlayerMove(board)

            if not board.isValidMove(move):
                print("Invalid move, please try again")
                continue

            board.executeMove(move)

            winner = board.getWinner()
            if winner != TokenType.MT:
                print(board)
                print(f"{winner.name} has won the game!!!")
                break

        print("Exiting....")


