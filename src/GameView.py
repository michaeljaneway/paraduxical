import os
import re
from typing import Any
from enums.Direction import Direction
from enums.MoveType import MoveType
from Position import Position
from Move import Move
from Board import Board
from options.Option import Option
from Session import Session


class GameView:
    def clear(self):
        """
        Clears the terminal screen by running cls (on Windows) or clear (on macOS/Linux).\n
        Source - https://github.com/asweigart/clear
        """
        os.system("cls" if os.name == "nt" else "clear")

    def update(self, options: list[Option], session: Session) -> None:
        # Clear the terminal at the start of each view update
        self.clear()
        
        visible_options = [option for option in options if option.is_visible()]

        # Display the game if one is active
        self.displaySession(session)

        # Display options
        print("Select an option by entering its corresponding number")
        for i, op in enumerate(visible_options):
            print(i + 1, op.desc)

        # Get user input and ensure that it's valid
        option_sel = input().strip()
        option_re = f"^[{'|'.join(str(x) for x in list(range(1, len(visible_options)+1)))}]$"

        if re.match(option_re, option_sel):
            selected_option = visible_options[int(option_sel) - 1]
            print(f"You selected {selected_option.desc}")

            option_fields = self.getOptionFields(selected_option.fields)
            selected_option.execute(option_fields)

    def getOptionFields(self, fields: list[tuple[str, str]]) -> list[Any]:
        results: list[Any] = []

        for field in fields:
            while True:
                print(field[0])
                field_input = input().strip()

                if re.match(field[1], field_input):
                    results.append(field_input)
                    break
                else:
                    print("Entry is incorrect, please re-enter...")

        return results

    def displaySession(self, session: Session) -> None:
        if session.game:
            print(session.game)

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
