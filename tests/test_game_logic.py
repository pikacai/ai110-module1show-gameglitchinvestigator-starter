from logic_utils import check_guess, guess_input_key, new_game_state, update_score

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_new_game_resets_status_to_playing():
    # Bug: clicking "New Game" after a loss left status == "lost",
    # so the "Game over" banner stuck around. A new game must reset
    # status back to "playing".
    state = new_game_state(1, 100)
    assert state["status"] == "playing"

def test_new_game_clears_score_attempts_and_history():
    # A fresh game should start completely clean, not carry over the
    # previous game's score, attempt count, or guess history.
    state = new_game_state(1, 100)
    assert state["score"] == 0
    assert state["attempts"] == 0
    assert state["history"] == []

def test_new_game_secret_respects_range():
    # The new secret should fall inside the difficulty's range.
    low, high = 1, 20
    state = new_game_state(low, high)
    assert low <= state["secret"] <= high

def test_new_game_clears_last_hint():
    # A new game must clear any leftover hint so a stale hint from the
    # previous game does not show under the "Show hint" toggle.
    state = new_game_state(1, 100)
    assert state["last_outcome"] is None
    assert state["last_message"] is None

def test_new_game_changes_guess_input_key_so_box_clears():
    # Bug: after clicking "New Game" the guess box kept the last number,
    # because the text-input widget key never changed. Bumping input_round
    # must yield a DIFFERENT key, so Streamlit rebuilds the input empty.
    before = guess_input_key("Normal", 0)
    after = guess_input_key("Normal", 1)
    assert before != after

def test_wrong_guesses_penalize_equally():
    # Bug was: "Too High" on an even attempt ADDED points while "Too Low"
    # subtracted. Both wrong outcomes should cost the same flat amount.
    too_high = update_score(50, "Too High", attempt_number=2)
    too_low = update_score(50, "Too Low", attempt_number=2)
    assert too_high == too_low == 45

def test_score_never_goes_negative():
    # A wrong guess at score 0 must stay at 0, not drop to -5.
    assert update_score(0, "Too Low", attempt_number=3) == 0
    assert update_score(0, "Too High", attempt_number=4) == 0

def test_first_guess_win_awards_full_points():
    # Winning on the first attempt should award the full 100, not 80.
    assert update_score(0, "Win", attempt_number=1) == 100

def test_win_award_decreases_with_more_attempts_and_floors():
    assert update_score(0, "Win", attempt_number=2) == 90
    # Even a very late win awards at least the floor of 10.
    assert update_score(0, "Win", attempt_number=50) == 10
