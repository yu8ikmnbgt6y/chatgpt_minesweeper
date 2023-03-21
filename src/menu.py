import tkinter as tk

class Menu:
    def __init__(self, root, callback_method_dict):
        self._root = root
        self._callback_method_dict = callback_method_dict

    def create_menu(self):
        menu = tk.Menu(self._root)
        self._create_difficulty_menu(menu)
        self._create_game_statistics_menu(menu)
        self._create_exit_menu(menu)
        return menu

    def _create_difficulty_menu(self, menu):
        difficulty_menu = tk.Menu(menu, tearoff=0)
        difficulty_menu.add_command(label="beginner", command=lambda: self._callback_method_dict["difficulty"]("beginner"))
        difficulty_menu.add_command(label="intermediate", command=lambda: self._callback_method_dict["difficulty"]("intermediate"))
        difficulty_menu.add_command(label="advanced", command=lambda: self._callback_method_dict["difficulty"]("advanced"))
        menu.add_cascade(label="Difficulty", menu=difficulty_menu)

    def _create_game_statistics_menu(self, menu):
        menu.add_command(label="Statistics", command=self._callback_method_dict["statistics"])

    def _create_exit_menu(self, menu):
        menu.add_command(label="Exit", command=self._callback_method_dict["exit"])
