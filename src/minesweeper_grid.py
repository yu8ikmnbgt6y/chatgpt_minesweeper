import random
from collections import deque
from typing import List, Tuple
from cell import Cell

class TooManyFlagsError(Exception):
    def __init__(self, message="", extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info
class UnavailableCellError(Exception):
    def __init__(self, message="", extra_info=None):
        super().__init__(message)
        self.extra_info = extra_info


CELL_SIZE = 20 # pixel

class MinesweeperGrid:
    def __init__(self, rows: int, cols: int, mines: int):
        self.n_rows = rows
        self.n_cols = cols
        self.n_mines = mines
        self.cell_pixel_size = CELL_SIZE
        self.cells = [[Cell(row=row, col=col, cell_size=self.cell_pixel_size) for col in range(cols)] for row in range(rows)]
        self.initialized = False
    
    @property
    def grid_width(self):
        return self.cell_pixel_size * self.n_cols
    
    @property
    def grid_height(self):
        return self.cell_pixel_size * self.n_rows
    
    # @property
    # def mines_remaining(self):
    #     flagged_cells = sum(a_cell.is_flagged for cells_row in self.cells for a_cell in cells_row)
    #     return self.n_mines - flagged_cells

    @property
    def n_flagged(self):
        flagged_cells = sum(a_cell.is_flagged for cells_row in self.cells for a_cell in cells_row)
        return flagged_cells


    def in_bounds(self, row: int, col: int) -> bool:
        return 0 <= row < self.n_rows and 0 <= col < self.n_cols

    def initialize_grid(self, first_click_row: int, first_click_col: int):
        self.setup_mines(first_click_row, first_click_col)
        self.setup_adjacent_mines()
        self.initialized = True

    def setup_mines(self, exclude_row: int, exclude_col: int):
        mines_placed = 0
        while mines_placed < self.n_mines:
            row = random.randint(0, self.n_rows - 1)
            col = random.randint(0, self.n_cols - 1)
            if not (row == exclude_row and col == exclude_col) and not self.cells[row][col].is_mine:
                self.cells[row][col].put_mine()
                mines_placed += 1

    def setup_adjacent_mines(self):
        for row in range(self.n_rows):
            for col in range(self.n_cols):
                if not self.cells[row][col].is_mine:
                    adjacent_mines = 0
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            r, c = row + dr, col + dc
                            if 0 <= r < self.n_rows and 0 <= c < self.n_cols and self.cells[r][c].is_mine:
                                adjacent_mines += 1
                    self.cells[row][col].set_adjacent_mines(adjacent_mines)


    def open_cell(self, row: int, col: int) -> Tuple[bool, List[Cell]]:
        cell = self.cells[row][col]
        cell.open()
        opened_cells = [cell]
        mine_hit = False

        if cell.is_mine:
            mine_hit = True
            return mine_hit, opened_cells

        queue = deque([cell])
        
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

        while queue:
            current_cell = queue.popleft()
            cur_row, cur_col = current_cell._row, current_cell._col

            if current_cell.adjacent_mines != 0:
                continue

            for dr, dc in directions:
                r, c = cur_row + dr, cur_col + dc
                if self.in_bounds(r, c):
                    this_cell = self.cells[r][c]
                    if not this_cell.is_open and not this_cell.is_mine:
                        this_cell.open()
                        opened_cells.append(this_cell)
                        if this_cell.adjacent_mines == 0 and this_cell not in queue:
                            queue.append(this_cell)

        return mine_hit, opened_cells

    def flag_cell(self, row: int, col: int) -> Cell:
        cell = self.cells[row][col]
        if cell.is_open:
            raise UnavailableCellError('Cell already opened')
        if self.n_flagged >= self.n_mines and not cell.is_flagged:
            # Raise error if setting more mines than allowed. No error when toggling flagged cells.
            raise TooManyFlagsError('Too many flags')
        cell.toggle_flag()
        return cell

    def check_game_status(self) -> str:

        any_mine_cell_opened = any(
            cell.is_open for row in self.cells for cell in row if cell.is_mine
        )
        if any_mine_cell_opened:
            return "lost"

        all_non_mine_cells_opened = all(
            cell.is_open for row in self.cells for cell in row if not cell.is_mine
        )
        all_mine_cells_flagged = all(
            cell.is_flagged for row in self.cells for cell in row if cell.is_mine
        )

        if all_non_mine_cells_opened and all_mine_cells_flagged:
            return "won"

        return "ongoing"
    
    def print_opened_cells(self):
        grid_representation = ""
        for row in range(self.n_rows):
            for col in range(self.n_cols):
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
            for row in range(self.n_rows):
                row_representation = []
                for col in range(self.n_cols):
                    if self.cells[row][col].is_mine:
                        row_representation.append('M')
                    else:
                        row_representation.append(str(self.cells[row][col].adjacent_mines))
                grid_representation.append(''.join(row_representation))
            return '\n'.join(grid_representation)
