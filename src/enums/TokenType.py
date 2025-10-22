from enum import Enum


class TokenType(Enum):
    """Enum representing the token type of a position on the game board"""

    INV = -1
    """Invalid (Used for positions beyond the boundary of the board)"""

    MT = 0
    """Empty Space"""

    P1 = 1
    """Player 1 Token"""

    P2 = 2
    """Player 2 Token"""
