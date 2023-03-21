import json
import random
from datetime import datetime, timedelta

def create_high_scores():
    high_scores = []
    clear_time = random.randint(60, 500)
    for rank in range(1, 11):
        high_score = {
            "rank": rank,
            "clear_time": clear_time,
            "clear_date": (datetime.now() - timedelta(days=random.randint(0, 100))).strftime("%Y-%m-%d %H:%M")
        }
        high_scores.append(high_score)
        clear_time += random.randint(1, 10)
    return high_scores

def create_statistics():
    game_played = random.randint(1, 2000)
    game_won = random.randint(0, game_played)
    return {"game_played": game_played, "game_won": game_won}

sample_data = {
    "statistics": {
        "beginner": create_statistics(),
        "intermediate": create_statistics(),
        "advanced": create_statistics()
    },
    "high_scores": {
        "beginner": create_high_scores(),
        "intermediate": create_high_scores(),
        "advanced": create_high_scores()
    }
}

with open("sample_savedata.json", "w") as outfile:
    json.dump(sample_data, outfile, indent=4)
