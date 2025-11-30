import argparse

from cli.enums.CLIProgram import CLIProgram
from cli.enums.ParaduxicalStack import ParaduxicalStack
from cli.enums.PortSwitch import PortSwitch

class CommandLineInterface():
    def init_paradux_cli(self) -> argparse.ArgumentParser:
        return argparse.ArgumentParser(prog=CLIProgram.PROG_NAME.value, description=CLIProgram.PROG_DESCRIPTION.value)

    def init_paradux_cli_args(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(ParaduxicalStack.PARADUXICAL_STACK.value, choices=[ParaduxicalStack.PARADUXICAL_SERVER.value, ParaduxicalStack.PARADUXICAL_TUI.value, ParaduxicalStack.PARADUXICAL_GUI.value])
        parser.add_argument(PortSwitch.PORT_SWITCH_SHORT.value, PortSwitch.PORT_SWITCH_LONG.value, type=PortSwitch.PORT_SWITCH_TYPE.value, default=PortSwitch.PORT_DEFAULT_VALUE.value, required=PortSwitch.PORT_REQUIRED.value, help=PortSwitch.PORT_HELP_MESSAGE.value)

    def parse_paradux_cli_args(self, parser: argparse.ArgumentParser) -> argparse.Namespace:
        return parser.parse_args()

    def print_parsed_cli_args(self, parsed_args: argparse.Namespace) -> None:
        print(f"The parsed arguments are: {parsed_args}")
