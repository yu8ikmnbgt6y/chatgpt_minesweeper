import tkinter as tk
from tkinter import ttk
from typing import List
from scoreboard import ScoreBoard, DIFFICULTIES, HighScore

class GameStatisticsWindow:
    def __init__(self, root):
        self._root = root
        self._statistics_window = None

    def show_statistics(self, scoreboard: ScoreBoard):
        if self._statistics_window is not None:
            self._statistics_window.destroy()

        self._statistics_window = tk.Toplevel(self._root)
        self._statistics_window.geometry("1000x800")
        self._statistics_window.title("Game Statistics")
        header_labels = ["Rank", "Time (seconds)", "Date"]

        # SCORE TABLE BLOCK
        current_column = 0
        for level in DIFFICULTIES:
            level_label = tk.Label(self._statistics_window, text=level.capitalize(), font=("Helvetica", 10, "bold"))
            level_label.grid(row=0, column=current_column, padx=10, pady=5, columnspan=3)

            for col, header_text in enumerate(header_labels):
                header_label = tk.Label(self._statistics_window, text=header_text, font=("Helvetica", 10, "bold"))
                header_label.grid(row=1, column=current_column + col, padx=10, pady=5)

            scores: List[HighScore] = scoreboard.get_high_scores(difficulty=level)
            max_row = 0
            for row, high_score in enumerate(scores, start=2):
                rank = high_score.rank
                clear_time = high_score.clear_time
                clear_date = high_score.clear_date

                rank_label = tk.Label(self._statistics_window, text=rank)
                rank_label.grid(row=row, column=current_column, padx=10, pady=5)

                time_label = tk.Label(self._statistics_window, text=clear_time)
                time_label.grid(row=row, column=current_column + 1, padx=10, pady=5)

                date_label = tk.Label(self._statistics_window, text=clear_date)
                date_label.grid(row=row, column=current_column + 2, padx=10, pady=5)
                if row > max_row:
                    max_row = row

            separator = ttk.Separator(self._statistics_window, orient='vertical')
            separator.grid(row=1, column=current_column + 3, rowspan=11, padx=10, pady=5, sticky='ns')

            current_column += 4  # Add space between levels

        separator = ttk.Separator(self._statistics_window, orient="horizontal")
        separator.grid(row=13, column=0, padx=10, pady=10, columnspan=14, sticky="ew")

        # WIN_RATE BLOCK
        win_rate_block_stats_row = 14
        current_column = 0
        for level in DIFFICULTIES:
            games_played = scoreboard.get_statistics(level)["game_played"]
            games_won = scoreboard.get_statistics(level)["game_won"]
            win_rate = (games_won / games_played) * 100 if games_played > 0 else 0

            games_played_label = tk.Label(self._statistics_window, text=f"play: {games_played}")
            games_played_label.grid(row=win_rate_block_stats_row, column=current_column, padx=10, pady=5, columnspan=3)

            games_won_label = tk.Label(self._statistics_window, text=f"win: {games_won}")
            games_won_label.grid(row=win_rate_block_stats_row + 1, column=current_column, padx=10, pady=5, columnspan=3)

            win_rate_label = tk.Label(self._statistics_window, text=f"win_rate: {win_rate:.2f}%")
            win_rate_label.grid(row=win_rate_block_stats_row + 2, column=current_column, padx=10, pady=5, columnspan=3)

            separator = ttk.Separator(self._statistics_window, orient='vertical')
            separator.grid(row=win_rate_block_stats_row, column=current_column + 3, rowspan=3, padx=10, pady=5, sticky='ns')

            current_column += 4  # Add space between levels
