import tkinter as tk
from typing import Dict, Tuple
from grid import Grid
from timer import Timer


class GameScreen(tk.Frame):
    ADJACENT_MINES_COLORS = {1: "blue", 2: "green", 3: "red", 4: "dark blue",
                              5: "maroon", 6: "cyan", 7: "black", 8: "gray"}

    DIFFICULTY_SETTINGS = {
        "beginner": (9, 9, 10),
        "intermediate": (16, 16, 40),
        "advanced": (16, 30, 99)
    }

    def __init__(self, root, difficulty: str):
        super().__init__(root)
        self.root = root
        self.canvas = tk.Canvas(self.root)
        self.score_label = tk.Label(self.root)
        self.timer_label = tk.Label(self.root)

        rows, cols, mines = self.DIFFICULTY_SETTINGS[difficulty]
        self.grid = Grid(rows=rows, cols=cols, mines=mines)
        self.timer = Timer()
        self._create_ui_elements()

    def _create_ui_elements(self):
        self.root.title("Minesweeper")

        self.canvas.config(width=self.grid.grid_width, height=self.grid.grid_height)
        self.canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.handle_left_click)
        self.canvas.bind("<Button-3>", self.handle_right_click)

        self.score_label.config(text=f"Mines: {self.grid.mines_remaining}")
        self.score_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.timer_label.config(text=f"Time: {self.timer.get_elapsed_time()}s")
        self.timer_label.grid(row=0, column=1, padx=10, pady=5, sticky="e")
        # self.grid.draw()

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