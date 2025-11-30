from pydantic.dataclasses import dataclass

from shared.Coordinate import Coordinate
from shared.enums import Direction, MoveType


@dataclass(frozen=True)
class Move():
    """A single board move"""

    move_type: MoveType
    c1: Coordinate
    c2: Coordinate
    direction: Direction = Direction.NoDirection
