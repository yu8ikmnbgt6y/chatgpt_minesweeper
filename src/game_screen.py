import tkinter as tk
from typing import Dict, Tuple
from grid import Grid
from timer import Timer


class GameScreen:
    ADJACENT_MINES_COLORS = {1: "blue", 2: "green", 3: "red", 4: "dark blue",
                              5: "maroon", 6: "cyan", 7: "black", 8: "gray"}

    DIFFICULTY_SETTINGS = {
        "beginner": (9, 9, 10),
        "intermediate": (16, 16, 40),
        "advanced": (16, 30, 99)
    }

    def __init__(self, root, difficulty: str):
        self.root = root
        self.master = tk.Toplevel(self.root)
        self.canvas = tk.Canvas(self.master)
        self.score_label = tk.Label(self.master)
        self.timer_label = tk.Label(self.master)
        self.grid = Grid(self, *self.DIFFICULTY_SETTINGS[difficulty])
        self.timer = Timer(self)

    def create_ui_elements(self):
        pass

    def update_score_label(self, score: int):
        pass

    def update_timer_label(self, time: int):
        pass

    def draw_cell(self, x: int, y: int, color: str, text: str):
        pass

    def handle_left_click(self, event):
        pass

    def handle_right_click(self, event):
        pass

    def show_game_over(self, result: str, time: int):
        pass