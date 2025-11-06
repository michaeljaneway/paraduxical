from enums.TokenType import TokenType
from Coordinate import Coordinate


class TokenLine:
    def __init__(self, type: TokenType, coords: list[Coordinate]) -> None:
        self.type: TokenType = type
        self.coords: list[Coordinate] = coords

    def __repr__(self) -> str:
        return f"TL({self.type.name}, {self.coords})"

    def __str__(self) -> str:
        return self.__repr__()
