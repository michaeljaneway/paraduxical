import uvicorn

from cli.CommandLineInterface import CommandLineInterface
from gui.ParaduxWindow import ParaduxGui
from tui.ParaduxApp import ParaduxTui

if __name__ == "__main__":
    # Setting up our CLI for Paraduxical
    cli = CommandLineInterface()
    cli_args_parser = cli.init_paradux_cli()
    cli.init_paradux_cli_args(cli_args_parser)
    cli_args_parsed = cli.parse_paradux_cli_args(cli_args_parser)
    print(f"`port` as defined by the user is {cli_args_parsed.port}")

    # Execute the application respective to the mode
    match cli_args_parsed.stack:
        case "gui":
            gui_app = ParaduxGui(cli_args_parsed.port)
            gui_app.mainloop()
        case "tui":
            tui_app = ParaduxTui(cli_args_parsed.port)
            tui_app.run()
        case "server":
            uvicorn.run("backend.GameServerController:app", port=cli_args_parsed.port, reload=False)
