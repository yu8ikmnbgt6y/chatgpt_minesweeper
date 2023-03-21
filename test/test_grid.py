import pytest
from minesweeper_grid import MinesweeperGrid


@pytest.fixture
def empty_grid():
    return MinesweeperGrid(4, 4, 0)


@pytest.fixture
def grid_with_mines():
    grid = MinesweeperGrid(4, 4, 4)
    grid.initialize_grid(0, 0)
    return grid


@pytest.mark.parametrize("row, col, expected", [
    (0, 0, True),
    (3, 3, True),
    (-1, 0, False),
    (4, 4, False),
    (0, 4, False),
])
def test_in_bounds(empty_grid, row, col, expected):
    assert empty_grid.in_bounds(row, col) == expected


def test_initialize_grid(empty_grid):
    empty_grid.initialize_grid(0, 0)
    assert sum([cell.is_mine for row in empty_grid.cells for cell in row]) == 0


def test_open_cell_no_mines(empty_grid):
    is_mine, opened_cells = empty_grid.open_cell(1, 1)
    assert not is_mine
    assert len(opened_cells) == empty_grid.rows * empty_grid.cols
    for row in range(empty_grid.rows):
        for col in range(empty_grid.cols):
            assert (row, col) in opened_cells


def test_open_cell_mines(grid_with_mines):
    is_mine, opened_cells = grid_with_mines.open_cell(0, 0)
    assert not is_mine

    grid_with_mines.cells[1][1].put_mine()
    is_mine, opened_cells = grid_with_mines.open_cell(1, 1)
    assert is_mine


def test_flag_cell(empty_grid):
    assert not empty_grid.cells[0][0].flagged
    empty_grid.flag_cell(0, 0)
    assert empty_grid.cells[0][0].flagged
    empty_grid.flag_cell(0, 0)
    assert not empty_grid.cells[0][0].flagged


def test_check_game_status_won(empty_grid):
    # Test empty grid (game won)
    for row in range(empty_grid.rows):
        for col in range(empty_grid.cols):
            empty_grid.cells[row][col].open()
    assert empty_grid.check_game_status() == "won"


def test_check_game_status_ongoing(grid_with_mines):
    # Test initialized grid with mines (game ongoing)
    assert grid_with_mines.check_game_status() == "ongoing"


def test_check_game_status_lost(grid_with_mines):
    # Test mine grid (game lost)
    mine_row, mine_col = 0, 0
    grid_with_mines.cells[mine_row][mine_col].put_mine()
    grid_with_mines.open_cell(mine_row, mine_col)
    assert grid_with_mines.check_game_status() == "lost"
