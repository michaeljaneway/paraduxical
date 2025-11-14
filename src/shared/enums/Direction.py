from enum import Enum


class Direction(Enum):
    """Valid directions leading from a tile on a Paradux board"""

    NoDirection = -1
    """No direction"""

    NE = 0
    """North East"""

    E = 1
    """East"""

    SE = 2
    """South East"""

    SW = 3
    """South West"""

    W = 4
    """West"""

    NW = 5
    """North West"""
