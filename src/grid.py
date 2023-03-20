import random
from collections import deque
from typing import List, Tuple
from cell import Cell


class Grid:
    def __init__(self, rows: int, cols: int, mines: int):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.cells = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.mine_opened = False

    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.rows and 0 <= col < self.cols

    def initialize_grid(self, first_click_row: int, first_click_col: int):
        self.place_mines(first_click_row, first_click_col)
        self.calculate_adjacent_mines()

    def place_mines(self, exclude_row: int, exclude_col: int):
        mines_placed = 0
        while mines_placed < self.mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not (row == exclude_row and col == exclude_col) and not self.cells[row][col].is_mine:
                self.cells[row][col].put_mine()
                mines_placed += 1

    def calculate_adjacent_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.cells[row][col].is_mine:
                    adjacent_mines = 0
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            r, c = row + dr, col + dc
                            if 0 <= r < self.rows and 0 <= c < self.cols and self.cells[r][c].is_mine:
                                adjacent_mines += 1
                    self.cells[row][col].set_adjacent_mines(adjacent_mines)


    def open_cell(self, row: int, col: int) -> Tuple[bool, List[Tuple[int, int]]]:
        cell = self.cells[row][col]
        cell.open()

        if cell.is_mine:
            self.mine_opened = True
            return True, []

        opened_cells = [(row, col)]
        queue = deque([(row, col)])

        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        while queue:
            cur_row, cur_col = queue.popleft()
            if self.cells[cur_row][cur_col].adjacent_mines != 0:
                continue

            for dr, dc in directions:
                r, c = cur_row + dr, cur_col + dc
                if self.in_bounds(r, c):
                    this_cell = self.cells[r][c]
                    if not this_cell.is_open and not this_cell.is_mine:
                        this_cell.open()
                        opened_cells.append((r, c))
                        if this_cell.adjacent_mines == 0 and (r, c) not in queue:
                            queue.append((r, c))

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
    
    def print_opened_cells(self):
        grid_representation = ""
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.cells[row][col]
                if not cell.is_open:
                    grid_representation += '?'
                elif cell.is_mine:
                    grid_representation += 'X'
                elif cell.adjacent_mines == 0:
                    grid_representation += ' '
                else:
                    grid_representation += str(cell.adjacent_mines)
                grid_representation += ' '
            grid_representation += '\n'
        print(grid_representation)

    def __str__(self):
            grid_representation = []
            for row in range(self.rows):
                row_representation = []
                for col in range(self.cols):
                    if self.cells[row][col].is_mine:
                        row_representation.append('X')
                    else:
                        row_representation.append(str(self.cells[row][col].adjacent_mines))
                grid_representation.append(''.join(row_representation))
            return '\n'.join(grid_representation)
