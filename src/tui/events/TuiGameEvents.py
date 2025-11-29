from textual.message import Message


class TuiGameEvents:
    class GameCreated(Message, bubble=False):
        pass

    class GameSaved(Message, bubble=False):
        pass

    class GameCleared(Message, bubble=False):
        pass

    class GameStateUpdated(Message, bubble=False):
        pass
