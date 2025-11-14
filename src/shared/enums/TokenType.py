from enum import Enum


class TokenType(Enum):
    """Token type of any space on the game board"""

    INV = -1
    """Invalid 
    
    Used for coordinates beyond the boundary of the board"""

    MT = 0
    """Empty Space"""

    P1 = 1
    """Player 1 Token"""

    P2 = 2
    """Player 2 Token"""
