from enum import IntEnum


class BoardLayout(IntEnum):
    """Starting Paradux board layouts"""

    HORZ = 1
    """The center two pieces are placed horizontally across from each other"""

    DIAG = 2
    """The center two pieces are placed diagonally across from each other"""
