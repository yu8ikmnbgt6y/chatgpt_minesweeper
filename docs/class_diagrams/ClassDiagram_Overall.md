```mermaid
classDiagram
    Cell
    Interface
    MinesweeperGrid
    ScoreBoard
    GameScreen
    Menu
    StartScreen
    Timer
    GameStatisticsWindow

    Interface *-- Menu
    Interface *-- StartScreen
    Interface *-- GameScreen
    Interface *-- GameStatisticsWindow
    Interface *-- ScoreBoard

    GameScreen *-- MinesweeperGrid
    GameScreen *-- Timer

    MinesweeperGrid *-- Cell

    GameStatisticsWindow *-- ScoreBoard
```