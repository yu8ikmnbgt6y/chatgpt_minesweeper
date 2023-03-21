import tkinter as tk
import tkinter.messagebox as messagebox
from typing import Dict, Tuple
from datetime import timedelta
from minesweeper_grid import MinesweeperGrid
from timer import Timer
from cell import Cell

CELL_COLOR_BASE = "gray"
CELL_COLOR_OPEND = "white"
CELL_COLOR_MINE = "black"

class GameScreen(tk.Frame):
    ADJACENT_MINES_COLORS = {1: "blue", 2: "green", 3: "red", 4: "dark blue",
                              5: "maroon", 6: "cyan", 7: "black", 8: "gray"}

    DIFFICULTY_SETTINGS = {
        "beginner": (9, 9, 10),
        "intermediate": (16, 16, 40),
        "advanced": (16, 30, 99)
    }

    def __init__(self, root, difficulty: str, create_start_callback):
        super().__init__(root)
        self.root = root
        self.canvas = tk.Canvas(self.root)
        self.score_label = tk.Label(self.root)
        self.flagged_label = tk.Label(self.root)
        self.timer_label = tk.Label(self.root)
        self.timer = Timer()

        rows, cols, mines = self.DIFFICULTY_SETTINGS[difficulty]
        self.minesweeper_grid = MinesweeperGrid(rows=rows, cols=cols, mines=mines)

        self._font_size = int(self.minesweeper_grid.cell_pixel_size * 0.6)
        self._font = ("Arial", self._font_size)

        self._popup_displayed = False
        self._return_start_callback = create_start_callback
        self._create_ui_elements()

    def _create_ui_elements(self):

        self.canvas.config(width=self.minesweeper_grid.grid_width, height=self.minesweeper_grid.grid_height)

        self.canvas.grid(row=1, column=0, columnspan=2, padx=10, pady=10)
        self.canvas.bind("<Button-1>", self.handle_left_click)
        self.canvas.bind("<Button-3>", self.handle_right_click)

        self.score_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.flagged_label.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        self.timer_label.grid(row=0, column=2, padx=10, pady=5, sticky="e")
        self.initialize_grid_view()
        self._update_screen()

    def _clear_ui_elements(self):
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Button-3>")
        self.canvas.grid_forget()
        self.score_label.grid_forget()
        self.flagged_label.grid_forget()
        self.timer_label.grid_forget()

    def initialize_grid_view(self):        
        for row in range(self.minesweeper_grid.n_rows):
            for col in range(self.minesweeper_grid.n_cols):
                cell = self.minesweeper_grid.cells[row][col]
                x1, x2, y1, y2 = cell.x1, cell.x2, cell.y1, cell.y2
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=CELL_COLOR_BASE, outline="black")

    def draw_cell(self, cell: Cell):
        x1, x2, y1, y2 = cell.x1, cell.x2, cell.y1, cell.y2
        center_x, center_y = cell.center_x, cell.center_y

        if cell.is_open:
            if cell.is_mine:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="red", outline="gray")
                self.canvas.create_text(center_x, center_y, text="B", fill="black", font=self._font)
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=CELL_COLOR_OPEND, outline="gray")
                if cell.adjacent_mines > 0:
                    color = self.ADJACENT_MINES_COLORS[cell.adjacent_mines]
                    self.canvas.create_text(center_x, center_y, text=str(cell.adjacent_mines), fill=color, font=self._font)
        else:
            if cell.is_flagged:
                self.canvas.create_text(center_x, center_y, text="F", fill="black", font=self._font)
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=CELL_COLOR_BASE, outline="black")


    def _safe_get_clicked_cell(self, event) -> Tuple[bool, int, int]:
        col = event.x // self.minesweeper_grid.cell_pixel_size
        row = event.y // self.minesweeper_grid.cell_pixel_size
        in_range = (0 <= col < self.minesweeper_grid.n_cols) and (0 <= row < self.minesweeper_grid.n_rows)
        return in_range, row, col


    def handle_left_click(self, event):
        print("left button clicked")
        in_range, row, col = self._safe_get_clicked_cell(event)
        if not in_range:
            print("out of range")
            return
        
        # First Click
        if not self.minesweeper_grid.initialized:
            self.minesweeper_grid.initialize_grid(row, col)
            self.timer.start()
            self.update_timer()

        cell: Cell = self.minesweeper_grid.cells[row][col]
        if cell.is_flagged or cell.is_open:  # if the cell has been already flagged or opened, do nothing.
            print("skip")
            return
        
        print(f"grid {row}, {col}")
        print(self.minesweeper_grid)
       
        mine_hit, opened_cells = self.minesweeper_grid.open_cell(row, col)
        if not mine_hit:
            for cell in opened_cells:
                self.draw_cell(cell)

        self._update_screen()
        game_status = self.minesweeper_grid.check_game_status()
        if not game_status == "ongoing":
            self._finalize_game(game_status=game_status)
        
    def update_timer(self):
        if self.timer.running:
            elapsed_time = int(self.timer.get_elapsed_time())
            formatted_time = str(timedelta(seconds=elapsed_time))
            self.timer_label.config(text=f"Time: {formatted_time}")
            self.root.after(1000, self.update_timer)

    def handle_right_click(self, event):
        print("right button clicked")
        in_range, row, col = self._safe_get_clicked_cell(event)
        if not in_range:
            return
        print(f"grid {row}, {col}")

        cell = self.minesweeper_grid.flag_cell(row=row, col=col)
        self.draw_cell(cell=cell)
        self._update_screen()


    def _update_screen(self):
        self.score_label.config(text=f"Mine: {self.minesweeper_grid.n_mines}")
        self.flagged_label.config(text=f"Flag: {self.minesweeper_grid.n_flagged}")


    def _finalize_game(self, game_status: str):
        if game_status == "lost":
            self.timer.stop()
            self.show_popup("Game Over", "You lost! Better luck next time.")
        elif game_status == "won":
            self.timer.stop()
            self.show_popup("Congratulations!", "You won the game!")


    def show_popup(self, title: str, message: str):
        if self._popup_displayed:
            return

        self._popup_displayed = True
        popup = tk.Toplevel(self.root)
        popup.title(title)
        popup.geometry("200x100")

        # Make the popup modal and disable the GameScreen
        popup.grab_set()

        label = tk.Label(popup, text=message)
        label.pack(pady=10)

        ok_button = tk.Button(popup, text="OK", command=lambda: self.close_popup(popup))
        ok_button.pack(pady=5)


    def close_popup(self, popup):
        popup.destroy()
        self._popup_displayed = False
        self._clear_ui_elements()
        self._return_start_callback()
