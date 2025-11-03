from options.Option import Option
from typing import Any
from Session import Session


class ExitGameOption(Option):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

        self.desc = "Exit Game"

    def is_visible(self) -> bool:
        return self.session.game != None

    def execute(self, results: list[Any]) -> None:
        self.session.game = None
