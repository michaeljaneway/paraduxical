import sys

import uvicorn

from gui.ParaduxWindow import ParaduxGui
from tui.ParaduxApp import ParaduxTui

if __name__ == "__main__":
    # Get the mode from the cmd arguments if one was selected
    mode: str = "server"
    if len(sys.argv) > 1:
        mode = sys.argv[1]

    # Execute the application respective to the mode
    match mode:
        case "gui":
            gui_app = ParaduxGui()
            gui_app.mainloop()
        case "tui":
            tui_app = ParaduxTui()
            tui_app.run()
        case "server" | _:
            uvicorn.run("backend.GameServerController:app", reload=False)
