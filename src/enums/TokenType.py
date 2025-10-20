from enum import Enum


class TokenType(Enum):
    INV = -1
    """Invalid"""
    
    MT = 0
    """Empty Space"""
    
    P1 = 1
    """Player 1 Token"""
    
    P2 = 2
    """Player 2 Token"""
