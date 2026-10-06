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

### Game purpose

A Streamlit number-guessing game. You pick a difficulty, guess the secret number within a limited
number of attempts, and get a "Go HIGHER / Go LOWER" hint after each guess. Winning sooner scores more
(up to 100), and wrong guesses cost points (the score never goes below 0).

| Difficulty | Range | Attempts |
|---|---|---|
| Easy | 1-20 | 8 |
| Normal | 1-50 | 7 |
| Hard | 1-100 | 6 |

### Bugs found

- **Swapped hints:** a too-high guess said "Go HIGHER!" and a too-low guess said "Go LOWER!".
- **Wrong hints on every second guess:** the secret was converted to a string on even attempts, so the
  comparison was made on text instead of numbers.
- **New Game didn't work after a finished game:** it never reset `status`, so the game-over check kept
  blocking guesses. It also never reset score or history, and ignored the difficulty range.
- **Score bugs:** a Too High guess *added* 5 points on even attempts, the score could go negative, and
  the win bonus was off by one (a first-try win scored 80).
- **Impossible guesses wasted attempts:** out-of-range numbers, and even non-numbers, were accepted and
  used up an attempt.
- **Wrong range text:** the prompt always said "between 1 and 100", whatever the difficulty.
- **Attempts left was off by one,** and lagged a click behind after pressing Submit.
- **Difficulty settings were out of order:** Normal had a bigger range than Hard, and Hard had the
  fewest attempts.

### Fixes applied

- Moved `get_range_for_difficulty`, `parse_guess`, `check_guess` and `update_score` into
  `logic_utils.py`; `app.py` imports them.
- Corrected the hint messages and removed the string-comparison fallback in `check_guess`.
- The secret is always passed to `check_guess` as an integer.
- New Game resets status, score and history, and picks a secret from the current difficulty's range.
- Wrong guesses cost 5 points, the score is floored at 0 and capped at 100, and a first-try win
  scores 100 (`100 - 10 * (attempt - 1)`, minimum 10 bonus).
- `parse_guess(raw, low, high)` rejects out-of-range guesses. Only valid guesses count as an attempt or
  appear in history.
- The range text uses the selected difficulty, attempts start at 0, and "Attempts left" and the debug
  panel update immediately on Submit.
- Difficulty ranges now grow with difficulty and attempt limits shrink.
- Every fix is marked with a `# FIX:` comment in the code.

## 📸 Demo Walkthrough

1. Run `python -m streamlit run app.py` and choose a difficulty in the sidebar. The sidebar and the
   prompt both show the range for that difficulty (for example 1 to 50 on Normal).
2. Type a number and press **Submit Guess**. "Attempts left" drops by one straight away.
3. Read the hint: a guess above the secret says "Go LOWER!" and a guess below it says "Go HIGHER!".
4. Try a number outside the range or text such as "abc". You get an error and no attempt is used.
5. Guess the secret to win. A first-try win scores 100, and later wins score less.
6. Press **New Game** to start again with a fresh secret, a reset score, and guesses accepted again.

**Screenshot** *(optional)*: <!-- Insert a screenshot of your fixed, winning game here -->

## 🧪 Test Results

```
$ python3 -m pytest tests -q
....................                                                     [100%]
20 passed in 0.00s
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
