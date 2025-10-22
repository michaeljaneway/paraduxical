# from enums.BoardLayout import BoardLayout
from enums.Direction import Direction

# from enums.TokenType import TokenType
from enums.MoveType import MoveType
from Position import Position
from Move import Move
from Board import Board


class GameView:
    def getCoordinate(self) -> tuple[str, str]:
        pos_input = input().strip()
        return (pos_input[0], pos_input[1])

    def getDirection(self) -> Direction:
        while True:
            print(
                "Please enter the shift direction by entering the abbreviation (case-insensitive): "
            )
            print("NE - North-East")
            print("E - East")
            print("SE - South-East")
            print("SW - South-West")
            print("W - West")
            print("NW - North-West")

            dir_input = input().strip().lower()

            match dir_input:
                case "ne":
                    return Direction.NE
                case "e":
                    return Direction.E
                case "se":
                    return Direction.SE
                case "sw":
                    return Direction.SW
                case "w":
                    return Direction.W
                case "nw":
                    return Direction.NW
                case _:
                    continue

    def getPlayerMove(self, board: Board) -> Move:
        move_type: MoveType
        pos1: Position
        pos2: Position
        move_dir: Direction = Direction.NoDirection

        # Select move type
        while True:
            move_type_str = input(
                "Please enter the type of move you'd like to make\n1 for SWAP\n2 for SHIFT\n"
            ).strip()

            match int(move_type_str):
                case 1:
                    move_type = MoveType.SWAP
                    break
                case 2:
                    move_type = MoveType.SHIFT
                    break
                case _:
                    print("Please enter a valid selection")

        print("Please enter the first token's position (e.g. 'J7')")
        pos1 = board.coordToPosition(self.getCoordinate())

        print("Please enter the second token's position (e.g. 'K6')")
        pos2 = board.coordToPosition(self.getCoordinate())

        if move_type == MoveType.SHIFT:
            move_dir = self.getDirection()

        return Move(move_type, pos1, pos2, move_dir)
