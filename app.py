import random
import streamlit as st

from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)


ATTEMPT_LIMITS = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}


def reset_game():
    low, high = get_range_for_difficulty(st.session_state.difficulty)
    st.session_state.secret = random.randint(low, high)
    st.session_state.attempts = 0
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state.status = "playing"
    st.session_state.guess_input = ""
    st.session_state.feedback = None
    st.session_state.input_error = None


def submit_guess():
    if st.session_state.status != "playing":
        return

    difficulty = st.session_state.difficulty
    low, high = get_range_for_difficulty(difficulty)
    attempt_limit = ATTEMPT_LIMITS[difficulty]

    if st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"
        return

    ok, guess, error = parse_guess(
        st.session_state.guess_input, low, high
    )

    st.session_state.input_error = error
    st.session_state.feedback = None

    if not ok:
        return

    st.session_state.attempts += 1
    st.session_state.history.append(guess)

    outcome, message = check_guess(guess, st.session_state.secret)
    st.session_state.feedback = message
    st.session_state.score = update_score(
        st.session_state.score,
        outcome,
        st.session_state.attempts,
    )

    if outcome == "Win":
        st.session_state.status = "won"
    elif st.session_state.attempts >= attempt_limit:
        st.session_state.status = "lost"


st.set_page_config(page_title="Number Guesser", page_icon="🎮")
st.title("🎮 Game Glitch Investigator")

if "difficulty" not in st.session_state:
    st.session_state.difficulty = "Normal"

st.sidebar.header("Settings")
st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    key="difficulty",
    on_change=reset_game,
)

if "secret" not in st.session_state:
    reset_game()

difficulty = st.session_state.difficulty
low, high = get_range_for_difficulty(difficulty)
attempt_limit = ATTEMPT_LIMITS[difficulty]
finished = st.session_state.status != "playing"

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

st.subheader("Make a guess")
st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

st.text_input(
    "Enter your guess:",
    key="guess_input",
    disabled=finished,
)

col1, col2, col3 = st.columns(3)

with col1:
    st.button(
        "Submit Guess 🚀",
        on_click=submit_guess,
        disabled=finished,
    )

with col2:
    st.button("New Game 🔁", on_click=reset_game)

with col3:
    show_hint = st.checkbox("Show hint", value=True)

if st.session_state.input_error:
    st.error(st.session_state.input_error)

if st.session_state.status == "won":
    st.success(
        f"You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}. "
        "Start a new game to play again."
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}. "
        "Start a new game to try again."
    )
elif show_hint and st.session_state.feedback:
    st.warning(st.session_state.feedback)

st.write("Score:", st.session_state.score)
st.write("Guess history:", st.session_state.history)

st.divider()
st.caption("Choose a difficulty, enter a whole number, and follow the hints.")
