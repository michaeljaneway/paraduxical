from Move import Move
from Token import Token


class Board:
    def __init__(self) -> None:
        self.grid: list[list[Token]] = []
        self.lastMove: Move

    def placeInitialTokens(self) -> None:
        raise NotImplementedError

    def updateBoard(self, move: Move) -> None:
        raise NotImplementedError

    def isValidMove(self, move: Move) -> None:
        raise NotImplementedError
