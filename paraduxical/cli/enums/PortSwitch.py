from enum import Enum


class PortSwitch(Enum):
    """Defaults for the Paraduxical Command-Line Interface (CLI) Port Switches"""
    PORT_DEFAULT_VALUE = 8000
    PORT_HELP_MESSAGE = "Provide the port number you wish to host the Paraduxical game server on. The value must be an integer. For example: --port <num>, where `num` is an integer representing an open port on your compute environment."
    PORT_REQUIRED = True
    PORT_SWITCH_LONG = "--port"
    PORT_SWITCH_SHORT = "-p"
    PORT_SWITCH_TYPE = int
