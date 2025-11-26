from tkinter import Misc, ttk
from typing import Callable

from GameClientController import GameClientController


class EventCallback:
    def __init__(self, event: str, callback: Callable, funcid: str = "") -> None:
        self.event = event
        self.callback = callback
        self.funcid = funcid


class BaseFrame(ttk.Frame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self._controller = controller
        self._model = self._controller.model_proxy
        self._event_callbacks: list[EventCallback]

    def switch_frame(self, frame: ttk.Frame):
        self.unbind_event_callbacks()
        self.destroy()
        frame.grid()

    """Event Callbacks"""

    def bind_event_callbacks(self, event_callbacks: list[EventCallback]):
        """Bind a list of event callbacks"""
        self._event_callbacks = event_callbacks
        for callback in self._event_callbacks:
            callback.funcid = self.winfo_toplevel().bind(callback.event, callback.callback, "+")

    def unbind_event_callbacks(self):
        """Unbind all callbacks and clear the event callbacks list"""
        for ec in self._event_callbacks:
            self.winfo_toplevel().unbind(ec.event, ec.funcid)
        self._event_callbacks = []
