# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I used Claude Code (in the VS Code extension) and asked it to explain and then fix the bugs in the guessing game, add tests, and run the app to confirm the fixes worked.

**What did the agent do?**

- Diagnosed the reversed-hint bug, tracing it to the `str(secret)` conversion that forced lexicographic comparison, and marked the spots with `# FIXME` comments.
- Refactored the game logic out of `app.py` into `logic_utils.py` (`check_guess`, `parse_guess`, `get_range_for_difficulty`, `update_score`, and a new `new_game_state`) and wired `app.py` to import them.
- Fixed four bugs: reversed hint direction, New Game not resetting `status`/`score`/`history`, the Show-hint checkbox doing nothing (now persisted in session state), and the asymmetric/negative scoring.
- Added pytest cases (suite grew from 3 to 11), ran `pytest` (11 passed), and launched `streamlit run app.py` headless to confirm it served HTTP 200.

**What did you have to verify or fix manually?**

I played the live app to confirm hints, New Game, and the Show-hint toggle behaved correctly, and I checked the secret in the Developer Debug Info to validate the hint direction. The agent also briefly mis-diagnosed a "still wrong" report as a logic bug when it was actually a **stale Streamlit process** serving old cached code — I confirmed the fix only after it killed the old process and restarted clean.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| New Game must clear "lost" status | "add a pytest case targeting the bug you just fixed" | `test_new_game_resets_status_to_playing` → `new_game_state(...)["status"] == "playing"` | Yes | Directly guards the bug where the "Game over" banner persisted after restart. |
| Wrong guesses must penalize equally | "add a test that too-high and too-low penalize equally" | `test_wrong_guesses_penalize_equally` → both return 45 from 50 | Yes | Catches the glitch where too-high on even attempts added points. |
| Score must never go negative | "test the score never goes negative" | `test_score_never_goes_negative` → wrong guess at 0 stays 0 | Yes | The old code let the score sink to -10; now floored at 0. |
| First-guess win awards full points | (AI-suggested edge case) | `test_first_guess_win_awards_full_points` → 100 on attempt 1 | Yes | Exposed an off-by-one (`attempt_number + 1`) that awarded 80 instead of 100. |

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
```

**Linting output before:**

```
<!-- Paste relevant linter warnings/errors -->
```

**Changes applied:**

<!-- Describe what you changed based on the AI's suggestions -->

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
