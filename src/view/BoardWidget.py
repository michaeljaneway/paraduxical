from textual.widget import Widget
from textual.widgets import Header, Footer, Button
from textual.containers import HorizontalGroup, VerticalGroup

from Game import Game
from enums.BoardLayout import BoardLayout
from enums.TokenType import TokenType


class BoardWidget(Widget):
    BINDINGS = [
        ("q", "quit_app", "Quit"),
    ]

    def __init__(
        self,
        *children: Widget,
        name: str | None = None,
        id: str | None = None,
        classes: str | None = None,
        disabled: bool = False,
        markup: bool = True
    ) -> None:
        super().__init__(*children, name=name, id=id, classes=classes, disabled=disabled, markup=markup)
        
        pass

    def compose(self):
        new_game = Game(BoardLayout.HORZ)
        board_2d = new_game.board.get_2d_coord_list()

        token_color: dict[TokenType, str] = {
            TokenType.MT: "gray",
            TokenType.P1: "black",
            TokenType.P2: "white",
        }

        yield Header()
        with VerticalGroup():
            for row in board_2d:
                with HorizontalGroup(classes="row"):
                    for cell in row:
                        c_butt = Button("", classes="board_cell")
                        c_butt.styles.background = token_color[new_game.board[cell]]
                        c_butt.styles.text_align = "center"

                        yield c_butt
        yield Footer()

