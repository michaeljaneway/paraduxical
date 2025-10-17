from Board import Board
from Player import Player
from enums.GameStatus import GameStatus


class Game:
    def __init__(self) -> None:
        self.board: Board
        self.players: list[Player]
        self.currentTurnIndex: int
        self.status: GameStatus

    def startGame(self) -> None:
        raise NotImplementedError

    def setupBoard(self) -> None:
        raise NotImplementedError

    def switchTurn(self) -> None:
        raise NotImplementedError

    def checkWinCondition(self) -> None:
        raise NotImplementedError
    
    def endGame(self, winner: Player) -> None:
        raise NotImplementedError
