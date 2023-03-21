import pytest
from scoreboard import ScoreBoard


@pytest.fixture
def empty_scoreboard():
    return ScoreBoard()


@pytest.mark.parametrize("difficulty", ["beginner", "intermediate", "advanced"])
def test_get_statistics(empty_scoreboard, difficulty):
    stats = empty_scoreboard.get_statistics(difficulty)
    assert stats == {"games_played": 0, "games_won": 0}


@pytest.mark.parametrize("difficulty", ["beginner", "intermediate", "advanced"])
def test_update_statistics(empty_scoreboard, difficulty):
    empty_scoreboard.update_statistics(difficulty, True)
    stats = empty_scoreboard.get_statistics(difficulty)
    assert stats == {"games_played": 1, "games_won": 1}


@pytest.mark.parametrize("difficulty", ["beginner", "intermediate", "advanced"])
def test_get_high_scores(empty_scoreboard, difficulty):
    high_scores = empty_scoreboard.get_high_scores(difficulty)
    assert high_scores == []


@pytest.mark.parametrize("difficulty", ["beginner", "intermediate", "advanced"])
def test_update_high_scores(empty_scoreboard, difficulty):
    empty_scoreboard.update_high_scores(difficulty, 42, "2023-01-01")
    high_scores = empty_scoreboard.get_high_scores(difficulty)
    assert high_scores == [(42, "2023-01-01")]


def test_invalid_difficulty(empty_scoreboard):
    with pytest.raises(NotImplementedError):
        empty_scoreboard.get_statistics("invalid")

    with pytest.raises(NotImplementedError):
        empty_scoreboard.update_statistics("invalid", True)

    with pytest.raises(NotImplementedError):
        empty_scoreboard.get_high_scores("invalid")

    with pytest.raises(NotImplementedError):
        empty_scoreboard.update_high_scores("invalid", 42, "2023-01-01")
