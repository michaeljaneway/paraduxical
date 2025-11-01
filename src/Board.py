from enums.BoardLayout import BoardLayout
from enums.Direction import Direction
from enums.TokenType import TokenType
from enums.MoveType import MoveType
from Position import Position
from Move import Move


class Board:
    """Represents a hexagonal game board"""

    def __init__(self, layout: BoardLayout) -> None:
        self.grid: list[list[TokenType]] = [
            [TokenType.P1, TokenType.P2, TokenType.P1, TokenType.P2],
            [TokenType.P2, TokenType.MT, TokenType.MT, TokenType.MT, TokenType.P1],
            [
                TokenType.P1,
                TokenType.MT,
                TokenType.MT,
                TokenType.MT,
                TokenType.MT,
                TokenType.P2,
            ],
            [
                TokenType.P2,
                TokenType.MT,
                TokenType.MT,
                TokenType.MT,
                TokenType.MT,
                TokenType.MT,
                TokenType.P1,
            ],
            [
                TokenType.P1,
                TokenType.MT,
                TokenType.MT,
                TokenType.MT,
                TokenType.MT,
                TokenType.P2,
            ],
            [TokenType.P2, TokenType.MT, TokenType.MT, TokenType.MT, TokenType.P1],
            [TokenType.P1, TokenType.P2, TokenType.P1, TokenType.P2],
        ]

        match layout:
            case BoardLayout.HORZ:
                self.grid[3][2] = TokenType.P1
                self.grid[3][4] = TokenType.P2
            case BoardLayout.DIAG:
                self.grid[2][3] = TokenType.P1
                self.grid[4][2] = TokenType.P2

    def __str__(self) -> str:
        spacing = 3

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
                board_str += f"{j.value}" + " " * (spacing * 2 - 1)
            board_str += "\n" * spacing

        return board_str

    def coordToPosition(self, coord: tuple[str, str]) -> Position:
        # Determine the Y position
        y: int = int(coord[1]) - 1

        # Determine the X position
        x = ord(coord[0].lower()) - 97
        x -= abs(len(self.grid) // 2 - y)

        if x % 2 != 0:
            raise Exception(
                f"The column '{coord[0]}' is not a valid column for row '{coord[1]}'"
            )

        x //= 2

        if x < 0:
            raise Exception(
                f"The column '{coord[0]}' preceeds the first valid column for row '{coord[1]}'"
            )
        elif x > len(self.grid[y]) - 1:
            raise Exception(
                f"The column '{coord[0]}' is past the last valid column for row '{coord[1]}'"
            )

        return Position(x, y)

    def getTokenAtPosition(self, pos: Position) -> TokenType:
        if (
            pos.x < 0
            or pos.y < 0
            or pos.y >= len(self.grid)
            or pos.x >= len(self.grid[pos.y])
        ):
            return TokenType.INV
        return self.grid[pos.y][pos.x]

    def getAdjacentPositions(self, pos: Position) -> dict[Direction, Position]:
        adjacent_positions: dict[Direction, Position] = {}

        # North
        if pos.y <= 3:
            adjacent_positions[Direction.NE] = Position(pos.x, pos.y - 1)
            adjacent_positions[Direction.NW] = Position(pos.x - 1, pos.y - 1)
        else:
            adjacent_positions[Direction.NE] = Position(pos.x + 1, pos.y - 1)
            adjacent_positions[Direction.NW] = Position(pos.x, pos.y - 1)

        # South
        if pos.y < 3:
            adjacent_positions[Direction.SE] = Position(pos.x + 1, pos.y + 1)
            adjacent_positions[Direction.SW] = Position(pos.x, pos.y + 1)
        else:
            adjacent_positions[Direction.SE] = Position(pos.x, pos.y + 1)
            adjacent_positions[Direction.SW] = Position(pos.x - 1, pos.y + 1)

        # East / West
        adjacent_positions[Direction.E] = Position(pos.x + 1, pos.y)
        adjacent_positions[Direction.W] = Position(pos.x - 1, pos.y)

        return adjacent_positions

    def getAdjacentTokens(self, pos: Position) -> dict[Direction, TokenType]:
        adjacent_tokens: dict[Direction, TokenType] = {}
        adjacent_positions = self.getAdjacentPositions(pos)

        for i in adjacent_positions:
            adjacent_tokens[i] = self.getTokenAtPosition(adjacent_positions[i])

        return adjacent_tokens

    def isValidMove(self, move: Move) -> bool:
        # Get token metadata
        t1 = move.token1
        t1_ttype = self.getTokenAtPosition(t1)
        t1_adjacent_pos = self.getAdjacentPositions(t1)
        t1_adjacent_tokens = self.getAdjacentTokens(t1)

        t2 = move.token2
        t2_ttype = self.getTokenAtPosition(t2)
        t2_adjacent_pos = self.getAdjacentPositions(t2)
        t2_adjacent_tokens = self.getAdjacentTokens(t2)

        # Tokens must be not empty and belong to different players
        p_token_types = [TokenType.P1, TokenType.P2]
        if not (
            t1_ttype in p_token_types
            and t2_ttype in p_token_types
            and t1_ttype != t2_ttype
        ):
            print("Invalid token types")
            return False

        # Tokens most be adjacent
        are_tokens_adjacent = False
        for direction in t1_adjacent_pos:
            if t2 == t1_adjacent_pos[direction]:
                are_tokens_adjacent = True
                break
        if not are_tokens_adjacent:
            print("Tokens are not adjacent")
            return False

        # If the move type is SWAP, we now know this is a valid move
        if move.moveType == MoveType.SWAP:
            return True

        # Ensure no pieces are in the way for the SHIFT move (unless it is the other piece involved in the move)
        if not (
            t1_adjacent_tokens[move.direction] == TokenType.MT
            or t1_adjacent_pos[move.direction] == t2
        ):
            print("Token one is blocked")
            return False
        if not (
            t2_adjacent_tokens[move.direction] == TokenType.MT
            or t2_adjacent_pos[move.direction] == t1
        ):
            return False

        # It is now guaranteed that the SHIFT move is valid
        return True

    def executeMove(self, move: Move) -> None:
        if not self.isValidMove(move):
            raise Exception("The given move is invalid")

        match move.moveType:
            case MoveType.SWAP:
                temp_token = self.getTokenAtPosition(move.token1)
                self.grid[move.token1.y][move.token1.x] = self.getTokenAtPosition(
                    move.token2
                )
                self.grid[move.token2.y][move.token2.x] = temp_token

            case MoveType.SHIFT:
                t1_new_pos = self.getAdjacentPositions(move.token1)[move.direction]
                t2_new_pos = self.getAdjacentPositions(move.token2)[move.direction]

                t1_token_type = self.getTokenAtPosition(move.token1)
                t2_token_type = self.getTokenAtPosition(move.token2)

                self.grid[move.token1.y][move.token1.x] = TokenType.MT
                self.grid[move.token2.y][move.token2.x] = TokenType.MT

                self.grid[t1_new_pos.y][t1_new_pos.x] = t1_token_type
                self.grid[t2_new_pos.y][t2_new_pos.x] = t2_token_type

    def checkDirection(self, pos: Position, dir: Direction) -> TokenType:
        current_ttype: TokenType = self.getTokenAtPosition(pos)
        current_count: int = 1

        while True:
            adjacent_pos = self.getAdjacentPositions(pos)
            new_pos = adjacent_pos[dir]
            new_ttype = self.getTokenAtPosition(new_pos)

            if new_ttype == TokenType.INV:
                # Handle reaching the edge of the board
                break
            elif new_ttype == current_ttype:
                # Handle same token type as last cycle
                current_count += 1
            else:
                # Handle different token type than the one last cycle
                current_ttype = new_ttype
                current_count = 1

            # Return winning player if someone has won
            if current_count >= 4 and current_ttype in [TokenType.P1, TokenType.P2]:
                return current_ttype

            pos = new_pos

        return TokenType.MT

    def getWinner(self) -> TokenType:
        starting_positions = [
            # North east starting points
            (Position(0, 3), Direction.NE),
            (Position(0, 4), Direction.NE),
            (Position(0, 5), Direction.NE),
            (Position(0, 6), Direction.NE),
            (Position(1, 6), Direction.NE),
            (Position(2, 6), Direction.NE),
            (Position(3, 6), Direction.NE),
            # East starting points
            (Position(0, 0), Direction.E),
            (Position(0, 1), Direction.E),
            (Position(0, 2), Direction.E),
            (Position(0, 3), Direction.E),
            (Position(0, 4), Direction.E),
            (Position(0, 5), Direction.E),
            (Position(0, 6), Direction.E),
            # South East starting points
            (Position(0, 3), Direction.SE),
            (Position(0, 2), Direction.SE),
            (Position(0, 1), Direction.SE),
            (Position(0, 0), Direction.SE),
            (Position(1, 0), Direction.SE),
            (Position(2, 0), Direction.SE),
            (Position(3, 0), Direction.SE),
        ]

        for start in starting_positions:
            result = self.checkDirection(start[0], start[1])
            if result != TokenType.MT:
                return result
        return TokenType.MT
