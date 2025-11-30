from enum import IntEnum


class TokenType(IntEnum):
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

    def is_player_token(self):
        return self in (TokenType.P1, TokenType.P2)
