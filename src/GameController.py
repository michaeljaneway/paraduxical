from GameView import GameView
from Session import Session
from options.Option import Option
from options.ExitProgramOption import ExitProgramOption
from options.StartGameOption import StartGameOption


class GameController:
    def __init__(self) -> None:
        self.session = Session()
        self.gameView = GameView()
        self.options: list[Option] = [
            StartGameOption(self.session),
            ExitProgramOption(self.session)
        ]

    def mainLoop(self) -> None:
        while True:
            self.gameView.update(self.options, self.session)
