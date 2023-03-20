import time

class Timer:
    def __init__(self):
        self.start_time = 0.0

    def start_timer(self):
        self.start_time = time.time()

    def get_elapsed_time(self) -> float:
        if self.start_time:
            return time.time() - self.start_time
        return 0.0
