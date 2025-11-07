# Change justifications

## General changes

- The original class diagram did not specify any classes/functions for inputs/outputs.
- We used the `textual` Python terminal user interface (TUI) framework to implement the game's UI.

## Model-View-Controller (MVC) fixes

Pages from the original design that are cited and relevant to all the content described in this section are: pages 8 to 12, inclusive. These pages from the original design document include all the class diagrams and lists relevant to this section. Any discussion in this section that refers to the original design document refers to these specific pages from the original design.

The original design included class diagrams and lists that made no mention of the View in the MVC architecture/design pattern. We solved this problem in our implementation by making changes to the original design to support the View component of the MVC design pattern. We were especially troubled by the missing game user interface (UI) view, which would have created tight coupling with all of the game's classes in implementation.

Before the views below are described, all the views implemented are "dumb views" because they do not do anything beyond just displaying the user interface and allowing the user to interact with it. They do not interact with the game's model, and are controlled by the game's controllers.

The precise fixes for the "View" part of MVC in the original design document with their rationale are described here:
  - Added `GameScreen` class to represent the main game view to comply with the MVC architecture.
    - The `GameScreen` holds and displays user interface elements for the game like the buttons for shifting and swapping tokens, and allows the user to interact with them too.
  - Added `MainMenuScreen` class to represent the game's main menu view to comply with the MVC architecture.
    - The game's main menu includes buttons for starting a new game, and loading an existing game, for example.
  - Added `NewGameScreen` class to represent the view for the "New Game" component to: (1) allow the player to choose between diagonal and horizontal setups for the game board, and (2) make the original design more MVC-compliant.
  - Added `RulesScreen` class to represent the "Rules" component to: (1) allow the user to view the rules of the game from the main menu of the game, and (2) make the original design more MVC-compliant.

## Class changes made during implementation

The changes made to the individual classes in this section are not directly related to MVC fixes, but they were made nonetheless because the original class diagrams and lists did not include important class members necessary to complete the classes. Further, completing the game's implementation without completing the important classes that have missing members in the original design would have made the correct implementation of the original design impossible.

This section is split into distinct lists for each of the core class from the original design, and they will describe the changes made and the rationale for making them where applicable.

The `Board` class changes (from and rationale behind them are here:
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
- Removed `players` instance variable list because using a list data structure for managing only 2 players at any time is redundant and unnecessary, and expanded the `TokenType` enumerator to track which tokens belong to which player instead.
  - Since there are only 2 players, our `TokenType` enumerator only tracks tokens for 2 players playing the same game.
- Modified `currentTurnIndex` instance variable to use the `move_history` list instance variable instead, which makes it so that we can use the length of the `move_history` list to get the current index of the game session.
  - We needed a data structure to hold the player move history of the game, which is critical for saving game states and allowing players to load a saved game from prior sessions.
  - However, we could use the same data structure to find the current index of the game by simply measuring the length of the list, which makes it more appropriate for tracking the current move of the game than the old `players` instance variable.
- Added a `layout_map` set to the `Game` class to allow it to provide a default set of values for setting the board at the start of a game, which decouples the `Game` and `Board` classes from one another.
  - The older design had the `Board` responsible for initially setting up the game board, but it meant that the `Board` class was knowledgeable of the game's implementation, and thus gave the `Board` class access to information it should not have had access to.
- Replaced
