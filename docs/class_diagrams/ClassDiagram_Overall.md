```mermaid
classDiagram
    class Cell
    class Interface
    class MinesweeperGrid
    class ScoreBoard
    class GameScreen
    class Menu
    class StartScreen
    class Timer
    class GameStatisticsWindow

    Interface --> StartScreen
    Interface --> GameScreen
    Interface --> Menu
    Interface --> GameStatisticsWindow
    Interface --> ScoreBoard
    
    StartScreen --> Interface
    GameScreen --> Interface
    Menu --> Interface
    GameStatisticsWindow --> Interface
    ScoreBoard --> Interface
    
    GameScreen --> MinesweeperGrid
    GameScreen --> Timer
    GameScreen --> ScoreBoard
    
    MinesweeperGrid *-- Cell
```