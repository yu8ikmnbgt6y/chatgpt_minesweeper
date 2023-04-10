import pytest

from scoreboard import (DEFAULT_SAVE_FILE, DIFFICULTIES, MAX_HIGH_SCORE_ROW,
                        HighScore, ScoreBoard)


@pytest.fixture
def tmp_save_data_file(tmp_path):
    return tmp_path / DEFAULT_SAVE_FILE

@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_get_statistics(tmp_save_data_file, difficulty):
    score_board = ScoreBoard(save_data_file=str(tmp_save_data_file))
    stats = score_board.get_statistics(difficulty)
    assert "game_played" in stats
    assert "game_won" in stats

@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_update_statistics(tmp_save_data_file, difficulty):
    score_board = ScoreBoard(save_data_file=str(tmp_save_data_file))
    score_board.update_statistics(difficulty, won=True)
    stats = score_board.get_statistics(difficulty)
    assert stats["game_played"] == 1
    assert stats["game_won"] == 1

@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_get_high_scores(tmp_save_data_file, difficulty):
    score_board = ScoreBoard(save_data_file=str(tmp_save_data_file))
    high_scores = score_board.get_high_scores(difficulty)
    assert isinstance(high_scores, list)

@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_update_high_scores(tmp_save_data_file, difficulty):
    score_board = ScoreBoard(save_data_file=str(tmp_save_data_file))
    time = 42
    score_board.update_high_scores(difficulty, time)
    high_scores = score_board.get_high_scores(difficulty)
    assert len(high_scores) == 1
    assert high_scores[0].clear_time == time

@pytest.mark.parametrize("difficulty", DIFFICULTIES)
def test_max_high_scores(tmp_save_data_file, difficulty):
    score_board = ScoreBoard(save_data_file=str(tmp_save_data_file))
    for _ in range(MAX_HIGH_SCORE_ROW * 2):
        score_board.update_high_scores(difficulty, 42)
    high_scores = score_board.get_high_scores(difficulty)
    assert len(high_scores) == MAX_HIGH_SCORE_ROW
