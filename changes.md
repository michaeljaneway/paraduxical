# Change justifications

## General changes

- The original class diagram did not specify any classes/functions for inputs/outputs.
- We used the `textual` Python terminal user interface (TUI) framework to implement the game's UI.

## Model-View-Controller (MVC) fixes

The original design included class diagrams and lists that made no mention of the View in the MVC architecture/design pattern. We solved this problem in our implementation by making changes to the original design to support the View component of the MVC design pattern. We were especially troubled by the missing game user interface (UI) view, which would have created tight coupling with all of the game's classes in implementation.

The precise fixes with their rationale are described here:
  - View class `ParaduxApp` is now implemented to describe the main UI of the Paradux game application/program, which allows for greater decoupling of our various classes in the implementation since all of our implemented classes have more distinct reponsibilities.
    - For example: `ParaduxApp` is only concerned with UI (or "View") responsibilities whereas `Board` is responsible for game logic. `Board` is a part of the "Model" in the MVC pattern, whereas `ParaduxApp` is a part of the "View". The existence of `ParaduxApp` makes it so that "Model" classes like `Board` do not need to work with the UI, thus improving separation of concerns within our implementation of the game.

## Class changes made during implementation

The changes made to the individual classes in this section are not directly related to MVC fixes, but they were made nonetheless because the original class diagrams and lists did not include important class members necessary to complete the classes. Further, completing the game's implementation without completing the important classes that have missing members in the original design would have made the correct implementation of the original design impossible.

This section is split into distinct lists for each of the core class from the original design, and they will describe the changes made and the rationale for making them where applicable.

The `Board` class changes and rationale behind them are here:
  - Moved `isValidMove()` method from original `Board` class to `Game` class to move gameplay responsibilities from the `Board` class to the `Game` class.
    - Also, we renamed the `isValidMove()` method to `validateMove()`, but this is not a significant change, so it is only briefly mentioned here.
  - Added `load_from_list()` method to the `Board` class to allow the game board to be constructed just by providing a list that contains the token types.
    - This method decouples the game board from the game logic by not exposing the game's logic to the board, which further helps with the separation of concerns for our classes.
  - Added `get_1d_coord_list()` and `get_2d_coord_list()` methods in the `Board` class to decouple the game board from the game logic, similar to how `load_from_list()` was described earlier.
  - Added `__str__()` method to the `Board` class to make debugging the board easier, especially as the game state progresses.
  - Changed the 2-dimensional (2D) grid system to a 3-dimensional (3D) cube hexagonal grid system in the `Board` class to make the game's implementation much easier.
    - We used the following guide to learn about and implement 3D hexagonal grid systems for games, which is linked [here](https://www.redblobgames.com/grids/hexagons/).
    - Moved from a public 2D list to represent the token grid in the original design of the `Board` class to a private dictionary where coordinate is the key for the token type in the same class.
      - We made the grid private to encapsulate it from external access, and provided the appropriate and necessary methods for accessing and mutating the board when required.
    - Added a `radius` class member to the `Board` class to allow us to build the 3D cube hexagonal grid described earlier that we used to simplify game board management as the game progressed.
  - Added `get_dir_edge()`, `get_dir_lines()`, `get_edge_coords()`, and `get_token_lines()` methods in the `Board` class to implement missing functionality for the original `Board` class to be useful in our implementation.
    - The original `Board` class did not make mention of how it would: (1) receive and handle directions from the user's input, and (2) manage the edges of the board and lines of tokens provided to it from other classes, so these methods were added and implemented.

The `Game` class changes and rationale behind them are here:
- Removed `players` instance variable list because using a list data structure for managing only 2 players at any time is redundant and unnecessary, and expanded the `TokenType` enumerator to track which tokens belong to which player.
  - Since there are only 2 players, our `TokenType` enumerator only tracks tokens for 2 players playing the same game.
- S
