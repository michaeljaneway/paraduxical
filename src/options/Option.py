from abc import ABC, abstractmethod
from typing import Any
from Session import Session


class OptionField:
    def __init__(self, desc: str, regex: str) -> None:
        self.desc = desc
        self.regex = regex


class Option(ABC):
    def __init__(self, session: Session) -> None:
        self.desc: str = ""
        self.fields: list[OptionField] = []
        self.session = session

    @abstractmethod
    def is_visible(self) -> bool:
        pass

    @abstractmethod
    def execute(self, results: list[Any]) -> None:
        pass
