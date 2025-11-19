import pickle

from backend.Board import Board
from shared.Coordinate import Coordinate
from shared.enums import BoardLayout, Direction, MoveType, TokenType
from shared.Move import Move
from shared.TokenLine import TokenLine


class Game:
    """The Paradux game model, handles all game logic"""

    # Diagonal and Horizontal game board layouts hardcoded as 1D array
    layout_map = {
        BoardLayout.HORZ: [
            TokenType(x) for x in [1, 2, 1, 2, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 2, 2, 0, 1, 0, 2, 0, 1, 1, 0, 0, 0, 0, 2, 2, 0, 0, 0, 1, 1, 2, 1, 2]
        ],
        BoardLayout.DIAG: [
            TokenType(x) for x in [1, 2, 1, 2, 2, 0, 0, 0, 1, 1, 0, 0, 1, 0, 2, 2, 0, 0, 0, 0, 0, 1, 1, 0, 2, 0, 0, 2, 2, 0, 0, 0, 1, 1, 2, 1, 2]
        ],
    }

    def __init__(self, layout: BoardLayout) -> None:
        self.layout = layout
        self.board = Board(radius=3)
        self.board.load_from_list(self.layout_map[self.layout])

        self.move_history: list[Move] = []

        self.current_player = TokenType.P1
        self._reset_movement()

    def _reset_movement(self):
        self.selected_coords: list[Coordinate] = []
        self.move_type: MoveType = MoveType.NULL
        self.move_direction: Direction = Direction.NoDirection

    """Movement Selection"""

    def set_move_type(self, move_type: MoveType) -> None:
        if move_type.is_valid_movetype():
            self.move_type = move_type

    def get_move_type(self) -> MoveType:
        return self.move_type

    """Coordinate Selection"""

    def deselect_coord(self, c: Coordinate) -> None:
        self.selected_coords.remove(c)

    def select_coord(self, c: Coordinate) -> None:
        """Selects a coordinate"""
        if c in self.get_selectable_coords():
            self.selected_coords.append(c)

    def get_selected_coords(self) -> list[Coordinate]:
        return self.selected_coords

    def get_selectable_coords(self) -> list[Coordinate]:
        """Returns a list of all coordinates which can be selected by the player"""
        if len(self.get_winning_lines()) > 0:
            # If the game is won, no pieces are selectable
            return []
        
        elif len(self.selected_coords) == 0:
            # If no piece is selected, all player cells are selectable
            return [cell.coord for cell in self.board.get_1d_cell_list() if cell.token.is_player_token()]

        elif len(self.selected_coords) == 1:
            # If one piece is selected, only allow selection of adjacent opposing tokens
            board_dict = self.board.get_board_dict()

            c1 = self.selected_coords[0]
            c1_token = board_dict[c1]
            selectable_coords = []

            for dir in [Direction.NE, Direction.E, Direction.SE, Direction.SW, Direction.W, Direction.NW]:
                neighbor_coord = c1.neighbor(dir)
                neighbor_token = board_dict.get(neighbor_coord)
                if not neighbor_token or c1_token == neighbor_token or neighbor_token not in [TokenType.P1, TokenType.P2]:
                    continue
                selectable_coords.append(neighbor_coord)
            
            return selectable_coords

        # If two pieces are selected, no more cells are selectable
        return []

    """Direction Execution"""

    def get_valid_shift_directions(self) -> list[Direction]:
        """Returns a list of valid directions for a shift move given two coordinates on the game board"""
        if len(self.selected_coords) != 2:
            return []

        valid_directions: list[Direction] = []
        c1 = self.selected_coords[0]
        c2 = self.selected_coords[1]

        for dir in [Direction.NE, Direction.E, Direction.SE, Direction.SW, Direction.W, Direction.NW]:
            c1_valid = self.board[c1.neighbor(dir)] == TokenType.MT or c1.neighbor(dir) == c2
            c2_valid = self.board[c2.neighbor(dir)] == TokenType.MT or c2.neighbor(dir) == c1
            if c1_valid and c2_valid:
                valid_directions.append(dir)

        return valid_directions

    def set_shift_direction(self, dir: Direction) -> None:
        if dir in self.get_valid_shift_directions():
            self.move_direction = dir

    def get_shift_direction(self) -> Direction:
        return self.move_direction

    """Movement Execution"""

    def is_move_playable(self) -> bool:
        """Returns True if the actively selected move is valid and playable, False otherwise"""
        if (
            len(self.selected_coords) != 2
            or not self.move_type.is_valid_movetype()
            or (self.move_type == MoveType.SHIFT and self.move_direction == Direction.NoDirection)
        ):
            return False
        return True

    def play_move(self) -> None:
        """Plays the current move (if valid)"""
        if not self.is_move_playable():
            return

        # Execute move
        move = Move(self.move_type, self.selected_coords[0], self.selected_coords[1], self.move_direction)
        match move.move_type:
            case MoveType.SWAP:
                c1_token = self.board[move.c1]
                self.board[move.c1] = self.board[move.c2]
                self.board[move.c2] = c1_token

            case MoveType.SHIFT:
                t1_new_coord = move.c1.neighbor(move.direction)
                t2_new_coord = move.c2.neighbor(move.direction)
                t1_token_type = self.board[move.c1]
                t2_token_type = self.board[move.c2]

                self.board[move.c1] = TokenType.MT
                self.board[move.c2] = TokenType.MT
                self.board[t1_new_coord] = t1_token_type
                self.board[t2_new_coord] = t2_token_type

        self.move_history.append(move)
        self.current_player = TokenType.P1 if self.current_player == TokenType.P2 else TokenType.P2
        self._reset_movement()

    """Win Conditions"""

    def get_winning_lines(self) -> list[TokenLine]:
        """Returns all lines which meet the requirements to win"""
        return self.board.get_token_lines(4)

    """Saving & Loading"""

    def save_to_file(self, filename):
        """Saves the game as a pickle file with the given filename"""
        with open(filename, "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def load_from_file(cls, filename):
        """Returns a Game object loaded from the given pickle file"""
        with open(filename, "rb") as f:
            loaded_game = pickle.load(f)
        return loaded_game
