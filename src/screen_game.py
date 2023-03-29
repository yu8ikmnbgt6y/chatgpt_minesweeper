import asyncio
import tkinter as tk
from datetime import timedelta
from typing import Dict, Tuple

from cell import Cell
from minesweeper_grid import (MinesweeperGrid, TooManyFlagsError,
                              UnavailableCellError)
from scoreboard import ScoreBoard
from timer import Timer
from window_chat import ChatWindow

CELL_COLOR_BASE = "gray"
CELL_COLOR_OPENED = "white"
CELL_COLOR_MINE = "black"

def has_attr_and_not_none(obj, attr_name):
    return hasattr(obj, attr_name) and getattr(obj, attr_name) is not None

class TkinterAsyncEventLoop(asyncio.AbstractEventLoop):
    def __init__(self, root):
        self.root = root
        self._ready = []
        self._stopping = False

    def run_forever(self):
        while not self._stopping:
            self.root.update()
            while self._ready:
                self._ready.pop(0)()

    def stop(self):
        self._stopping = True

    def create_task(self, coro):
        def wrapped_coro():
            try:
                coro.send(None)
            except StopIteration:
                pass
            else:
                self._ready.append(wrapped_coro)
        self._ready.append(wrapped_coro)

    def call_soon(self, callback, *args):
        self._ready.append(lambda: callback(*args))

    def call_later(self, delay, callback, *args):
        self.root.after(int(delay * 1000), lambda: self.call_soon(callback, *args))

    def call_at(self, when, callback, *args):
        now = self.time()
        delay = when - now
        return self.call_later(delay, callback, *args)

    def time(self):
        return self.root.tk.call('after', 'info')

    def run_in_executor(self, executor, func, *args, **kwargs):
        return asyncio.wrap_future(executor.submit(func, *args, **kwargs))


