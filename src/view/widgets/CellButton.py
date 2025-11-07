from textual.widgets import Button
from enums.TokenType import TokenType

from Coordinate import Coordinate


class CellButton(Button):
    token_color: dict[TokenType, str] = {
        TokenType.MT: "gray",
        TokenType.P1: "red",
        TokenType.P2: "blue",
    }

    def __init__(self, coord: Coordinate, token: TokenType, **kwargs):
        super().__init__(**kwargs)
        self.label = ""
        self.coord: Coordinate = coord
        self.token: TokenType = token
        self.styles.background = self.token_color[token]

    def is_player_token(self) -> bool:
        return self.token in [TokenType.P1, TokenType.P2]

    def select(self) -> None:
        self.disabled = True
        self.styles.border = ("outer", "white")

    def deselect(self) -> None:
        self.styles.border = ("hidden", "white")
