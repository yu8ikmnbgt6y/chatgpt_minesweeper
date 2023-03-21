class Cell:
    def __init__(self, row: int, col: int, cell_size: int):
        self._row = row
        self._col = col
        self._cell_size = cell_size
        self._x1 = col * cell_size
        self._y1 = row * cell_size
        self._x2 = self._x1 + cell_size
        self._y2 = self._y1 + cell_size

        self._is_mine = False
        self._is_open = False
        self._is_flagged = False
        self._adjacent_mines = 0
    
    @property
    def center_x(self):
        return (self.x1 + self.x2) / 2
    
    @property
    def center_y(self):
        return (self.y1 + self.y2) / 2

    @property
    def x1(self):
        return self._x1

    @property
    def x2(self):
        return self._x2

    @property
    def y1(self):
        return self._y1

    @property
    def y2(self):
        return self._y2

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
    def is_flagged(self):
        return self._is_flagged

    @property
    def is_mine(self):
        return self._is_mine

    def put_mine(self):
        self._is_mine = True
