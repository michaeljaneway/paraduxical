from abc import ABC, abstractmethod
from typing import Any
from Session import Session


class Option(ABC):
    def __init__(self, session: Session) -> None:
        self.desc: str = ""
        self.fields: list[tuple[str, str]] = []
        self.session = session

    @abstractmethod
    def is_visible(self) -> bool:
        pass

    @abstractmethod
    def execute(self, results: list[Any]) -> None:
        pass





