from enums.MoveType import MoveType
from Board import Board


class Move:
    def __init__(self) -> None:
        self.moveType: MoveType = MoveType.SHIFT
    
    def execute(self, board: Board):
        pass

