from textual.message import Message


class TuiGameEvents:
    """Events which can be generated, propogated, and textual DOMNodes can listen for"""

    class GameCreated(Message, bubble=False):
        pass

    class GameSaved(Message, bubble=False):
        pass

    class GameCleared(Message, bubble=False):
        pass

    class GameStateUpdated(Message, bubble=False):
        pass
