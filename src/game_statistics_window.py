import tkinter as tk
from scoreboard import ScoreBoard

class GameStatisticsWindow:
    def __init__(self, root):
        self._root = root
        self._statistics_window = None

    def show_statistics(self, scoreboard: ScoreBoard):
        if self._statistics_window is not None:
            self._statistics_window.destroy()

        self._statistics_window = tk.Toplevel(self._root)
        self._statistics_window.geometry("900x500")
        self._statistics_window.title("Game Statistics")

        levels = ["beginner", "intermediate", "advanced"]
        header_labels = ["Rank", "Time (seconds)", "Date"]

        current_column = 0
        for level in levels:
            level_label = tk.Label(self._statistics_window, text=level.capitalize(), font=("Helvetica", 10, "bold"))
            level_label.grid(row=0, column=current_column, padx=10, pady=5, columnspan=3)

            for col, header_text in enumerate(header_labels):
                header_label = tk.Label(self._statistics_window, text=header_text, font=("Helvetica", 10, "bold"))
                header_label.grid(row=1, column=current_column + col, padx=10, pady=5)

            scores = scoreboard.get_high_scores(difficulty=level)
            for row, high_score in enumerate(scores, start=2):
                rank = high_score["rank"]
                clear_time = high_score["clear_time"]
                clear_date = high_score["clear_date"]

                rank_label = tk.Label(self._statistics_window, text=rank)
                rank_label.grid(row=row, column=current_column, padx=10, pady=5)

                time_label = tk.Label(self._statistics_window, text=clear_time)
                time_label.grid(row=row, column=current_column + 1, padx=10, pady=5)

                date_label = tk.Label(self._statistics_window, text=clear_date)
                date_label.grid(row=row, column=current_column + 2, padx=10, pady=5)

            current_column += 4  # Add space between levels
