import pytest
from cell import Cell  # Assuming the Cell class is in a file called cell.py

@pytest.fixture
def cell_mine():
    return Cell(is_mine=True)

@pytest.fixture
def cell_no_mine():
    return Cell(is_mine=False)

def test_cell_initialization(cell_mine, cell_no_mine):
    assert cell_mine.is_mine
    assert not cell_mine.is_open
    assert not cell_mine.flagged
    assert cell_mine.adjacent_mines == 0

    assert not cell_no_mine.is_mine

def test_open_cell(cell_no_mine):
    cell_no_mine.open()
    assert cell_no_mine.is_open

def test_toggle_flag(cell_no_mine):
    cell_no_mine.toggle_flag()
    assert cell_no_mine.flagged
    cell_no_mine.toggle_flag()
    assert not cell_no_mine.flagged

def test_set_adjacent_mines(cell_no_mine):
    cell_no_mine.set_adjacent_mines(3)
    assert cell_no_mine.adjacent_mines == 3
