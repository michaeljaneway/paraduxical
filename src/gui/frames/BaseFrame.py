import tkinter as tk
from tkinter import Misc
from typing import Callable

from GameClientController import GameClientController
from gui.frames.FrameType import FrameType


class EventCallback:
    def __init__(self, event: str, callback: Callable, funcid: str = "") -> None:
        self.event = event
        self.callback = callback
        self.funcid = funcid


class BaseFrame(tk.Frame):
    def __init__(self, root: Misc, controller: GameClientController, **kwargs) -> None:
        super().__init__(root, **kwargs)
        self._controller = controller
        self._model = self._controller.model_proxy
        self._event_callbacks: list[EventCallback] = []

    def switch_frame(self, frame: FrameType):
        self.winfo_toplevel().switch_frame(frame)  # type: ignore

    """Event Callbacks"""

    def bind_event_callbacks(self):
        """Bind event callbacks"""
        for ec in self._event_callbacks:
            ec.funcid = self.winfo_toplevel().bind(ec.event, ec.callback, True)
            print("\nBaseFrame BINDING")
            print("\tEvent: ", ec.event)
            print("\tCallback: ", ec.callback)
            print("\tFuncId:", ec.funcid)

    def unbind_event_callbacks(self):
        """Unbind all callbacks and clear the event callbacks list"""
        for ec in self._event_callbacks:
            print("\nBaseFrame UNBINDING")
            print("\tEvent: ", ec.event)
            print("\tCallback: ", ec.callback)
            print("\tFuncId:", ec.funcid)
            self.winfo_toplevel().unbind(ec.event, ec.funcid)
        self._event_callbacks = []
