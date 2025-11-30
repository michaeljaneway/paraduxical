from enum import IntEnum, auto

class FrameType(IntEnum):
    MainMenu = auto()
    Game = auto()
    NewGame = auto()
    LoadGame = auto()
    SaveGame = auto()
    Rules = auto()
