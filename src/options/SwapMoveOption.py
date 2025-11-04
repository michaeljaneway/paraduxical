from options.Option import Option, OptionField
from Session import Session
from typing import Any
from Move import Move

from enums.TokenType import TokenType
from enums.MoveType import MoveType


class SwapMoveOption(Option):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

        self.desc = "Swap Pieces"
        self.fields = [
            OptionField(
                "Enter the first piece you would like to swap", r"^[a-z]\d$"),
            OptionField(
                "Enter the second piece you would like to swap", r"^[a-z]\d$")
        ]

    def is_visible(self) -> bool:
        return self.session.game != None and self.session.game.getWinner() == TokenType.MT

    def execute(self, results: list[Any]) -> None:
        if self.session.game == None:
            raise Exception("No game in progress")

        p1 = self.session.game.coordToPosition((results[0][0], results[0][1]))
        p2 = self.session.game.coordToPosition((results[1][0], results[1][1]))

        swap_move = Move(MoveType.SWAP, p1, p2)
        self.session.game.executeMove(swap_move)
