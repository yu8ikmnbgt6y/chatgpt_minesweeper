import tkinter as tk
from tkinter import ttk
from typing import List
from scoreboard import ScoreBoard, DIFFICULTIES, HighScore, MAX_HIGH_SCORE_ROW

class GameStatisticsWindow:
    def __init__(self, root):
        self._root = root
        self._statistics_window = None

    def show_statistics(self, scoreboard: ScoreBoard):
        if self._statistics_window is not None:
            self._statistics_window.destroy()

        self._statistics_window = tk.Toplevel(self._root)
        self._statistics_window.title("Game Statistics")
        self._statistics_window.resizable(False, False)

        # DIFFICULTY LABELS
        for i, level in enumerate(DIFFICULTIES):
            level_label = tk.Label(self._statistics_window, text=level.capitalize(), font=("Helvetica", 10, "bold"))
            level_label.grid(row=0, column=i, padx=10, pady=5)

        # HIGH SCORE TABLES
        for i, level in enumerate(DIFFICULTIES):
            tree = ttk.Treeview(self._statistics_window, columns=("Rank", "Time", "Date"), show="headings")
            tree.column("Rank", width=40, anchor="center")
            tree.column("Time", width=80, anchor="center")
            tree.column("Date", width=150, anchor="center")
            tree.heading("Rank", text="Rank")
            tree.heading("Time", text="Time(sec)")
            tree.heading("Date", text="Date")
            tree.grid(row=1, column=i, padx=10, pady=5)

            scores: List[HighScore] = scoreboard.get_high_scores(difficulty=level)
            for high_score in scores[:MAX_HIGH_SCORE_ROW]:
                rank = high_score.rank
                clear_time = high_score.clear_time
                clear_date = high_score.clear_date
                tree.insert("", "end", values=(rank, clear_time, clear_date))

        # WIN RATE INFORMATION
        for i, level in enumerate(DIFFICULTIES):
            frame = tk.Frame(self._statistics_window)
            frame.grid(row=2, column=i, padx=10, pady=5)

            games_played = scoreboard.get_statistics(level)["game_played"]
            games_won = scoreboard.get_statistics(level)["game_won"]
            win_rate = (games_won / games_played) * 100 if games_played > 0 else 0

            games_played_label = tk.Label(frame, text=f"play: {games_played}")
            games_played_label.pack(side="top", padx=10, pady=5)

            games_won_label = tk.Label(frame, text=f"win: {games_won}")
            games_won_label.pack(side="top", padx=10, pady=5)

            win_rate_label = tk.Label(frame, text=f"win_rate: {win_rate:.2f}%")
            win_rate_label.pack(side="top", padx=10, pady=5)

        self._statistics_window.update_idletasks()
        width, height = self._statistics_window.winfo_reqwidth(), self._statistics_window.winfo_reqheight()
        self._statistics_window.geometry(f"{width}x{height}")
