from Coordinate import Coordinate
from enums import TokenType


class TokenLine:
    """A single line of hex coordinates with an associated token type"""

    def __init__(self, type: TokenType, coords: list[Coordinate]) -> None:
        self.token_type: TokenType = type
        self.coords: list[Coordinate] = coords

    def __repr__(self) -> str:
        return f"TL({self.token_type.name}, {self.coords})"

    def __str__(self) -> str:
        return self.__repr__()
