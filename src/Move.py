from attr import dataclass
from enums.MoveType import MoveType
from enums.Direction import Direction
from Coordinate import Coordinate


@dataclass
class Move:
    """Represents a single board move"""
    move_type: MoveType
    c1: Coordinate
    c2: Coordinate
    direction: Direction = Direction.NoDirection
