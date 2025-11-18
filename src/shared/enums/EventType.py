from enum import StrEnum


class EventType(StrEnum):
    """Event types for WebSockets"""
    
    GameCreated = "GameCreated"
    
    GameCleared = "GameCleared"