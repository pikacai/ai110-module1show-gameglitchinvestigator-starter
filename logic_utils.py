import random


def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    ranges = {
        "Easy": (1, 20),
        "Normal": (1, 100),
        "Hard": (1, 50),
    }
    return ranges.get(difficulty, (1, 100))


def parse_guess(raw: str):
    """
    Parse user input into an int guess.

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except (ValueError, TypeError):
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    outcome is one of: "Win", "Too High", "Too Low"
    """
    # FIX: AI spotted that the original code cast the secret to a string on
    # even attempts, making this a lexicographic compare. We refactored it
    # into this pure numeric helper (agent mode) so it could be unit-tested.
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    - A win awards more points the fewer attempts it took (100 for a
      first-guess win, then -10 per extra attempt, floored at 10).
    - Any wrong guess costs a flat 5 points, regardless of whether it
      was too high or too low, and the score never drops below 0.
    """
    # FIX: paired with the AI to make scoring symmetric. It suggested the
    # edge cases (first-guess win = full 100, score floored at 0, both wrong
    # outcomes cost the same) that the broken version got wrong; I encoded
    # them here and locked them in with tests.
    if outcome == "Win":
        points = 100 - 10 * (attempt_number - 1)
        return current_score + max(points, 10)

    if outcome in ("Too High", "Too Low"):
        return max(current_score - 5, 0)

    return current_score


def guess_input_key(difficulty: str, input_round: int):
    """
    Build the session-state key for the guess text input.

    The key embeds ``input_round`` (bumped on every "New Game") so that a
    new game produces a *different* key. Streamlit then treats it as a
    brand-new widget and renders it empty, instead of keeping the previous
    game's number in the box.
    """
    # FIX: AI proposed this round-counter key (agent mode) after I rejected
    # its first idea of clearing the key inside the New Game block — that
    # raises Streamlit's "cannot modify a widget after instantiation" error.
    return f"guess_input_{difficulty}_{input_round}"


def new_game_state(low: int, high: int):
    """
    Build a fresh game state for a brand-new game.

    Returns a dict with every per-game field reset, so that starting a
    new game fully clears any previous "won"/"lost" status, score, and
    history (not just the secret and attempt counter).
    """
    # FIX: AI traced the sticky "Game over" banner to a partial reset and
    # had us centralize the full per-game reset here (agent mode).
    return {
        "attempts": 0,
        "secret": random.randint(low, high),
        "status": "playing",
        "score": 0,
        "history": [],
        "last_outcome": None,
        "last_message": None,
    }
