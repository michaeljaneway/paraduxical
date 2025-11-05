from GameView import GameView
from Session import Session
from options.Option import Option
from options.ExitProgramOption import ExitProgramOption
from options.StartGameOption import StartGameOption
from options.ExitGameOption import ExitGameOption
from options.SwapMoveOption import SwapMoveOption
from options.ShiftMoveOption import ShiftMoveOption


class GameController:
    def __init__(self) -> None:
        self.session = Session()
        self.gameView = GameView(self.session)
        self.options: list[Option] = [
            StartGameOption(self.session),
            SwapMoveOption(self.session),
            ShiftMoveOption(self.session),
            ExitGameOption(self.session),
            ExitProgramOption(self.session),
        ]

    def mainLoop(self) -> None:
        while True:
            self.gameView.update(self.options)
