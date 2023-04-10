import time

import pytest

from timer import Timer


@pytest.fixture
def timer_instance():
    return Timer()

@pytest.mark.parametrize("wait_time, tolerance", [(0.5, 0.1), (1, 0.1), (2, 0.1)])
def test_timer_running_state(timer_instance, wait_time, tolerance):
    timer_instance.start()
    assert timer_instance.running
    time.sleep(wait_time)
    elapsed_time = timer_instance.get_elapsed_time()
    assert wait_time - tolerance <= elapsed_time <= wait_time + tolerance

@pytest.mark.parametrize("wait_time, tolerance", [(0.5, 0.1), (1, 0.1), (2, 0.1)])
def test_timer_stopped_state(timer_instance, wait_time, tolerance):
    timer_instance.start()
    time.sleep(wait_time)
    timer_instance.stop()
    assert not timer_instance.running
    elapsed_time = timer_instance.get_elapsed_time()
    assert wait_time - tolerance <= elapsed_time <= wait_time + tolerance

def test_timer_initial_state(timer_instance):
    assert timer_instance.get_elapsed_time() == 0.0
    assert not timer_instance.running

def test_timer_reset(timer_instance):
    timer_instance.start()
    time.sleep(0.5)
    timer_instance.stop()
    timer_instance.start()
    assert timer_instance.running
    time.sleep(0.5)
    elapsed_time = timer_instance.get_elapsed_time()
    assert 0.4 <= elapsed_time <= 0.6
