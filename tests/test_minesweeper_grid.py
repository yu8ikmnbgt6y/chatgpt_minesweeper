import pytest

from minesweeper_grid import (MinesweeperGrid, TooManyFlagsError,
                              UnavailableCellError)


@pytest.fixture
def minesweeper_grid():
    return MinesweeperGrid(9, 9, 10)

def test_minesweeper_grid_initial_state(minesweeper_grid):
    assert minesweeper_grid.grid_width == 180
    assert minesweeper_grid.grid_height == 180
    assert minesweeper_grid.n_flagged == 0
    assert minesweeper_grid.progression_rate == 0

def test_minesweeper_grid_in_bounds(minesweeper_grid):
    assert minesweeper_grid.in_bounds(0, 0)
    assert not minesweeper_grid.in_bounds(-1, 0)
    assert not minesweeper_grid.in_bounds(0, -1)
    assert not minesweeper_grid.in_bounds(9, 9)

@pytest.mark.parametrize("row, col", [(4, 4), (0, 0), (8, 8)])
def test_minesweeper_grid_initialize_grid(minesweeper_grid, row, col):
    minesweeper_grid.initialize_grid(row, col)
    mine_count = sum(cell.is_mine for row_cells in minesweeper_grid.cells for cell in row_cells)
    assert mine_count == 10
    assert not minesweeper_grid.cells[row][col].is_mine

def test_minesweeper_grid_flag_cell(minesweeper_grid):
    minesweeper_grid.flag_cell(0, 0)
    assert minesweeper_grid.cells[0][0].is_flagged
    assert minesweeper_grid.n_flagged == 1

    minesweeper_grid.flag_cell(0, 0)
    assert not minesweeper_grid.cells[0][0].is_flagged
    assert minesweeper_grid.n_flagged == 0


def test_minesweeper_grid_flag_cell_errors(minesweeper_grid):
    minesweeper_grid.initialize_grid(4, 4)
    minesweeper_grid.cells[4][4].open()
    
    with pytest.raises(UnavailableCellError):
        minesweeper_grid.flag_cell(4, 4)
    
    # Flag non-mine cells up to the number of mines
    flags_remaining = minesweeper_grid.n_mines
    for i in range(minesweeper_grid.n_rows):
        for j in range(minesweeper_grid.n_cols):
            if not minesweeper_grid.cells[i][j].is_mine:
                minesweeper_grid.flag_cell(i, j)
                flags_remaining -= 1
                if flags_remaining == 0:
                    break
        if flags_remaining == 0:
            break

    # Find a cell that is not open and not flagged
    extra_row, extra_col = None, None
    for i in range(minesweeper_grid.n_rows):
        for j in range(minesweeper_grid.n_cols):
            if not minesweeper_grid.cells[i][j].is_open and not minesweeper_grid.cells[i][j].is_flagged:
                extra_row, extra_col = i, j
                break
        if extra_row is not None:
            break

    # Now, try to flag another cell and check if the TooManyFlagsError is raised
    with pytest.raises(TooManyFlagsError):
        minesweeper_grid.flag_cell(extra_row, extra_col)