from enum import Enum


class GameStatus(Enum):
    """Enum representing all possible game statuses"""

    NOT_STARTED = 0
    """The game has not begun"""
    
    IN_PROGRESS = 1
    """The game is in progress"""
    
    FINISHED = 2
    """The game is over"""
