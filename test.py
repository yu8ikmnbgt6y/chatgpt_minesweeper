import tkinter as tk
from tkinter import Menu

class MyMenu(Menu):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.create_file_menu()
        self.create_edit_menu()
        self.create_view_menu()

    def create_file_menu(self):
        self.file_menu = Menu(self, tearoff=0)
        self.add_cascade(label="File", menu=self.file_menu)

        self.file_menu.add_command(label="New", command=lambda: print("New file"))
        self.file_menu.add_command(label="Open", command=lambda: print("Open file"))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.parent.quit)

    def create_edit_menu(self):
        self.edit_menu = Menu(self, tearoff=0)
        self.add_cascade(label="Edit", menu=self.edit_menu)

        self.edit_menu.add_command(label="Undo", command=lambda: print("Undo"))
        self.edit_menu.add_command(label="Redo", command=lambda: print("Redo"))

    def create_view_menu(self):
        self.view_menu = Menu(self, tearoff=0)
        self.add_cascade(label="View", menu=self.view_menu)

        self.view_menu.add_command(label="Zoom In", command=lambda: print("Zoom In"))
        self.view_menu.add_command(label="Zoom Out", command=lambda: print("Zoom Out"))

class MyInterface(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("My GUI Program")
        self.create_menu()

    def create_menu(self):
        self.main_menu = MyMenu(self)
        self.config(menu=self.main_menu)

if __name__ == "__main__":
    app = MyInterface()
    app.mainloop()
