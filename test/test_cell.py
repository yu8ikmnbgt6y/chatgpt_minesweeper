import pytest
from cell import Cell

@pytest.fixture
def cell():
    return Cell()

def test_initial_state(cell):
    assert cell.is_open == False
    assert cell.flagged == False
    assert cell.is_mine == False
    assert cell.adjacent_mines == 0

def test_open_cell(cell):
    cell.open()
    assert cell.is_open == True

@pytest.mark.parametrize("initial_flagged_state, expected_flagged_state", [(False, True), (True, False)])
def test_toggle_flag(cell, initial_flagged_state, expected_flagged_state):
    cell._is_flagged = initial_flagged_state
    cell.toggle_flag()
    assert cell.flagged == expected_flagged_state

@pytest.mark.parametrize("adjacent_mines_value", [0, 1, 2, 3, 4, 5, 6, 7, 8])
def test_set_adjacent_mines(cell, adjacent_mines_value):
    cell.set_adjacent_mines(adjacent_mines_value)
    assert cell.adjacent_mines == adjacent_mines_value

def test_put_mine(cell):
    cell.put_mine()
    assert cell.is_mine == True
