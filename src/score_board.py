import json
from typing import Dict, List, Tuple

class ScoreBoard:
    def __init__(self):
        self.statistics = {
            "beginner": {"games_played": 0, "games_won": 0, "win_percentage": 0},
            "intermediate": {"games_played": 0, "games_won": 0, "win_percentage": 0},
            "advanced": {"games_played": 0, "games_won": 0, "win_percentage": 0},
        }
        self.high_scores = {"beginner": [], "intermediate": [], "advanced": []}
        self.load_data()

    def _check_difficulty(self, difficulty: str) -> None:
        if difficulty not in ["beginner", "intermediate", "advanced"]:
            raise NotImplementedError("Invalid difficulty")

    def get_statistics(self, difficulty: str) -> Dict[str, int]:
        self._check_difficulty(difficulty)
        return self.statistics[difficulty]

    def update_statistics(self, difficulty: str, won: bool) -> None:
        self._check_difficulty(difficulty)
        self.statistics[difficulty]["games_played"] += 1
        if won:
            self.statistics[difficulty]["games_won"] += 1
        self.statistics[difficulty]["win_percentage"] = int(
            self.statistics[difficulty]["games_won"] / self.statistics[difficulty]["games_played"] * 100
        )

    def get_high_scores(self, difficulty: str) -> List[Tuple[int, str]]:
        self._check_difficulty(difficulty)
        return self.high_scores[difficulty]

    def update_high_scores(self, difficulty: str, time: int, timestamp: str) -> None:
        self._check_difficulty(difficulty)
        self.high_scores[difficulty].append((time, timestamp))
        self.high_scores[difficulty].sort(key=lambda x: x[0])
        if len(self.high_scores[difficulty]) > 10:
            self.high_scores[difficulty].pop()

    def save_data(self) -> None:
        data = {"statistics": self.statistics, "high_scores": self.high_scores}
        try:
            with open("save_data.json", "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self) -> None:
        try:
            with open("save_data.json", "r") as f:
                data = json.load(f)
                self.statistics = data["statistics"]
                self.high_scores = data["high_scores"]
        except FileNotFoundError:
            pass