class GameScreen():
    ADJACENT_MINES_COLORS = {1: "blue", 2: "green", 3: "red", 4: "dark blue",
                              5: "maroon", 6: "cyan", 7: "black", 8: "gray"}

    DIFFICULTY_SETTINGS = {
        "beginner": (9, 9, 10),
        # "beginner": (4, 4, 2),
        "intermediate": (16, 16, 40),
        "advanced": (16, 30, 99)
    }

    def __init__(self, root, difficulty: str, scoreboard: ScoreBoard, chat_app:ChatWindow):
        self.release_ui()

        self.root: tk.Tk = root
        # Top Level
        self.frame_top = tk.Frame()
        self.score_label = tk.Label(self.frame_top)
        self.flagged_label = tk.Label(self.frame_top)
        self.timer_label = tk.Label(self.frame_top)
        # Message Level
        self.frame_message = tk.Frame()
        self.message_label = tk.Label(self.frame_message, fg="red")

        # Minesweeper Grid Level
        self.canvas = tk.Canvas(self.root)
        rows, cols, mines = self.DIFFICULTY_SETTINGS[difficulty]
        self.minesweeper_grid = MinesweeperGrid(rows=rows, cols=cols, mines=mines)

        self.timer = Timer()

        self.chat_app = chat_app

        # parameters
        self._font_size = int(self.minesweeper_grid.cell_pixel_size * 0.6)
        self._font = ("Arial", self._font_size)
        self._on_game = True
        self._message_count = 0
        self._difficulty = difficulty

        self.scoreboard: ScoreBoard = scoreboard

        self._create_ui_elements()

    def _create_ui_elements(self):
        # Information
        self.score_label.pack(side=tk.LEFT, padx=10)
        self.flagged_label.pack(side=tk.LEFT, padx=10)
        self.timer_label.pack(side=tk.LEFT, padx=10)
        self.frame_top.grid(column=1, row=0)

        self.message_label.pack()
        self.frame_message.grid(column=1, row=1)

        # Minesweeper Grid
        self.canvas.bind("<Button-1>", self.handle_left_click)
        self.canvas.bind("<Button-3>", self.handle_right_click)
        self.canvas.config(width=self.minesweeper_grid.grid_width, height=self.minesweeper_grid.grid_height)
        self.canvas.grid(column=1, row=2)

        self.initialize_grid_view()
        self._update_screen()

    def release_ui(self):
        if has_attr_and_not_none(self, "score_label"):
            self.score_label.pack_forget()
        if has_attr_and_not_none(self, "flagged_labe"):
            self.flagged_label.pack_forget()
        if has_attr_and_not_none(self, "timer_label"):
            self.timer_label.pack_forget()
        if has_attr_and_not_none(self, "frame_top"):
            self.frame_top.grid_forget()

        if has_attr_and_not_none(self, "message_label"):
            self.message_label.pack_forget()
        if has_attr_and_not_none(self, "frame_message"):
            self.frame_message.grid_forget()

        if has_attr_and_not_none(self, "canvas"):
            self.canvas.unbind("<Button-1>")
            self.canvas.unbind("<Button-3>")
            self.canvas.config()
            self.canvas.grid_forget()

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
                self.canvas.create_text(center_x, center_y, text="B", fill="white", font=self._font)
            else:
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=CELL_COLOR_OPENED, outline="gray")
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

    async def update_game_status_on_message_async(self, game_status_dict: Dict):
        await self.chat_app.update_game_status_on_message_async(game_status_dict=game_status_dict)

    async def send_message_from_game_screen_async(self, game_status_dict):
        await self.chat_app.send_message_from_game_screen_async(game_status_dict=game_status_dict)

    def handle_left_click(self, event):
        #print("left button clicked")
        if not self._on_game:
            return
        in_range, row, col = self._safe_get_clicked_cell(event)
        if not in_range:
            #print("out of range")
            return
        
        # First Click
        if not self.minesweeper_grid.initialized:
            self.minesweeper_grid.initialize_grid(row, col)
            self.timer.start()
            self.update_timer()

        cell: Cell = self.minesweeper_grid.cells[row][col]
        if cell.is_flagged or cell.is_open:  # if the cell has been already flagged or opened, do nothing.
            return
       
        mine_hit, opened_cells = self.minesweeper_grid.open_cell(row, col)

        for cell in opened_cells:
            self.draw_cell(cell)

        self._update_screen()
        
        game_status_dict: Dict = self.minesweeper_grid.create_game_status()

        game_status = game_status_dict["game_status"]

        if game_status == "ongoing":
            self._message_count += 1
            if self._message_count % 10 == 1:
                asyncio.get_event_loop().create_task(
                    self.send_message_from_game_screen_async(game_status_dict=game_status_dict)
                    )
            else:
                asyncio.get_event_loop().create_task(
                    self.update_game_status_on_message_async(game_status_dict=game_status_dict)
                )
        else:
            asyncio.get_event_loop().create_task(
                self.send_message_from_game_screen_async(game_status_dict=game_status_dict)
                )
            self._finalize_game(game_status=game_status)
        
    def update_timer(self):
        if self.timer.running:
            elapsed_time = int(self.timer.get_elapsed_time())
            formatted_time = str(timedelta(seconds=elapsed_time))
            self.timer_label.config(text=f"Time: {formatted_time}")
            self.root.after(1000, self.update_timer)

    def handle_right_click(self, event):
        #print("right button clicked")
        if not self._on_game:
            return
        in_range, row, col = self._safe_get_clicked_cell(event)
        if not in_range:
            return
        #print(f"grid {row}, {col}")

        try:
            cell = self.minesweeper_grid.flag_cell(row=row, col=col)
        except TooManyFlagsError:
            #print("over flagged")
            x, y = self.root.winfo_x(), self.root.winfo_y()

            dialog = tk.Toplevel(self.root)
            dialog.transient(self.root)
            dialog.grab_set()

            label1 = tk.Label(dialog, text="TOO MANY FLAGS", fg="red")
            label2 = tk.Label(dialog, text="You cannot place more flags than predicted mines.") 
            label1.pack()
            label2.pack()

            def close_dialog():
                dialog.grab_release()
                dialog.destroy()
            
            ok_button = tk.Button(dialog, text="OK", command=close_dialog)

            dialog.geometry(f"+{x+40}+{y+40}")
            ok_button.pack(pady=(0,20))
            return
        except UnavailableCellError as e:
            #print(e)
            return

        self.draw_cell(cell=cell)
        self._update_screen()

        game_status_dict: Dict = self.minesweeper_grid.create_game_status()
        game_status = game_status_dict["game_status"]

        if game_status == "ongoing":                
            asyncio.get_event_loop().create_task(
                self.update_game_status_on_message_async(game_status_dict=game_status_dict)
            )
        else:
            self._finalize_game(game_status=game_status)

    def _update_screen(self):
        self.score_label.config(text=f"Mine: {self.minesweeper_grid.n_mines}")
        self.flagged_label.config(text=f"Flag: {self.minesweeper_grid.n_flagged}")


    def _finalize_game(self, game_status: str):
        self.timer.stop()
        self._on_game = False
        won = (game_status == "won")
        
        # Update the scoreboard
        self.scoreboard.update_statistics(self._difficulty, won=won)

        # Check for high score and update if necessary
        if won:
            time_elapsed = self.timer.get_elapsed_time()
            self.scoreboard.update_high_scores(self._difficulty, time=int(time_elapsed))
            self.message_label.config(text="Congratulations!, You won the game!")
        else:
            # game_status == "lost":
            self.message_label.config(text="You lost! Game Over")
