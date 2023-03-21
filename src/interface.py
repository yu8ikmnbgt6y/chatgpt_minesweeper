import tkinter as tk
from screen_start import StartScreen
from screen_game import GameScreen
from window_game_statistics import GameStatisticsWindow
from screen_menu import Menu
from scoreboard import ScoreBoard


class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MinesweeperGame")
        self.root.geometry("300x300")

        self.start_screen = None
        self.game_screen = None
        self.game_statistics_window = GameStatisticsWindow(root=self.root)
        self.scoreboard = ScoreBoard()

        self._create_menu()
        self._create_start_screen()
    
   
    def _create_menu(self):
        callback_method_dict = {
            "difficulty": self._create_game_screen,
            "statistics": self._show_statistics,
            "exit": self.root.quit
        }    
        self.menu = Menu(root=self.root, callback_method_dict=callback_method_dict)
        menu_bar = self.menu.create_menu()
        self.root.config(menu=menu_bar)     

    def _release_screens(self):
        if self.start_screen:
            self.start_screen.grid_forget()
            self.start_screen.destroy()
            self.start_screen = None
        if self.game_screen:
            self.game_screen.grid_forget()
            self.game_screen.destroy()
            self.game_screen = None
    
    def _create_start_screen(self):
        self._release_screens()
        self.start_screen = StartScreen(root=self.root, create_game_callback=self._create_game_screen)


    def _create_game_screen(self, difficulty: str):
        self._release_screens()
        self.game_screen = GameScreen(root=self.root, difficulty=difficulty, create_start_callback=self._create_start_screen)

    def _show_statistics(self):
        self.game_statistics_window.show_statistics(self.scoreboard)

    def start(self):
        self.start_screen.grid()
        self.root.mainloop()



##-----test
app = Interface()
app.start()
