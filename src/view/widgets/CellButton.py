from textual.widgets import Button

from Coordinate import Coordinate
from enums.TokenType import TokenType


class CellButton(Button):
    """A button which represents a cell in the UI game board"""

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
        """Returns True if the cell contains a token belonging to a player"""
        return self.token in [TokenType.P1, TokenType.P2]

    def select(self) -> None:
        """Outlines the cell to show it has been selected"""
        self.disabled = True
        self.styles.border = ("outer", "white")

    def deselect(self) -> None:
        """Removes any selection outline on the cell"""
        self.styles.border = ("hidden", "white")
