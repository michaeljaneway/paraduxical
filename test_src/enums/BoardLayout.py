from enum import Enum


class BoardLayout(Enum):
    """Enum representing the possible starting Paradux board layouts"""
    
    HORZ = 0
    """The center two pieces are placed horizontally across from each other"""

    DIAG = 1
    """The center two pieces are placed diagonally across from each other"""
