import tkinter as tk
from start_screen import StartScreen
from game_screen import GameScreen
from game_statistics_window import GameStatisticsWindow
from menu import Menu
from scoreboard import ScoreBoard


class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.start_screen = StartScreen()
        self.game_screen = GameScreen()
        self.game_statistics_window = GameStatisticsWindow()
        self.menu = Menu()
        self.scoreboard = ScoreBoard()

    def initialize_game(self, difficulty: str):
        self.game_screen = GameScreen(difficulty)

    def start(self):
        self.start_screen.pack()
        self.root.mainloop()
