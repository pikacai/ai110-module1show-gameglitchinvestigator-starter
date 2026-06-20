import streamlit as st

from logic_utils import (
    check_guess,
    get_range_for_difficulty,
    guess_input_key,
    new_game_state,
    parse_guess,
    update_score,
)

# Hint text for each outcome. A guess that is too HIGH should tell the
# player to go LOWER, and vice versa.
HINT_MESSAGES = {
    "Win": "🎉 Correct!",
    "Too High": "📉 Go LOWER!",
    "Too Low": "📈 Go HIGHER!",
}

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("An AI-generated guessing game. Something is off.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    for key, value in new_game_state(low, high).items():
        st.session_state[key] = value

# Bumped on every "New Game" so the guess input gets a brand-new widget
# key and renders empty, instead of keeping the previous game's number.
if "input_round" not in st.session_state:
    st.session_state.input_round = 0

st.subheader("Make a guess")

st.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)
    st.write("Difficulty:", difficulty)
    st.write("History:", st.session_state.history)

raw_guess = st.text_input(
    "Enter your guess:",
    key=guess_input_key(difficulty, st.session_state.input_round),
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess 🚀")
with col2:
    new_game = st.button("New Game 🔁")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    # Reset EVERY per-game field (status/score/history too), not just the
    # secret and attempt counter — otherwise a finished game keeps its
    # "won"/"lost" status and the "Game over" banner sticks around.
    for key, value in new_game_state(low, high).items():
        st.session_state[key] = value
    # Change the input widget's key so it comes back empty on rerun.
    st.session_state.input_round += 1
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won. Start a new game to play again.")
    else:
        st.error("Game over. Start a new game to try again.")
    st.stop()

if submit:
    st.session_state.attempts += 1

    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)
        message = HINT_MESSAGES[outcome]

        # Persist the hint so it survives reruns and so toggling the
        # "Show hint" checkbox can show/hide it at any time — not just
        # on the exact rerun where Submit was clicked.
        st.session_state.last_outcome = outcome
        st.session_state.last_message = message

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(
                f"You won! The secret was {st.session_state.secret}. "
                f"Final score: {st.session_state.score}"
            )
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"
                st.error(
                    f"Out of attempts! "
                    f"The secret was {st.session_state.secret}. "
                    f"Score: {st.session_state.score}"
                )

# Show the most recent hint whenever "Show hint" is on, regardless of
# which widget triggered this rerun. This is what makes the checkbox
# actually toggle the hint on and off.
if show_hint and st.session_state.get("last_message"):
    st.warning(f"Hint: {st.session_state.last_message}")
elif not show_hint:
    st.caption("💡 Turn on \"Show hint\" to see a hint after each guess.")

st.divider()
st.caption("Built by an AI that claims this code is production-ready.")
