from enum import Enum


class BoardLayout(Enum):
    HORZ = 0
    """The starting middle two pieces are placed horizontally across from each other"""

    DIAG = 1
    """The starting middle two pieces are placed diagonally across from each other"""
