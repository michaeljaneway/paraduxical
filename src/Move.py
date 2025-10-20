from enums.MoveType import MoveType
from enums.Direction import Direction
from Position import Position


class Move:
    def __init__(self, moveType: MoveType, pos1: Position, pos2: Position, direction: Direction) -> None:
        self.moveType: MoveType = moveType
        self.token1 = pos1
        self.token2 = pos2
        self.direction = direction
