from enum import StrEnum


class GameEvent(StrEnum):
    """Event types for WebSockets"""

    GameCreated = "GameCreated"

    GameCleared = "GameCleared"

    GameStateUpdated = "GameStateUpdated"
