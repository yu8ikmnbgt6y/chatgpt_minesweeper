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
        
        self.start_screen = None
        self.game_screen = None
        self.game_statistics_window = GameStatisticsWindow(root=self.root)
        self.scoreboard = ScoreBoard()

        self._create_menu()

        self.root.grid()
        # create 4x3 Grid
        for i in range(3):
            for j in range(4):
                #label = tk.Label(self._root, text=f"({i},{j})", bg="lightgray", padx=10, pady=10)
                label = tk.Label(self.root)
                label.grid(row=i, column=j, sticky='nsew')

        # Set weights for StartScreen
        for i in range(3):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)
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
            self.start_screen.release_ui()
            self.start_screen = None
        if self.game_screen:
            self.game_screen.release_ui()
            # self.game_screen.destroy()
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
        if self.start_screen:
            self.root.mainloop()



##-----test
app = Interface()
app.start()
# app.root.mainloop()