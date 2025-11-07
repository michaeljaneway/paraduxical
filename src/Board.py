import copy
from attr import dataclass
from enums.TokenType import TokenType
from enums.Direction import Direction
from Coordinate import Coordinate
from TokenLine import TokenLine


@dataclass
class Tile:
    coord: Coordinate
    token: TokenType


class Board:
    """
    Represents a hexagonal game board with a given radius
    Uses the Cube hexagonal coordinate system: https://www.redblobgames.com/grids/hexagons
    """

    def __init__(self, radius: int = 3) -> None:
        self._radius: int = radius
        self._board_map: dict[Coordinate, TokenType] = {coord: TokenType.INV for coord in Coordinate.spiral(Coordinate(0, 0, 0), radius)}

    def __str__(self) -> str:
        row_strings: list[str] = []

        # Convert rows to strings
        rows = self.get_2d_coord_list()
        for row in rows:
            row_str = " ".join([str(self[tile.coord].value) for tile in row])
            row_strings.append(row_str)

        # Center each row string
        max_str_len = len(max(row_strings, key=len))
        for i in range(len(row_strings)):
            row_strings[i] = row_strings[i].center(max_str_len)

        return "\n".join(row_strings)

    def __getitem__(self, key: Coordinate) -> TokenType:
        """Returns the token type of the given coordinate"""
        if not key in self._board_map:
            return TokenType.INV
        return self._board_map[key]

    def __setitem__(self, key: Coordinate, value: TokenType) -> None:
        """Sets the tile at the given coordinate to the given token type"""
        if not key in self._board_map:
            raise Exception(f"No valid token exists at {key}")
        self._board_map[key] = value

    def load_from_list(self, token_list: list[TokenType]) -> None:
        """Allow loading the board from an array of token types. Loads as Left->Right, Top->Bottom"""
        coords_1d = self.get_1d_coord_list()

        if len(coords_1d) != len(token_list):
            raise Exception(f"Incorrect size of token list ({len(token_list)}), should be {len(coords_1d)}")

        for i, tile in enumerate(coords_1d):
            self[tile.coord] = token_list[i]

    def get_1d_coord_list(self) -> list[Tile]:
        """Returns a 1D array containing the spaces in the board from Left->Right, Top->Bottom"""
        coord_list_1d: list[Tile] = []
        coord_list_2d = self.get_2d_coord_list()

        for row in coord_list_2d:
            coord_list_1d.extend(row)
        return coord_list_1d

    def get_2d_coord_list(self) -> list[list[Tile]]:
        """Returns a 2D array containing spaces Left->Right as rows, Top->Bottom"""
        coord_list: list[list[Tile]] = []
        for r in range(-self._radius, self._radius + 1):
            coord_list.append([])
            for s in range(self._radius, -self._radius - 1, -1):
                for q in range(-self._radius, self._radius + 1):
                    if q + r + s == 0:
                        i_coord = Coordinate(q, r, s)
                        coord_list[-1].append(Tile(i_coord, self._board_map[i_coord]))
        return coord_list

    def get_board_dict(self) -> dict[Coordinate, TokenType]:
        return copy.copy(self._board_map)

    def get_dir_edge(self, coord: Coordinate, dir: Direction) -> Coordinate:
        """Returns the coordinate at the edge of the board when moving in a given direction from the given coordinate"""
        while self[coord.neighbor(dir)] != TokenType.INV:
            coord = coord.neighbor(dir)
        return coord

    def get_dir_lines(self, coord: Coordinate, dir: Direction, min_line_len: int) -> list[TokenLine]:
        """From a given coord, scan in a given direction for lines with length >= line_len"""
        valid_lines: list[TokenLine] = []
        active_line = TokenLine(self[coord], [coord])
        
        print(dir.name, coord)

        while True:
            coord = active_line.coords[-1].neighbor(dir)
            token_type = self[coord]

            # If token is the same, just con
            if token_type == active_line.type:
                active_line.coords.append(coord)
                continue

            # If line has ended and is >= line_len, add it to the list of valid lines
            if len(active_line.coords) >= min_line_len and active_line.type in [
                TokenType.P1,
                TokenType.P2,
            ]:
                valid_lines.append(active_line)

            if token_type == TokenType.INV:
                # Break upon reaching the edge of the board
                break
            else:
                # Create new line
                active_line = TokenLine(token_type, [coord])

        return valid_lines

    def get_edge_coords(self, dir: Direction) -> list[Coordinate]:
        """Get all coordinates along a given edge of the hexagonal board"""
        scan_map: dict[Direction, tuple[Direction, Direction]] = {
            Direction.NE: (Direction.W, Direction.SE),
            Direction.E: (Direction.NW, Direction.SW),
            Direction.SE: (Direction.NE, Direction.W),
            Direction.SW: (Direction.E, Direction.NW),
            Direction.W: (Direction.SE, Direction.NE),
            Direction.NW: (Direction.SW, Direction.E),
        }

        edge_center = self.get_dir_edge(Coordinate(0, 0, 0), dir)
        edge_coords: list[Coordinate] = [edge_center]

        dir0_coord = edge_center
        dir1_coord = edge_center

        for _ in range(self._radius):
            dir0_coord = dir0_coord.neighbor(scan_map[dir][0])
            dir1_coord = dir1_coord.neighbor(scan_map[dir][1])

            edge_coords.append(dir0_coord)
            edge_coords.append(dir1_coord)

        return edge_coords

    def get_token_lines(self, min_line_len: int) -> list[TokenLine]:
        """Returns all lines on the board that are >= the given length"""
        lines: list[TokenLine] = []

        # Check along Southwest to Northeast
        sw_coords = self.get_edge_coords(Direction.SW)
        for coord in sw_coords:
            lines.extend(self.get_dir_lines(coord, Direction.NE, min_line_len))

        # Check along West to East
        w_coords = self.get_edge_coords(Direction.W)
        for coord in w_coords:
            lines.extend(self.get_dir_lines(coord, Direction.E, min_line_len))

        # Check along Northwest to Southeast
        nw_coords = self.get_edge_coords(Direction.NW)
        for coord in nw_coords:
            lines.extend(self.get_dir_lines(coord, Direction.SE, min_line_len))

        return lines


if __name__ == "__main__":
    b = Board(1)
    b.load_from_list([
              TokenType.P1, TokenType.P2,
        TokenType.P1, TokenType.P2, TokenType.P1,
              TokenType.P1, TokenType.P2,
    ])
    print(b)
    print(b.get_token_lines(2))