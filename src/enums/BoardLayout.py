from enum import Enum


class BoardLayout(Enum):
    HORZ = 1
    """The starting middle two pieces are placed horizontally across from each other"""

    DIAG = 2
    """The starting middle two pieces are placed diagonally across from each other"""
