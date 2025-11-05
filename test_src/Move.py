from enums.MoveType import MoveType
from enums.Direction import Direction
from Coordinate import Coordinate


class Move:
    """A single board move"""

    def __init__(
            self,
            moveType: MoveType,
            c1: Coordinate,
            c2: Coordinate,
            direction: Direction = Direction.NoDirection
        ) -> None:

        self.move_type: MoveType = moveType
        self.token1 = c1
        self.token2 = c2
        self.direction = direction
