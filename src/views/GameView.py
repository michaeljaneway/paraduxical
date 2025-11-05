from textual.app import App
from textual.widgets import Header, Footer, Button
from textual.containers import Horizontal, Vertical

from Game import Game
from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType


class ParaduxApp(App[None]):
    BINDINGS = [
        ("q", "quit_app", "Quit"),
    ]

    CSS_PATH = "GameView.tcss"

    def compose(self):
        new_game = Game(BoardLayout.HORZ)
        board_2d = new_game.board.get_2d_coord_list()

        token_color: dict[TokenType, str] = {
            TokenType.MT: "gray",
            TokenType.P1: "#FF0000",
            TokenType.P2: "#0000FF",
        }

        yield Header()
        with Vertical():
            for row in board_2d:
                with Horizontal(classes="row"):
                    for cell in row:
                        c_butt = Button(f"{new_game.board[cell].value}", classes="board_cell")
                        c_butt.styles.background = token_color[new_game.board[cell]]
                        c_butt.styles.text_align = "center"
                        yield c_butt
        yield Footer()

    def action_quit_app(self) -> None:
        """An action to quit the app."""
        self.exit()


if __name__ == "__main__":
    app = ParaduxApp()
    app.run()
