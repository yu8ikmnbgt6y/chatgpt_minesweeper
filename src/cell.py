class Cell:
    def __init__(self, is_mine: bool):
        self.is_mine = is_mine
        self.is_open = False
        self.is_flagged = False
        self.adjacent_mines = 0

    def open(self):
        self.is_open = True

    def toggle_flag(self):
        self.is_flagged = not self.is_flagged

    def set_adjacent_mines(self, adjacent_mines: int):
        self.adjacent_mines = adjacent_mines

    def get_adjacent_mines(self) -> int:
        return self.adjacent_mines

    def is_opened(self) -> bool:
        return self.is_open

    def is_flagged(self) -> bool:
        return self.is_flagged

    def contains_mine(self) -> bool:
        return self.is_mine
