#FIX: Refactored logic into logic_utils.py using agent mode
def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    # FIX: Normal and Hard ranges were out of order (Normal was 1-100, Hard was 1-50).
    # Ranges now grow with difficulty: Easy 1-20, Normal 1-50, Hard 1-100.
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 50
    if difficulty == "Hard":
        return 1, 100
    return 1, 50


def parse_guess(raw: str, low: int = None, high: int = None):
    """
    Parse user input into an int guess.

    If low and high are given, the guess must be within [low, high] (inclusive).

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    # FIX: guesses outside the difficulty range used to be accepted and wasted an attempt.
    if low is not None and high is not None and not (low <= value <= high):
        return False, None, f"Guess must be between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    outcome examples: "Win", "Too High", "Too Low"
    """
    if guess == secret:
        return "Win", "🎉 Correct!"

    # FIX: hint messages were swapped (Too High said "Go HIGHER!" and Too Low said "Go LOWER!").
    # Also removed the TypeError string-comparison fallback, which was dead code.
    if guess > secret:
        return "Too High", "📉 Go LOWER!"
    return "Too Low", "📈 Go HIGHER!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Update score based on outcome and attempt number."""
    if outcome == "Win":
        # FIX: win formula was off by one (a first-try win scored 80). A first-try win now
        # scores 100, and the total score is capped at 100.
        points = 100 - 10 * (attempt_number - 1)
        if points < 10:
            points = 10
        return min(100, current_score + points)

    # FIX: Too High used to add 5 points on even attempts, and the score could go negative.
    # Both wrong-guess outcomes now cost 5 points, floored at 0.
    if outcome in ("Too High", "Too Low"):
        return max(0, current_score - 5)

    return current_score
