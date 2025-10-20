from Token import Token
from Move import Move


class Player:
    def __init__(self, ) -> None:
        self.name: str = ""
        self.color: str = ""
        self.tokens: list[Token] = []

    def selectTokens(self) -> list[Token]:
        return self.tokens

    def makeMove(self, move: Move) -> bool:
        raise NotImplementedError
