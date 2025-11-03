from abc import ABC, abstractmethod
import sys


# Option todo:
# accept additional values into execute

class Option(ABC):
    def __init__(self) -> None:
        self.description = "Base Option Description"
        self.additional_fields = []
    
    @abstractmethod
    def execute(self):
        pass


class ExitGameOption(Option):
    def __init__(self) -> None:
        self.description = "Exit Game"
    
    def execute(self):
        sys.exit(0)