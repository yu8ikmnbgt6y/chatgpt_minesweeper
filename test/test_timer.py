import pytest
from time import sleep

from timer import Timer


@pytest.fixture
def timer():
    return Timer()


def test_initial_state(timer):
    assert timer.start_time == 0.0
    assert timer.get_elapsed_time() == 0.0


def test_start_timer(timer):
    timer.start_timer()
    assert timer.start_time != 0.0


def test_get_elapsed_time(timer):
    timer.start_timer()
    sleep(1)
    elapsed_time = timer.get_elapsed_time()
    assert 0.9 <= elapsed_time <= 1.1


@pytest.mark.parametrize("sleep_duration", [0.5, 1.5, 2])
def test_get_elapsed_time_with_parametrize(timer, sleep_duration):
    timer.start_timer()
    sleep(sleep_duration)
    elapsed_time = timer.get_elapsed_time()
    assert sleep_duration - 0.1 <= elapsed_time <= sleep_duration + 0.1
