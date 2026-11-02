"""
backend/app/utils/fsrs.py
Free Spaced Repetition Scheduler (FSRS-5) implementation.
Clean, deterministic, open-source, mathematically aligned with open-spaced-repetition/fsrs4anki.
Version: 5.0.0
"""

import math
import time
from typing import Dict, Any, Tuple

FSRS_VERSION = "5.0.0"

# Standard FSRS-5 default weights
# Reference: https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm
DEFAULT_W = (
    0.40255, 1.18385, 3.173, 15.69105,
    7.1949, 0.5345, 1.4604, 0.0046, 1.54575, 0.1192, 1.01925,
    1.9395, 0.11, 0.29605, 2.2698, 0.2315, 2.9898, 0.51655, 0.6621
)

FACTOR = 19.0 / 81.0
DECAY = -0.5

# Ratings
RATING_AGAIN = 1  # 不会
RATING_HARD = 2   # 模糊
RATING_GOOD = 3   # 会了 (经测验通过)
RATING_EASY = 4   # 内部备用 (不对普通用户暴露)

# States
STATE_NEW = "new"
STATE_LEARNING = "learning"
STATE_REVIEW = "review"
STATE_RELEARNING = "relearning"

def init_card(word: str) -> Dict[str, Any]:
    """Creates a fresh unlearned FSRS card."""
    return {
        "word": word,
        "state": STATE_NEW,
        "stability": 0.0,
        "difficulty": 0.0,
        "reps": 0,
        "lapses": 0,
        "last_review": None,
        "due": 0.0,
        "rating": None,
        "retrievability": 1.0,
    }

def retrievability(stability: float, elapsed_days: float) -> float:
    """Computes retention probability R(t, S)."""
    if stability <= 0.0:
        return 0.0
    return math.pow(1.0 + FACTOR * (elapsed_days / stability), DECAY)

def next_interval(stability: float, request_retention: float = 0.90) -> float:
    """Calculates next review interval in days given target retention."""
    if stability <= 0.0:
        return 1.0
    raw_interval = (stability / FACTOR) * (math.pow(request_retention, 1.0 / DECAY) - 1.0)
    return max(1.0, round(raw_interval))

def schedule_card(
    card: Dict[str, Any],
    rating: int,
    now: float = None,
    request_retention: float = 0.90,
    w: Tuple[float, ...] = DEFAULT_W
) -> Dict[str, Any]:
    """
    Schedules card according to FSRS-5 rules.
    rating: 1 (Again), 2 (Hard), 3 (Good)
    """
    if now is None:
        now = time.time()

    state = card.get("state", STATE_NEW)
    stability = float(card.get("stability", 0.0) or 0.0)
    difficulty = float(card.get("difficulty", 0.0) or 0.0)
    reps = int(card.get("reps", 0) or 0)
    lapses = int(card.get("lapses", 0) or 0)
    last_review = card.get("last_review")

    elapsed_days = 0.0
    if last_review is not None and last_review > 0:
        elapsed_days = max(0.0, (now - last_review) / 86400.0)

    # 1. First review (Initial state: new or reps == 0)
    if state == STATE_NEW or reps == 0:
        # Initial stability: S0(G) = w[G-1]
        new_stability = w[rating - 1]
        # Initial difficulty: D0(G) = w[4] - exp(w[5]*(G-1)) + 1
        new_difficulty = max(1.0, min(10.0, w[4] - math.exp(w[5] * (rating - 1)) + 1.0))
        
        if rating == RATING_AGAIN:
            new_state = STATE_LEARNING
            interval_sec = 600.0  # 10 minutes
        elif rating == RATING_HARD:
            new_state = STATE_LEARNING
            interval_sec = 86400.0 * 1.0 # 1 day
        else: # Good
            new_state = STATE_REVIEW
            interval_days = next_interval(new_stability, request_retention)
            interval_sec = 86400.0 * interval_days

        new_reps = 1
        new_lapses = 1 if rating == RATING_AGAIN else 0
        new_due = now + interval_sec

        return {
            "word": card["word"],
            "state": new_state,
            "stability": round(new_stability, 4),
            "difficulty": round(new_difficulty, 4),
            "reps": new_reps,
            "lapses": new_lapses,
            "last_review": now,
            "due": new_due,
            "rating": rating,
            "retrievability": 1.0,
            "interval_days": round(interval_sec / 86400.0, 2)
        }

    # 2. Subsequent review
    r_current = retrievability(stability, elapsed_days)

    # Next difficulty
    delta_d = -w[6] * (rating - 3)
    d_prime = w[7] * (w[4] - math.exp(w[5] * (3 - 1)) + 1.0) + (1.0 - w[7]) * (difficulty + delta_d)
    new_difficulty = max(1.0, min(10.0, d_prime))

    # Next stability
    if rating == RATING_AGAIN:
        # Review failure
        s_forget = w[11] * math.pow(new_difficulty, -w[12]) * (math.pow(stability + 1.0, w[13]) - 1.0) * math.exp(w[14] * (1.0 - r_current))
        new_stability = max(0.1, min(stability, s_forget))
        new_state = STATE_RELEARNING
        new_lapses = lapses + 1
        interval_sec = 600.0  # 10 minutes relearning
    else:
        # Review success (Hard or Good)
        hard_penalty = w[15] if rating == RATING_HARD else 1.0
        easy_bonus = 1.0
        s_recall = stability * (1.0 + math.exp(w[8]) * (11.0 - new_difficulty) * math.pow(stability, -w[9]) * (math.exp(w[10] * (1.0 - r_current)) - 1.0) * hard_penalty * easy_bonus)
        new_stability = max(0.1, s_recall)
        new_state = STATE_REVIEW
        new_lapses = lapses
        interval_days = next_interval(new_stability, request_retention)
        if rating == RATING_HARD:
            interval_days = max(1.0, interval_days * 0.7)
        interval_sec = 86400.0 * interval_days

    new_reps = reps + 1
    new_due = now + interval_sec

    return {
        "word": card["word"],
        "state": new_state,
        "stability": round(new_stability, 4),
        "difficulty": round(new_difficulty, 4),
        "reps": new_reps,
        "lapses": new_lapses,
        "last_review": now,
        "due": new_due,
        "rating": rating,
        "retrievability": round(r_current, 4),
        "interval_days": round(interval_sec / 86400.0, 2)
    }
