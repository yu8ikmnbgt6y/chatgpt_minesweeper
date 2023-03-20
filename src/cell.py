class Cell:
    def __init__(self):
        self._is_mine = False
        self._is_open = False
        self._is_flagged = False
        self._adjacent_mines = 0

    @property
    def is_open(self):
        return self._is_open

    def open(self):
        self._is_open = True

    def set_adjacent_mines(self, adjacent_mines: str):
        self._adjacent_mines = adjacent_mines

    @property
    def adjacent_mines(self):
        return self._adjacent_mines

    def toggle_flag(self):
        self._is_flagged = not self._is_flagged

    @property
    def flagged(self):
        return self._is_flagged

    @property
    def is_mine(self):
        return self._is_mine
    
    def put_mine(self):
        self._is_mine = True
