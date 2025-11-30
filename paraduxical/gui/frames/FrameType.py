from enum import IntEnum, auto


class FrameType(IntEnum):
    """All of the different Frames available in the GUI to allow frame switching without circular imports"""

    MainMenu = auto()
    Game = auto()
    NewGame = auto()
    LoadGame = auto()
    SaveGame = auto()
    Rules = auto()
