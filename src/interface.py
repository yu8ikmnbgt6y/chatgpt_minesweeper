import tkinter as tk
from start_screen import StartScreen
from game_screen import GameScreen
from game_statistics_window import GameStatisticsWindow
from menu import Menu
from scoreboard import ScoreBoard


class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MinesweeperGame")
        self.root.geometry("300x300")
        self.start_screen = StartScreen(root=self.root, initialize_game_callback=self.initialize_game)
        # self.game_screen = GameScreen(root=self.root)
        # self.game_statistics_window = GameStatisticsWindow(root=self.root)
        # self.menu = Menu(root=self.root)
        self.scoreboard = ScoreBoard()

    def initialize_game(self, difficulty: str):
        print("START_GAME")
        print("Not Implemented")
        #self.game_screen = GameScreen(difficulty)

    def start(self):
        self.start_screen.pack()
        self.root.mainloop()



##-----test
app = Interface()
app.start()
