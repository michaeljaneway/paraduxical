# Change justifications

## General changes

- The original class diagram did not specify any classes/functions for inputs/outputs, so we added specific classes to handle the input and output needs of the game application.
- We used the `textual` Python terminal user interface (TUI) framework to implement the game's UI.
  - The original design made no mention of which framework to use to implement the game application, therefore we decided to use the `textual` terminal user interface (TUI) framework for building the game itself.
  - The `textual` TUI framework is an actively maintained free and open-source (FOSS) project for building TUI applications, and explicitly supports the Model-View-Controller (MVC) architecture, which are the reasons for our adoption of it in this implementation.
- Since `textual` is the framework powering our game implementation, we added a `ParaduxApp` class to serve as the entrypoint for the `textual` TUI framework to run our implementation.
  - Note: frameworks, contrary to libraries, run the user's code rather than the user calling functions from the framework itself.
    - This feature/design of frameworks is why an explicit entrypoint for our game application: `ParaduxApp`, is necessary to allow the framework to find and run our game application implementation.

## MVC fixes

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
  - Added `BoardWidget` class to serve as a reusable and portable UI element, which is used by the `GameView` to display the board with different tokens at instances of winning and losing.
    - The original design did not make mention of UI widgets that can be reused by different parts of the views, which makes reusing UI elements across distinct views much harder. So, it was necessary to implement widgets to add reusability to our implementation of the game.
  - Added `CellButton` class to provide a reusable and interactive button to represent: (1) the token type that describes whether tokens belong to either player or are empty, and (2) the coordinates of the token on the game board, because the original design made no mention of reusable UI elements.
    - Much like `BoardWidget`, the inclusion of `CellButton` allows for more reusable code in the game's implementation.
  - Added `LoadScreen` view to provide a dedicated view for loading a game from a save file to comply with the MVC architecture, since the original design made no mention of the "View" in the MVC architecture.
  - Added `SaveScreen` view to allocate a distinct view for saving a game to a file to comply with the MVC architecture because the original design made no mention of the "View" in the MVC architecture.
  - Added `WinScreen` view to give a singular view for displaying the winning player to comply with the MVC architecture as the original design did not make use of the "View" in the MVC architecture.

Notes about controllers in the original design:
  - For the "Controller" aspect of the MVC pattern, we implemented a `GameController` class to serve as the primary and sole controller of the game.
  - We reviewed the class diagrams and class list in the original design document (from pages 8-12, inclusive), and found that there were no clear controllers for the design.
  - In-fact, many of the classes, like `Game` and `Move` (see pages 9-10, inclusive, of the original design document) are serving as both models and controllers, which made implementing the design correctly with the MVC pattern impossible.
  - Our `GameController` serves as a clear barrier between the model and view classes of the game's implementation, and is, essentially, a middleman between the view classes and the model classes.

## Class changes made during implementation

The changes made to the individual classes in this section are not directly related to MVC fixes, but they were made nonetheless because the original class diagrams and lists did not include important class members necessary to complete the classes. Further, completing the game's implementation without completing the important classes that have missing members in the original design would have made the correct implementation of the original design impossible.

This section is split into distinct lists for each of the core class from the original design, and they will describe the changes made and the rationale for making them where applicable.

The `Board` class (from pages 8 and 11 of the original design document) changes and rationale behind them are here:
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
  - Added a `Tile` data class in `Board.py` to make it easier to map token types with their coordinates, since the previous design had a difficult token grid to impelemnt.

