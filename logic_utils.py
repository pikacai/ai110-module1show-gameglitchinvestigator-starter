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
    return f"guess_input_{difficulty}_{input_round}"


def new_game_state(low: int, high: int):
    """
    Build a fresh game state for a brand-new game.

    Returns a dict with every per-game field reset, so that starting a
    new game fully clears any previous "won"/"lost" status, score, and
    history (not just the secret and attempt counter).
    """
    return {
        "attempts": 0,
        "secret": random.randint(low, high),
        "status": "playing",
        "score": 0,
        "history": [],
        "last_outcome": None,
        "last_message": None,
    }
