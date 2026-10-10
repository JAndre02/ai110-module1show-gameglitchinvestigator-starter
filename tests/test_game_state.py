from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


APP = str(Path(__file__).resolve().parents[1] / "app.py")


def start_game():
    app = AppTest.from_file(APP).run()
    assert not app.exception
    app.session_state.secret = 10
    return app


def guess(app, value):
    app.text_input[0].set_value(str(value))
    app.button[0].click().run()
    assert not app.exception


def assert_reset(app):
    assert not app.exception
    assert app.session_state.history == []
    assert app.session_state.attempts == 0
    assert app.session_state.score == 0
    assert app.session_state.status == "playing"
    assert app.text_input[0].value == ""
    assert not app.button[0].disabled


def test_counter_updates_immediately_and_ignores_invalid_input():
    app = start_game()
    assert "Attempts left: 8" in app.info[0].value
    for value in ("", "abc", "101"):
        guess(app, value)
        assert app.session_state.attempts == 0
        assert app.session_state.history == []
    guess(app, 1)
    assert app.session_state.attempts == 1
    assert app.session_state.history == [1]
    assert "Attempts left: 7" in app.info[0].value


@pytest.mark.parametrize("ending", ["playing", "won", "lost"])
def test_new_game_resets_all_state_and_allows_play(ending):
    app = start_game()
    if ending == "lost":
        for _ in range(8):
            guess(app, 1)
        assert "Attempts left: 0" in app.info[0].value
        assert app.button[0].disabled
    else:
        guess(app, 10 if ending == "won" else 1)
    assert app.session_state.status == ending
    app.button[1].click().run()
    assert_reset(app)
    assert "Attempts left: 8" in app.info[0].value
    app.session_state.secret = 10
    guess(app, 1)
    assert app.session_state.history == [1]
    assert app.session_state.attempts == 1


def test_difficulty_change_resets_game():
    app = start_game()
    guess(app, 1)
    app.selectbox[0].select("Easy").run()
    assert_reset(app)
    assert 1 <= app.session_state.secret <= 20
    assert "Attempts left: 6" in app.info[0].value


def test_correct_last_guess_wins():
    app = start_game()
    for _ in range(7):
        guess(app, 1)
    guess(app, 10)
    assert app.session_state.status == "won"
    assert app.session_state.attempts == 8
    assert "Attempts left: 0" in app.info[0].value
