from enum import StrEnum


class GameEvent(StrEnum):
    """Event types for WebSockets"""

    GameCreated = "GameCreated"

    GameSaved = "GameSaved"
    
    GameCleared = "GameCleared"

    GameStateUpdated = "GameStateUpdated"
