from enums.BoardLayout import BoardLayout


class Board:
    def __init__(self, layout: BoardLayout) -> None:
        self.grid: list[list[int]] = [
            [1, 2, 1, 2],
            [2, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 2],
            [2, 0, 0, 0, 1],
            [1, 2, 1, 2],
        ]

        match layout:
            case BoardLayout.HORZ:
                self.grid[3][2] = 1
                self.grid[3][4] = 2
            case BoardLayout.DIAG:
                self.grid[2][3] = 1
                self.grid[4][2] = 2

    def __str__(self) -> str:
        spacing = 2

        type_dict = {
            0: "-",
            1: "o",
            2: "x",
        }

        row_count = len(self.grid)
        max_row_len = len(max(self.grid, key=len))
        column_count = max_row_len * 2 - 1

        # Add corner space & spacing until the first column
        board_str = " " + " " * spacing

        # Add column headers
        for i in range(column_count):
            board_str += chr(65 + i) + " " * (spacing - 1)
        board_str += "\n\n" if spacing > 1 else "\n"

        # Add rows
        for i in range(row_count):
            # Row number
            board_str += f"{i+1}" + " " * spacing

            # Spacing before first token
            board_str += " " * spacing * (max_row_len - len(self.grid[i]))

            # Iterate over tokens and
            for j in self.grid[i]:
                board_str += f"{type_dict[j]}" + " " * (spacing * 2 - 1)
            board_str += "\n" * spacing

        return board_str


if __name__ == "__main__":
    horz_board = Board(BoardLayout.HORZ)
    print(horz_board)

    diag_board = Board(BoardLayout.DIAG)
    print(diag_board)
