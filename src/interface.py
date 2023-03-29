import asyncio
import tkinter as tk

from scoreboard import ScoreBoard
from screen_game import GameScreen, TkinterAsyncEventLoop
from screen_menu import Menu
from screen_start import StartScreen
from window_chat import ChatWindow
from window_game_statistics import GameStatisticsWindow


class Interface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("MinesweeperGame")
        event_loop = TkinterAsyncEventLoop(self.root)
        asyncio.set_event_loop(event_loop)
        
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

        self.chat_app = None
        self.chat_button = tk.Button(self.root, text="Launch Chat", command=self._launch_chat_window)
        self.chat_button.grid(row=3, column=1, sticky='nsew')

        self._create_start_screen()
        self._launch_chat_window()
        event_loop.run_forever()
       
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
        
        self.game_screen = GameScreen(
            root=self.root,
            difficulty=difficulty,
            scoreboard=self.scoreboard,
            chat_app=self.chat_app
            )

    def _show_statistics(self):
        self.game_statistics_window.show_statistics(self.scoreboard)

    def _launch_chat_window(self):
        if not hasattr(self, "chat_app") or self.chat_app is None:
            self.chat_window_root = tk.Toplevel(self.root)
            self.chat_window_root.title("ChatGPT")
            main_window_x, main_window_y = self.root.winfo_x(), self.root.winfo_y()
            self.chat_window_root.geometry(f"+{main_window_x + 400}+{main_window_y + 50}")
        
            self.chat_app = ChatWindow(self.chat_window_root)
            self.chat_window_root.protocol("WM_DELETE_WINDOW", self._close_chat_window)
        else:
            self.chat_app.root.focus()
    
    def _close_chat_window(self):
        self.chat_app = None
        self.chat_window_root.destroy()


    def start(self):       
        if self.start_screen:
            self.root.mainloop()


if __name__ == "__main__":
    app = Interface()
    app.start()
