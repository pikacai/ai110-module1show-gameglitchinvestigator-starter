# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

- What did the game look like the first time you ran it?
- List at least two concrete bugs you noticed at the start  
  (for example: "the hints were backwards").

The game ran and looked finished, but the feedback couldn't be trusted. The clearest bug was the hint direction: guessing 26 against a smaller secret reported "Too low," because on even-numbered attempts the secret was converted to a string and the comparison silently became lexicographic (`"26" < "5"`) instead of numeric. On top of that the hint *text* was reversed — a "Too High" outcome told the player to "Go HIGHER!" Two more bugs showed up with play: clicking **New Game** left the "Game over" banner because only `secret`/`attempts` were reset (not `status`/`score`/`history`), and the **Show hint** checkbox did nothing because the hint was only rendered inside the `if submit:` block. I also found a scoring glitch where the score went negative and a too-high guess on an even attempt actually *added* points.

**Bug Reproduction Log**

Document at least 3 bugs you found. Add rows as needed.

| Input | Expected Behavior | Actual Behavior | Console Output / Error |
|-------|-------------------|-----------------|------------------------|
| guess of 26 | "Too high" hint | "Too low" hint | None |
| after click on "New Game" | No error message | "Game over. Start a new game to try again" error message still there | None |
| After click "New Game" | empty in input box | last enter numbers in input box | None |
| two wrong guesses (e.g. 6 then 9) | small/zero score | Score: -10 (negative; too-high on even attempts even *adds* points) | None |


---

## 2. How did you use AI as a teammate?

- Which AI tools did you use on this project (for example: ChatGPT, Gemini, Copilot)?
- Give one example of an AI suggestion that was correct (including what the AI suggested and how you verified the result).
- Give one example of an AI suggestion that was incorrect or misleading (including what the AI suggested and how you verified the result).

I used Claude Code as an in-editor agent that could read the files, edit them, run pytest, and launch the app. A correct suggestion: it traced the "Too low for 26" bug to the `str(secret)` conversion forcing string comparison, and I verified it with a quick script (`check_guess(26, 5)` → "Too High" → "Go LOWER") and by playing the live app. A misleading moment: after the first round of fixes the app *still* showed the old wrong hint — the AI initially assumed the code was wrong again, but the real cause was a stale Streamlit process serving cached code; killing all `streamlit run` processes and restarting fixed it. That taught me to confirm *which* process and code version I'm actually looking at before assuming the logic is broken.

---

## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?
- Describe at least one test you ran (manual or using pytest)  
  and what it showed you about your code.
- Did AI help you design or understand any tests? How?

I treated a bug as fixed only when both a pytest case and a manual run in the live app agreed. The logic was refactored out of `app.py` into `logic_utils.py` so it could be tested directly. One concrete test, `test_wrong_guesses_penalize_equally`, asserts that `update_score(50, "Too High", 2)` and `update_score(50, "Too Low", 2)` both return 45 — this caught and now guards against the asymmetric scoring glitch. AI helped design the tests by suggesting edge cases I hadn't considered, like "score never goes negative" and "a first-guess win awards the full 100," which exposed an off-by-one in the win formula. The final suite has 11 passing tests covering comparison, new-game reset, hint persistence, and scoring.

---

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Streamlit re-runs the whole script top to bottom every time you interact with any widget, so the script is more like a "redraw" than a long-running program. Anything you want to survive between reruns has to live in `st.session_state`; plain local variables are recreated each time. The **Show hint** bug was a perfect example — the hint only appeared on the exact rerun where the Submit button returned `True`, so any other interaction wiped it out. Fixing it meant *storing* the last hint in session state and rendering it from there based on the checkbox, instead of relying on the transient button click.

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.

The habit I want to keep is marking the "crime scene" with `# FIXME` comments and writing a failing test *before* fixing, then confirming both the test and the live app afterward. Next time I'd restart the dev server (or check the running process) earlier, since I wasted time thinking a fix hadn't worked when I was really looking at a stale instance. Overall this project made me treat AI-generated code as a confident first draft that needs verification: it looked production-ready and ran without errors, yet had four real bugs that only surfaced through testing and actually playing the game.
