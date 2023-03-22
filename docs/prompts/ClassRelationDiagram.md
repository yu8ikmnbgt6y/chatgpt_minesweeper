
# ClassDiagram
Please make the Class Diagram for our Minesweeper game implementation we discussed until now.
The Class diagram you will make have all the classes the application has.
So, it will be the overall view of the application.

## Format
Markdown, Mermaid

## Classes
Output Class diagram must include these classes
* "Cell"
* "Interface"
* "MinesweeperGrid"
* "ScoreBoard"
* "GameScreen"
* "Menu"
* "StartScreen"
* "Timer"
* "GameStatisticsWindow"

## Exclude
Exclude class members contained in above classes from this output.
Focus on describing the relationship between the classes.
Just depict class boxes and relate them.

## Relationship
There are types of relationship between classes like below.
When you relate classes use their relationship representation.

| Classification | Relationship | Mermaid Representation |
| --- | --- | --- |
| Class Structure | Inheritance | ```classDiagram A <|-- B``` |
| Class Structure | Aggregation | ```classDiagram A o-- B``` |
| Class Structure | Composition | ```classDiagram A *-- B``` |
| Class Structure | Association | ```classDiagram A -- B``` |
| Class Structure | Instantiation | ```classDiagram A --> B``` |
| Class Interaction | Dependency | ```classDiagram A ..> B``` |
| Class Interaction | Realization | ```classDiagram A <|.. B``` |
| Multiplicity | Multiplicity | ```classDiagram A "1" -- "1..*" B``` |
| Multiplicity | Selectivity | ```classDiagram A "1" -- "0..1" B``` |
| Multiplicity | Dependency | ```classDiagram A "1" ..> "1..*" B``` |
| Multiplicity | Application | ```classDiagram A "1" --> "*" B``` |
