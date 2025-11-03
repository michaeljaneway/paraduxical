import sys
from options.Option import Option
from typing import Any
from Session import Session

class ExitProgramOption(Option):
    def __init__(self, session: Session) -> None:
        super().__init__(session)

        self.desc = "Exit Program"

    def is_visible(self) -> bool:
        return True

    def execute(self, results: list[Any]) -> None:
        sys.exit(0)