from options.Option import Option, OptionField
from Session import Session
from typing import Any
from Move import Move
from enums.TokenType import TokenType
from enums.MoveType import MoveType
from enums.Direction import Direction


class ShiftMoveOption(Option):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

        self.desc = "Shift Pieces"
        self.fields = [
            OptionField(
                "Enter the first piece you would like to shift", r"^[a-z]\d$"),
            OptionField(
                "Enter the second piece you would like to shift", r"^[a-z]\d$"),
            OptionField(
                "Enter the direction you would like to move in:\none of 'ne', 'e', 'se', 'sw', 'w', 'nw'", r"^[ne|e|se|sw|w|nw]$")
        ]

    def is_visible(self) -> bool:
        return self.session.game != None and self.session.game.getWinner() == TokenType.MT

    def execute(self, results: list[Any]) -> None:
        if self.session.game == None:
            raise Exception("No game in progress")

        p1 = self.session.game.coordToPosition((results[0][0], results[0][1]))
        p2 = self.session.game.coordToPosition((results[1][0], results[1][1]))
        direction_map = {
            'ne': Direction.NE,
            'e': Direction.E,
            'se': Direction.SE,
            'sw': Direction.SW,
            'w': Direction.W,
            'nw': Direction.NW,
        }

        shift_move = Move(MoveType.SHIFT, p1, p2, direction_map[results[2]])
        self.session.game.executeMove(shift_move)
