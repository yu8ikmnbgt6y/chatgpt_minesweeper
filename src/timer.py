import time


class Timer:
    def __init__(self):
        self._start_time = None
        self._stop_time = None

    def start(self):
        self._start_time = time.time()
        self._stop_time = None
    
    def stop(self):
        self._stop_time = time.time()

    @property
    def running(self) -> bool:
        return self._start_time is not None and self._stop_time is None

    def get_elapsed_time(self) -> float:
        if self._start_time:
            if self._stop_time:
                return self._stop_time - self._start_time
            else:
                return time.time() - self._start_time
        else:
            return 0.0
