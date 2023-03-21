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
        self.start_screen = StartScreen(root=self.root, initialize_game_callback=self._initialize_game)
        # self.game_screen = GameScreen(root=self.root)
        self.game_statistics_window = GameStatisticsWindow(root=self.root)

        callback_method_dict = {
            "difficulty": self._initialize_game,
            "statistics": self._show_statistics,
            "exit": self.root.quit
        }    
        self.menu = Menu(root=self.root, callback_method_dict=callback_method_dict)
        menu_bar = self.menu.create_menu()
        self.root.config(menu=menu_bar)
        self.scoreboard = ScoreBoard()

    def _initialize_game(self, difficulty: str):
        print(f"START_GAME: with difficulty {difficulty}")
        print("Not Implemented")
        #self.game_screen = GameScreen(difficulty)
    
    def _show_statistics(self):
        self.game_statistics_window.show_statistics(self.scoreboard)


    def start(self):
        self.start_screen.pack()
        self.root.mainloop()



##-----test
app = Interface()
app.start()
