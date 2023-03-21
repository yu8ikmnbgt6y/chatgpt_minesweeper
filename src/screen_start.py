import tkinter as tk
from tkinter import ttk

class StartScreen(tk.Frame):
    def __init__(self, root, initialize_game_callback):
        super().__init__(root)
        self._initialize_game_callback = initialize_game_callback
        self._setup_ui()

    def _setup_ui(self):
        self.pack(expand=True)

        self._title_label = tk.Label(self, text="Minesweeper", font=("Helvetica", 24))
        self._title_label.pack(pady=(50, 20))

        self._difficulty_var = tk.StringVar()
        self._difficulty_menu = ttk.Combobox(self, textvariable=self._difficulty_var, state="readonly")
        self._difficulty_menu["values"] = ("beginner", "intermediate", "advanced")
        self._difficulty_menu.current(0)
        self._difficulty_menu.pack(pady=10)

        self._start_button = tk.Button(self, text="Start Game", command=self._start_game)
        self._start_button.pack(pady=10)

    def _start_game(self):
        difficulty = self._difficulty_var.get()
        self._initialize_game_callback(difficulty)
