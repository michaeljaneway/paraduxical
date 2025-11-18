from enum import IntEnum


class Direction(IntEnum):
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

    def is_valid_direction(self) -> bool:
        return self in (Direction.NE, Direction.E, Direction.SE, Direction.SW, Direction.W, Direction.NW)
