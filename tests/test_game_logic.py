from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    parse_guess,
    update_score,
)


def test_winning_guess():
    assert check_guess(50, 50) == ("Win", "Correct!")


def test_guess_too_high():
    assert check_guess(60, 50) == ("Too High", "Too high. Go LOWER!")


def test_guess_too_low():
    assert check_guess(40, 50) == ("Too Low", "Too low. Go HIGHER!")


def test_numeric_comparison():
    assert check_guess(9, 50)[0] == "Too Low"


def test_difficulty_ranges():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)


def test_invalid_guesses():
    for raw in ("", "   ", "abc", "7.9", "0", "51"):
        assert parse_guess(raw, 1, 50)[0] is False


def test_valid_range_boundaries():
    assert parse_guess("1", 1, 50) == (True, 1, None)
    assert parse_guess("50", 1, 50) == (True, 50, None)


def test_incorrect_guesses_always_lose_five_points():
    for attempt in (1, 2):
        for outcome in ("Too High", "Too Low"):
            assert update_score(20, outcome, attempt) == 15


def test_win_bonus():
    assert update_score(0, "Win", 1) == 100
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 20) == 10
