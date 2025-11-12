from attr import dataclass

from Coordinate import Coordinate
from enums import Direction, MoveType


@dataclass
class Move:
    """A single board move"""

    move_type: MoveType
    c1: Coordinate
    c2: Coordinate
    direction: Direction = Direction.NoDirection
