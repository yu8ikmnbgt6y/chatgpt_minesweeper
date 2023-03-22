# Code Description Table

Create a table that interprets the code written in Python in the ##CODE field and describes the class.
The table to be answered should follow the conditions in the ##Condition field

## Condition
Format: Markdown, Table
Table Header Content: ["Name", "Access", "Member Type", "Data Type", "Description"]
Row: member

Please enter the items in the table according to the content of the header
The description of each item is as follows

* "Name":
  * The name of member
* "Access":
  Describes which Access Specifier the member corresponds to. It will be "Public" or "Private" in Python code.
* "Member Type":
	Describes whether the member is a "Method", "Variable", or "Property".
	When the Method is decorated as @classmethod add "/class" after the "Method".
	When the Method is decorated as @staticmethod add "/static" after the "Method".
* "DataType":
  * DataType of the member.
  * what Datatype is return, when the member is called.
  * when the member is method or property, this item means return DataType
  * When the member is variable, this item means Variable DataType.
* "Description":
  * Description of the member.
  * length of this items differ from the , If the member is important, make description longer up to 8 sentences.
  * When the member is not important, make description shorter. One sentence is acceptable.

Ensure that the table is ordered according to these two priorities:
	1. Members whose "Access" is "Public" must appear above "Private" members.
	2. Members should be listed in the same order as they appear in the source code unless the above conditions are violated.


## CODE

```
class ScoreBoard:
    def __init__(self, save_data_file: str = "save_data.json"):
        self._save_data_file = save_data_file
        self._statistics = defaultdict(lambda: defaultdict(int))
        self._high_scores = defaultdict(list)
        self._load_data()


    def _check_difficulty(self, difficulty: str) -> None:
        if difficulty not in DIFFICULTIES:
            raise NotImplementedError("Invalid difficulty")

    def get_statistics(self, difficulty: str) -> Dict[str, int]:
        self._check_difficulty(difficulty)
        return self._statistics[difficulty]

    def update_statistics(self, difficulty: str, won: bool) -> None:
        self._check_difficulty(difficulty)
        self._statistics[difficulty]["game_played"] += 1
        if won:
            self._statistics[difficulty]["game_won"] += 1
        self._save_data()

    def get_high_scores(self, difficulty: str) -> List[Tuple[int, str]]:
        self._check_difficulty(difficulty)
        return self._high_scores[difficulty]

    def update_high_scores(self, difficulty: str, time: int) -> None:
        self._check_difficulty(difficulty)

        clear_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self._high_scores[difficulty].append(HighScore(rank=sys.maxsize, clear_time=time, clear_date=clear_date))
        self._high_scores[difficulty].sort(key=lambda x: x.clear_time)

        for index, high_score in enumerate(self._high_scores[difficulty], start=1):
            self._high_scores[difficulty][index-1] = high_score._replace(rank=index)

        if len(self._high_scores[difficulty]) > MAX_HIGH_SCORE_ROW:
            self._high_scores[difficulty].pop()
        self._save_data()
        

    def _save_data(self, save_file_name: str=DEFAULT_SAVE_FILE) -> None:
        data = {
                "statistics": self._statistics,
                "high_scores": self._high_scores
             }
        try:
            with open(save_file_name, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def _load_data(self) -> None:
        try:
            with open(self._save_data_file, "r") as f:
                data = json.load(f)
                highscores = data["high_scores"]
                self._statistics = data["statistics"]

                for difficulty in DIFFICULTIES:
                    for row in highscores[difficulty]:
                        _high_score = HighScore(*row)
                        self._high_scores[difficulty].append(_high_score)
                pass
        except Exception as e:
            # print(e)
            # set default values
            self._statistics = defaultdict(lambda: defaultdict(int))
            self._high_scores = defaultdict(list)
        return

```
