```mermaid
classDiagram
    class Timer {
        +start_time: float
        +__init__(): None
        +start_timer(): None
        +get_elapsed_time(): float
    }
```

| name            | type                              | description                                              |
| --------------- | --------------------------------- | -------------------------------------------------------- |
| \_\_init\_\_        | instance method, public, None     | Initializes a Timer object with start_time set to 0.0    |
| start_timer     | instance method, public, None     | Starts the timer by setting start_time to the current time |
| get_elapsed_time| instance method, public, float    | Returns the elapsed time since start_timer was called   |
| start_time      | instance attribute, private, float| Stores the start time of the timer                      |



```mermaid
classDiagram
    class ScoreBoard {
        -_save_data_file: str
        -statistics: Dict[str, Dict[str, int]]
        -high_scores: Dict[str, List[Tuple[int, str]]]
        +__init__(save_data_file: str): None
        +_check_difficulty(difficulty: str): None
        +get_statistics(difficulty: str): Dict[str, int]
        +update_statistics(difficulty: str, won: bool): None
        +get_high_scores(difficulty: str): List[Tuple[int, str]]
        +update_high_scores(difficulty: str, time: int, timestamp: str): None
        +_save_data(): None
        +load_data(): None
    }
```
| name             | type                                         | description                                              |
| ---------------- | -------------------------------------------- | -------------------------------------------------------- |
| \_\_init\_\_         | instance method, public, None                | Initializes a ScoreBoard object with default values     |
| get_statistics   | instance method, public, Dict[str, int]      | Returns the statistics for the given difficulty         |
| update_statistics| instance method, public, None                | Updates the statistics for the given difficulty         |
| get_high_scores  | instance method, public, List[Tuple[int, str]]| Returns the high scores for the given difficulty       |
| update_high_scores| instance method, public, None               | Updates the high scores for the given difficulty        |
| _save_data       | instance method, private, None               | Saves the statistics and high scores to a JSON file     |
| _load_data       | instance method, private, None               | Loads the statistics and high scores from a JSON file   |
| _check_difficulty| instance method, private, None               | Checks if the given difficulty is valid                 |
| _save_data_file  | instance attribute, private, str             | Stores the path to the save data file                   |
| _statistics      | instance attribute, private, Dict[str, Dict[str, int]]| Stores the statistics for each difficulty          |
| _high_scores     | instance attribute, private, Dict[str, List[Tuple[int, str]]]| Stores the high scores for each difficulty  |


### Grid class description
```mermaid
classDiagram
    class Grid {
        +rows: int
        +cols: int
        +mines: int
        +cells: List[List[Cell]]
        +mine_opened: bool
        +__init__(rows: int, cols: int, mines: int): None
        -in_bounds(row: int, col: int): bool
        +initialize_grid(first_click_row: int, first_click_col: int): None
        -place_mines(exclude_row: int, exclude_col: int): None
        -calculate_adjacent_mines(): None
        +open_cell(row: int, col: int): Tuple[bool, List[Tuple[int, int]]]
        +flag_cell(row: int, col: int): bool
        +check_game_status(): str
        +print_opened_cells(): None
        +__str__(): str
    }
```
| name                 | type                              | description                                                  |
| -------------------- | --------------------------------- | ------------------------------------------------------------ |
| \_\_init\_\_             | instance method, public, None     | Initializes a Grid object with rows, cols, and mines         |
| initialize_grid      | instance method, public, None     | Initializes the grid with mines and adjacent mines after the first click |
| open_cell            | instance method, public, Tuple[bool, List[Tuple[int, int]]] | Opens a cell and returns whether it's a mine and a list of opened cells |
| flag_cell            | instance method, public, bool     | Toggles the flag status of a cell and returns the new flag state |
| check_game_status    | instance method, public, str      | Checks the game status and returns "lost", "won", or "ongoing" |
| print_opened_cells   | instance method, public, None     | Prints the opened cells in the grid                           |
| \_\_str\_\_              | instance method, public, str      | Returns a string representation of the grid                   |
| rows                 | instance attribute, private, int  | Number of rows in the grid                                   |
| cols                 | instance attribute, private, int  | Number of columns in the grid                                |
| mines                | instance attribute, private, int  | Number of mines in the grid                                  |
| cells                | instance attribute, private, List[List[Cell]] | 2D list of Cell objects representing the grid                |
| mine_opened          | instance attribute, private, bool | Flag indicating if a mine has been opened                    |
| in_bounds            | instance method, private, bool    | Checks if the given row and col are within the grid bounds   |
| place_mines          | instance method, private, None    | Places mines on the grid, excluding the cell specified       |
| calculate_adjacent_mines | instance method, private, None | Calculates the number of adjacent mines for each cell        |


---
```mermaid
classDiagram
    class Cell {
        -_is_mine: bool
        -_is_open: bool
        -_is_flagged: bool
        -_adjacent_mines: int

        +__init__(is_mine: bool): None
        +open(): None
        +set_adjacent_mines(adjacent_mines: int): None
        +toggle_flag(): None

        +is_open: bool (property)
        +adjacent_mines: int (property)
        +flagged: bool (property)
        +is_mine: bool (property)
    }
```

| name             | type                               | description                                              |
| ---------------- | ---------------------------------- | -------------------------------------------------------- |
| \_\_init\_\_         | instance method, public, None      | Initializes a Cell object with default values           |
| is_open          | property, public, bool             | Returns the value of _is_open attribute                 |
| open             | instance method, public, None      | Sets the _is_open attribute to True                     |
| set_adjacent_mines| instance method, public, None     | Sets the _adjacent_mines attribute to the given value   |
| adjacent_mines   | property, public, int              | Returns the value of _adjacent_mines attribute          |
| toggle_flag      | instance method, public, None      | Toggles the value of _is_flagged attribute              |
| flagged          | property, public, bool             | Returns the value of _is_flagged attribute              |
| is_mine          | property, public, bool             | Returns the value of _is_mine attribute                 |
| put_mine         | instance method, public, None      | Sets the _is_mine attribute to True                     |
| _is_mine         | instance attribute, private, bool  | Stores whether the cell contains a mine                 |
| _is_open         | instance attribute, private, bool  | Stores whether the cell is open                         |
| _is_flagged      | instance attribute, private, bool  | Stores whether the cell is flagged                      |
| _adjacent_mines  | instance attribute, private, int   | Stores the number of adjacent mines                     |

---