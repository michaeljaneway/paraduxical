from attr import dataclass

from Coordinate import Coordinate
from enums.Direction import Direction
from enums.MoveType import MoveType


@dataclass
class Move:
    """A single board move"""

    move_type: MoveType
    c1: Coordinate
    c2: Coordinate
    direction: Direction = Direction.NoDirection
