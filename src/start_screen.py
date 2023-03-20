import tkinter as tk
from tkinter import ttk

class StartScreen(tk.Frame):
    def __init__(self, root, initialize_game_callback):
        super().__init__(root)
        self.initialize_game_callback = initialize_game_callback
        self.setup_ui()

    def setup_ui(self):
        self.pack(expand=True)

        self.title_label = tk.Label(self, text="Minesweeper", font=("Helvetica", 24))
        self.title_label.pack(pady=(50, 20))

        self.difficulty_var = tk.StringVar()
        self.difficulty_menu = ttk.Combobox(self, textvariable=self.difficulty_var, state="readonly")
        self.difficulty_menu["values"] = ("beginner", "intermediate", "advanced")
        self.difficulty_menu.current(0)
        self.difficulty_menu.pack(pady=10)

        self.start_button = tk.Button(self, text="Start Game", command=self.start_game)
        self.start_button.pack(pady=10)

    def start_game(self):
        difficulty = self.difficulty_var.get()
        self.initialize_game_callback(difficulty)