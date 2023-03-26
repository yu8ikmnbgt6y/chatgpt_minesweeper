
# ClassDiagram
Please make the Class Diagram for our implementation we discussed until now.
The Class diagram you will make have all the classes the application has.
So, it will be the overall view of the application.

## Format
Markdown, Mermaid

## Classes
Output Class diagram must include these classes
#####含むべきクラスを列挙する以下は例#######
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
When relating classes, use a relational expression such as the one below.

| Relationship | Mermaid Representation |
| --- | --- |
| Inheritance | ``` A <|-- B``` |
| Aggregation | ``` A o-- B``` |
| Composition | ``` A *-- B``` |
| Association | ``` A --> B``` |
| Link | ``` A -- B``` |
| Dependency | ``` A ..> B``` |
| Realization | ``` A ..|> B``` |
| Multiplicity | ```eg.) A "1" -- "1..*" B``` |
