from logic_utils import check_guess, get_range_for_difficulty, parse_guess, update_score


def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    outcome, _ = check_guess(50, 50)
    assert outcome == "Win"


def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    outcome, _ = check_guess(60, 50)
    assert outcome == "Too High"


def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    outcome, _ = check_guess(40, 50)
    assert outcome == "Too Low"


# Regression tests for the swapped high/low hint bug: a guess that was too
# high used to say "Go HIGHER!" and a guess that was too low said "Go LOWER!".

def test_too_high_hint_says_go_lower():
    _, message = check_guess(60, 50)
    assert "LOWER" in message
    assert "HIGHER" not in message


def test_too_low_hint_says_go_higher():
    _, message = check_guess(40, 50)
    assert "HIGHER" in message
    assert "LOWER" not in message


def test_hint_boundaries():
    # Off-by-one guesses on either side of the secret
    assert check_guess(51, 50) == ("Too High", "📉 Go LOWER!")
    assert check_guess(49, 50) == ("Too Low", "📈 Go HIGHER!")


def test_win_message_has_no_direction():
    _, message = check_guess(50, 50)
    assert "HIGHER" not in message
    assert "LOWER" not in message


# Scoring: wrong guesses cost 5 points either way, and the score never goes negative.

def test_too_high_always_costs_points():
    # Used to add 5 points on even attempts
    assert update_score(50, "Too High", 1) == 45
    assert update_score(50, "Too High", 2) == 45


def test_too_low_costs_points():
    assert update_score(50, "Too Low", 1) == 45
    assert update_score(50, "Too Low", 2) == 45


def test_score_never_negative():
    assert update_score(0, "Too High", 1) == 0
    assert update_score(3, "Too Low", 2) == 0


def test_first_try_win_scores_100():
    assert update_score(0, "Win", 1) == 100


def test_win_points_shrink_per_attempt():
    assert update_score(0, "Win", 2) == 90
    assert update_score(0, "Win", 5) == 60


def test_win_points_have_minimum_of_10():
    assert update_score(0, "Win", 20) == 10


def test_score_capped_at_100():
    assert update_score(95, "Win", 1) == 100


# parse_guess range validation: out-of-range guesses are rejected.

def test_parse_guess_in_range():
    assert parse_guess("50", 1, 100) == (True, 50, None)


def test_parse_guess_boundaries_allowed():
    assert parse_guess("1", 1, 100)[0] is True
    assert parse_guess("100", 1, 100)[0] is True


def test_parse_guess_too_high_rejected():
    ok, value, err = parse_guess("101", 1, 100)
    assert not ok and value is None and "between 1 and 100" in err


def test_parse_guess_too_low_rejected():
    ok, _, err = parse_guess("0", 1, 100)
    assert not ok and "between 1 and 100" in err


def test_parse_guess_no_range_still_works():
    assert parse_guess("500") == (True, 500, None)


def test_difficulty_ranges_grow_with_difficulty():
    assert get_range_for_difficulty("Easy") == (1, 20)
    assert get_range_for_difficulty("Normal") == (1, 50)
    assert get_range_for_difficulty("Hard") == (1, 100)