The `Game` class (from pages 8-9, inclusive, of the original design document) changes and rationale behind them are here:
  - Removed `players` instance variable list because using a list data structure for managing only 2 players at any time is redundant and unnecessary, and expanded the `TokenType` enumerator to track which tokens belong to which player instead.
    - Since there are only 2 players, our `TokenType` enumerator only tracks tokens for 2 players playing the same game.
  - Modified `currentTurnIndex` instance variable to use the `move_history` list instance variable instead, which makes it so that we can use the length of the `move_history` list to get the current index of the game session.
    - We needed a data structure to hold the player move history of the game, which is critical for saving game states and allowing players to load a saved game from prior sessions.
    - However, we could use the same data structure to find the current index of the game by simply measuring the length of the list, which makes it more appropriate for tracking the current move of the game than the old `players` instance variable.
  - Added a `layout_map` set to the `Game` class to allow it to provide a default set of values for setting the board at the start of a game, which decouples the `Game` and `Board` classes from one another.
    - The older design had the `Board` responsible for initially setting up the game board, but it meant that the `Board` class was knowledgeable of the game's implementation, and thus gave the `Board` class access to information it should not have had access to.
  - Moved `StartGame()` from `Game` class, which is a class inside the "Model" of the MVC architecture, to the `GameController` class, which is a class for a "Controller" in the MVC pattern.
    - The old design incorrectly put the responsibility of creating a new game within the `Game` class, which is a class that is a part of the model of the game application.
      - This bad design decision made it so that the non-existent views, from the original design, had to directly talk to the `Game` model class to simply start a new game, thus violating the rules of the MVC design pattern.
      - To fix this bad decision, we used a `GameController` to provide various controller-appropriate responsibilities, such as to: (1) create a new game, and (2) clear a current game, and it serves as an application processing interface (API) provider that the newly implemented views described in the [MVC fixes](#mvc-fixes) section can talk to in order to update the model through its provided methods.
  - Moved `setupBoard()` into the `Game` class constructor since the `Game` class must setup a board before it is able to do anything useful, so it made sense to have it inside an important class method like the class constructor.
  - Moved `switchTurn()` into the `play_move()` method in `Game` because you have to play a move in order to have a turn switch occur, and the original design incorrectly put the execution of a move within the `Move` class.
    - Having the execution of the move within the `Move` class violates the single responsibility principle (SRP) since the `Move` class should not be executing moves; the game should be the only executor of a game move in the full implementation.
  - Moved `endGame()` method from the `Game` class to the `GameController` class because ending an active game is a controller responsibility -- and not a model responsibility -- to comply with the MVC architecture.
    - In this case, the `GameController` simply deletes the active game by setting a reference to an instance of the `Game` class to nothing, so it makes separating and decoupling the view classes from the model classes for deleting games much easier.

The `Move` class (from pages 8 and 9 of the original design document) changes are here:
  - Moved `execute()` method from the `Move` class to the `Game` class.
    - For justification, see the `Game` class changelog in the [Class changes made during implementation](#class-changes-made-during-implementation) section.

The `Token` class (from pages 8 and 11 of the original design document) changes are here:
  - Split the original `Token` class into the: (1) `TokenType` enumerator class, (2) `TokenLine` class, and (3) `Coordinate` class, to make implementation possible and to comply with SRP and encapsulate lines of winning tokens possible.
    - The previous design had `Token` position accessing and mutating methods, which violated SRP because tokens do not need to know about how they are moved across the board to function.
      - We expanded the `Coordinate` class to include: (1) information about coordinates for tokens, and (2) methods to access and mutate token coordinates, to decouple token position information from the actual token properties, which are stored in the `TokenType` enumerator.
    - The `TokenType` enumerator provides all the information necessary for a token's basic elements to be understood by the `TokenLine` and `Board` classes.
    - The previous design also did not provide any correct ways to group and encapsulate lines of winning tokens on a grid, so we implemented the `TokenLine` class to provide this functionality.
      - We need this functionality to be able to determine winners of the game during a game session.

The `Player` class (from pages 8 and 10-11, inclusive) changes are described here:
  - Removed `Player` class to reduce redundancy and improve implementation correctness.
    - During implementation, the `Player` class proved redundant and incorrect because it did not provide any useful functionality for the full implementation of the game.
      - Everything in the `Player` class from the original design was already provided by the `Token` and `Move` classes through their class members, and there was no clear justification for the existence of the `Player` class in the original design.

<!--The `Coordinate` class (from pages 8 and 12) changes are described here:
  - S-->
