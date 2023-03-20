import random
from typing import List, Tuple
from cell import Cell

class Grid:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.cells = [[Cell(False) for _ in range(cols)] for _ in range(rows)]
        self.mine_opened = False

    def initialize_grid(self, first_click_row: int, first_click_col: int):
        self.place_mines(first_click_row, first_click_col)
        self.calculate_adjacent_mines()

    def place_mines(self, exclude_row: int, exclude_col: int):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not (row == exclude_row and col == exclude_col) and not self.cells[row][col].is_mine:
                self.cells[row][col]._is_mine = True
                mines_placed += 1

    def calculate_adjacent_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.cells[row][col].is_mine:
                    adjacent_mines = 0
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            r, c = row + dr, col + dc
                            if 0 <= r < self.rows and 0 <= c < self.cols and self.cells[r][c].is_mine:
                                adjacent_mines += 1
                    self.cells[row][col].set_adjacent_mines(adjacent_mines)

    def open_cell(self, row: int, col: int) -> Tuple[bool, List[Tuple[int, int]]]:
        cell = self.cells[row][col]
        cell.open()

        if cell.is_mine:
            return True, []

        opened_cells = [(row, col)]
        if cell.adjacent_mines == 0:
            for dr in range(-1, 2):
                for dc in range(-1, 2):
                    r, c = row + dr, col + dc
                    if 0 <= r < self.rows and 0 <= c < self.cols and not self.cells[r][c].is_open:
                        opened_cells.extend(self.open_cell(r, c)[1])

        return False, opened_cells

    def flag_cell(self, row: int, col: int) -> bool:
        cell = self.cells[row][col]
        cell.toggle_flag()
        return cell.flagged

    def check_game_status(self) -> str:
        if self.mine_opened:
            return "lost"

        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if not cell.is_mine and not cell.is_open:
                    return "ongoing"

        return "won"
