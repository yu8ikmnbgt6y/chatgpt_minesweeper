import json
from typing import Dict, List, Tuple

class ScoreBoard:
    def __init__(self, save_data_file: str = "save_data.json"):
        self._save_data_file = save_data_file
        self._statistics = {
            "beginner": {"games_played": 0, "games_won": 0},
            "intermediate": {"games_played": 0, "games_won": 0},
            "advanced": {"games_played": 0, "games_won": 0},
        }
        self._high_scores = {"beginner": [], "intermediate": [], "advanced": []}
        self._load_data()


    def _check_difficulty(self, difficulty: str) -> None:
        if difficulty not in ["beginner", "intermediate", "advanced"]:
            raise NotImplementedError("Invalid difficulty")

    def get_statistics(self, difficulty: str) -> Dict[str, int]:
        self._check_difficulty(difficulty)
        return self._statistics[difficulty]

    def update_statistics(self, difficulty: str, won: bool) -> None:
        self._check_difficulty(difficulty)
        self._statistics[difficulty]["games_played"] += 1
        if won:
            self._statistics[difficulty]["games_won"] += 1

    def get_high_scores(self, difficulty: str) -> List[Tuple[int, str]]:
        self._check_difficulty(difficulty)
        return self._high_scores[difficulty]

    def update_high_scores(self, difficulty: str, time: int, timestamp: str) -> None:
        self._check_difficulty(difficulty)
        self._high_scores[difficulty].append((time, timestamp))
        self._high_scores[difficulty].sort(key=lambda x: x[0])
        if len(self._high_scores[difficulty]) > 10:
            self._high_scores[difficulty].pop()

    def _save_data(self) -> None:
        data = {"statistics": self._statistics, "high_scores": self._high_scores}
        try:
            with open("save_data.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def _load_data(self) -> None:
        try:
            with open(self._save_data_file, "r") as f:
                data = json.load(f)
                self._statistics = data["statistics"]
                self._high_scores = data["high_scores"]
        except:
            pass
