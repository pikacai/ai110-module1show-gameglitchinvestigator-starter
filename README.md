# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

**The game's purpose.** Glitchy Guesser is a Streamlit number-guessing game. The app picks a secret number within a range set by the difficulty (Easy 1–20, Normal 1–100, Hard 1–50), and the player tries to find it within a limited number of attempts. After each guess the game gives a higher/lower hint, tracks a score, and ends on a win or when attempts run out.

**Bugs found.**

1. **Reversed hints / wrong comparison.** Guessing 26 against a smaller secret reported "Too low." On even-numbered attempts the secret was cast to a string, so the comparison became lexicographic (`"26" < "5"`) instead of numeric; the hint text was also swapped ("Too High" → "Go HIGHER!").
2. **New Game didn't reset state.** Clicking **New Game** only reset the secret and attempt counter, so a finished game kept its `status`, and the "Game over" banner stuck around.
3. **Guess box didn't clear.** After **New Game**, the input box still showed the last number typed, because its widget key never changed.
4. **"Show hint" did nothing.** The hint was only rendered inside the Submit-click branch, so toggling the checkbox couldn't show or hide it.
5. **Broken scoring.** The score could go negative, and a too-high guess on an even attempt actually *added* points, while too-low always subtracted.

**Fixes applied.**

- Refactored all game logic out of `app.py` into `logic_utils.py` (`check_guess`, `parse_guess`, `get_range_for_difficulty`, `update_score`, `new_game_state`, `guess_input_key`) and added a test suite.
- `check_guess` now compares numerically and returns a clean outcome string; `app.py` maps the outcome to the correct hint text.
- `new_game_state()` resets **every** per-game field (status, score, history, last hint), and New Game bumps an `input_round` counter that changes the guess box's widget key so it renders empty.
- The last hint is stored in session state and rendered from the **Show hint** checkbox on every rerun, so it persists and toggles correctly.
- `update_score` now penalizes any wrong guess by a flat 5, never drops below 0, and awards the full 100 for a first-guess win.

## 📸 Demo Walkthrough

A sample game on **Normal** difficulty (secret = 57, visible in the Developer Debug Info panel):

1. Player enters **40** → game returns **"📈 Go HIGHER!"** (Too Low). Score: 0 → falls to 0 (floored).
2. Player enters **70** → game returns **"📉 Go LOWER!"** (Too High). Score stays floored at 0.
3. Player enters **50** → **"📈 Go HIGHER!"** (Too Low). The hint updates after each guess and stays visible as long as **Show hint** is checked.
4. Player toggles **Show hint** off and on → the latest hint hides and reappears without needing another guess.
5. Player enters **57** → **"🎉 Correct!"**, balloons appear, and the game shows the win message with the final score; the board then locks until a new game starts.
6. Player clicks **New Game 🔁** → the "Game over"/win banner clears, the guess box is empty, and score/attempts/history all reset for a fresh round.

## 🧪 Test Results

```
$ python -m pytest tests/ -v
============================= test session starts ==============================
platform darwin -- Python 3.9.6, pytest-8.4.2, pluggy-1.6.0
collected 12 items

tests/test_game_logic.py::test_winning_guess PASSED                      [  8%]
tests/test_game_logic.py::test_guess_too_high PASSED                     [ 16%]
tests/test_game_logic.py::test_guess_too_low PASSED                      [ 25%]
tests/test_game_logic.py::test_new_game_resets_status_to_playing PASSED  [ 33%]
tests/test_game_logic.py::test_new_game_clears_score_attempts_and_history PASSED [ 41%]
tests/test_game_logic.py::test_new_game_secret_respects_range PASSED     [ 50%]
tests/test_game_logic.py::test_new_game_clears_last_hint PASSED          [ 58%]
tests/test_game_logic.py::test_new_game_changes_guess_input_key_so_box_clears PASSED [ 66%]
tests/test_game_logic.py::test_wrong_guesses_penalize_equally PASSED     [ 75%]
tests/test_game_logic.py::test_score_never_goes_negative PASSED          [ 83%]
tests/test_game_logic.py::test_first_guess_win_awards_full_points PASSED [ 91%]
tests/test_game_logic.py::test_win_award_decreases_with_more_attempts_and_floors PASSED [100%]

============================== 12 passed in 0.01s ==============================
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
