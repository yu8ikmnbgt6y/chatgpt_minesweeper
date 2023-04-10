import pytest

from cell import Cell


@pytest.fixture
def cell():
    return Cell(1, 1, 10)

def test_cell_initial_state(cell):
    assert cell.x1 == 10
    assert cell.y1 == 10
    assert cell.x2 == 20
    assert cell.y2 == 20
    assert cell.center_x == 15
    assert cell.center_y == 15
    assert not cell.is_open
    assert not cell.is_flagged
    assert not cell.is_mine
    assert cell.adjacent_mines == 0

def test_cell_open(cell):
    cell.open()
    assert cell.is_open

def test_cell_set_adjacent_mines(cell):
    cell.set_adjacent_mines(3)
    assert cell.adjacent_mines == 3

def test_cell_toggle_flag(cell):
    cell.toggle_flag()
    assert cell.is_flagged
    cell.toggle_flag()
    assert not cell.is_flagged

def test_cell_put_mine(cell):
    cell.put_mine()
    assert cell.is_mine

def test_cell_str_representation(cell):
    assert str(cell) == "(1,1)"