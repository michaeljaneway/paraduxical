from enum import StrEnum

class ParaduxicalStack(StrEnum):
    """Specify the values for the Paraduxical stacks for the command-line interface (CLI)"""
    PARADUXICAL_GUI = "gui"
    PARADUXICAL_SERVER = "server"
    PARADUXICAL_STACK = "stack"
    PARADUXICAL_TUI = "tui"
