import tkinter as tk

class StartScreen(tk.Frame):
    def __init__(self, root=None, **kwargs):
        super().__init__(root, **kwargs)
        
        self.label = tk.Label(self, text="Welcome to the game!")
        self.label.pack()
