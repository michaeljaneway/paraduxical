from enums.TokenType import TokenType
from Coordinate import Coordinate


class TokenLine:
    def __init__(self, type: TokenType, coords: list[Coordinate]) -> None:
        self.type: TokenType = type
        self.coords: list[Coordinate] = coords
