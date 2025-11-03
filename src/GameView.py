import os
import re
from typing import Any
from options.Option import Option, OptionField
from Session import Session


class GameView:
    def __init__(self, session: Session) -> None:
        self.session = session

    def update(self, options: list[Option]) -> None:
        # Clear the terminal & display the game if one is active
        self.clearTerminal()
        self.displaySession()
        
        self.promptOption(options)

    def promptOption(self, options: list[Option]) -> bool:
        # Display options
        visible_options = [option for option in options if option.is_visible()]
        print("Select an option by entering its corresponding number")
        for i, op in enumerate(visible_options):
            print(i + 1, op.desc)

        # Get user input and ensure that it's valid
        option_input = input().strip().lower()
        option_re = f"^[{'|'.join(str(x) for x in list(range(1, len(visible_options)+1)))}]$"

        if re.match(option_re, option_input):
            option_selection = visible_options[int(option_input) - 1]
            option_fields = self.promptOptionFields(option_selection.fields)

            try:
                option_selection.execute(option_fields)
                return True
            except Exception as e:
                print("There was an issue with your entry: ", e)
                print("Press [ENTER] to acknowledge & retry")
                input()
        else:
            print(
                f"Input {option_input} is invalid for the input, please try again...\n")

        return False

    def promptOptionFields(self, fields: list[OptionField]) -> list[Any]:
        results: list[Any] = []

        for field in fields:
            while True:
                print(field.desc)
                field_input = input().strip().lower()

                if re.match(field.regex, field_input):
                    results.append(field_input)
                    break
                else:
                    print("Entry is incorrect, please re-enter...\n")

        return results

    def displaySession(self) -> None:
        if self.session.game:
            print(self.session.game)

    @staticmethod
    def clearTerminal():
        """
        Clears the terminal screen by running cls (on Windows) or clear (on macOS/Linux).\n
        Source - https://github.com/asweigart/clear
        """
        os.system("cls" if os.name == "nt" else "clear")
