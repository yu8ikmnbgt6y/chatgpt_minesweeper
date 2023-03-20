from typing import Dict, List, Tuple

class ScoreBoard:
    def __init__(self):
        self.statistics = {
            "beginner": {"games_played": 0, "games_won": 0, "win_percentage": 0},
            "intermediate": {"games_played": 0, "games_won": 0, "win_percentage": 0},
            "advanced": {"games_played": 0, "games_won": 0, "win_percentage": 0},
        }
        self.high_scores = {"beginner": [], "intermediate": [], "advanced": []}

    def get_statistics(self) -> Dict[str, Dict[str, int]]:
        return self.statistics

    def update_statistics(self, difficulty: str, won: bool) -> None:
        self.statistics[difficulty]["games_played"] += 1
        if won:
            self.statistics[difficulty]["games_won"] += 1
        self.statistics[difficulty]["win_percentage"] = int(
            self.statistics[difficulty]["games_won"] / self.statistics[difficulty]["games_played"] * 100
        )

    def get_high_scores(self) -> Dict[str, List[Tuple[int, str]]]:
        return self.high_scores

    def update_high_scores(self, difficulty: str, time: int, timestamp: str) -> None:
        self.high_scores[difficulty].append((time, timestamp))
        self.high_scores[difficulty].sort(key=lambda x: x[0])
        if len(self.high_scores[difficulty]) > 10:
            self.high_scores[difficulty].pop()

    def save_data(self) -> None:
        # Save statistics and high_scores data to a file on disk

    def load_data(self) -> None:
        # Load statistics and high_scores data from a file on disk, if it exists
        # If the file does not exist, initialize the data with default values
