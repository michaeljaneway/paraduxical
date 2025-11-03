from options.Option import Option, OptionField
from Board import Board
from Session import Session
from enums.BoardLayout import BoardLayout
from typing import Any


class StartGameOption(Option):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

        self.desc = "Start New Game"
        self.fields = [
            OptionField(
                "Enter 'h' for Horizontal Layout, 'd' for Diagonal Layout", r"^[h|d]$")
        ]

    def is_visible(self) -> bool:
        return self.session.game == None

    def execute(self, results: list[Any]) -> None:
        match results[0]:
            case 'h':
                self.session.game = Board(BoardLayout.HORZ)
            case 'd':
                self.session.game = Board(BoardLayout.DIAG)
            case _:
                pass
