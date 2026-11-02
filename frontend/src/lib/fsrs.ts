/**
 * frontend/src/lib/fsrs.ts
 * Free Spaced Repetition Scheduler (FSRS-5) implementation in TypeScript.
 * Identical mathematical behavior with backend/app/utils/fsrs.py.
 * Version: 5.0.0
 */

export const FSRS_VERSION = "5.0.0";

export const DEFAULT_W = [
  0.40255, 1.18385, 3.173, 15.69105,
  7.1949, 0.5345, 1.4604, 0.0046, 1.54575, 0.1192, 1.01925,
  1.9395, 0.11, 0.29605, 2.2698, 0.2315, 2.9898, 0.51655, 0.6621
];

export const FACTOR = 19.0 / 81.0;
export const DECAY = -0.5;

export type CardState = "new" | "learning" | "review" | "relearning";

export interface FSRSCard {
  word: string;
  state: CardState;
  stability: number;
  difficulty: number;
  reps: number;
  lapses: number;
  last_review: number | null;
  due: number;
  rating?: number | null;
  retrievability?: number;
  interval_days?: number;
}

export const RATING_AGAIN = 1; // 不会
export const RATING_HARD = 2;  // 模糊
export const RATING_GOOD = 3;  // 会了 (测验成功)
export const RATING_EASY = 4;

export function initCard(word: string): FSRSCard {
  return {
    word,
    state: "new",
    stability: 0,
    difficulty: 0,
    reps: 0,
    lapses: 0,
    last_review: null,
    due: 0,
    rating: null,
    retrievability: 1.0,
  };
}

export function retrievability(stability: number, elapsedDays: number): number {
  if (stability <= 0) return 0;
  return Math.pow(1.0 + FACTOR * (elapsedDays / stability), DECAY);
}

export function nextInterval(stability: number, requestRetention = 0.90): number {
  if (stability <= 0) return 1;
  const raw = (stability / FACTOR) * (Math.pow(requestRetention, 1.0 / DECAY) - 1.0);
  return Math.max(1, Math.round(raw));
}

export function scheduleCard(
  card: FSRSCard,
  rating: 1 | 2 | 3,
  now = Date.now() / 1000,
  requestRetention = 0.90,
  w = DEFAULT_W
): FSRSCard {
  const state = card.state || "new";
  const stability = card.stability || 0;
  const difficulty = card.difficulty || 0;
  const reps = card.reps || 0;
  const lapses = card.lapses || 0;
  const lastReview = card.last_review;

  let elapsedDays = 0;
  if (lastReview && lastReview > 0) {
    elapsedDays = Math.max(0, (now - lastReview) / 86400.0);
  }

  // 1. Initial Review
  if (state === "new" || reps === 0) {
    const newStability = w[rating - 1];
    const newDifficulty = Math.max(1.0, Math.min(10.0, w[4] - Math.exp(w[5] * (rating - 1)) + 1.0));

    let newState: CardState;
    let intervalSec: number;

    if (rating === RATING_AGAIN) {
      newState = "learning";
      intervalSec = 600; // 10 minutes
    } else if (rating === RATING_HARD) {
      newState = "learning";
      intervalSec = 86400 * 1; // 1 day
    } else {
      newState = "review";
      const days = nextInterval(newStability, requestRetention);
      intervalSec = 86400 * days;
    }

    const newReps = 1;
    const newLapses = rating === RATING_AGAIN ? 1 : 0;
    const newDue = now + intervalSec;

    return {
      word: card.word,
      state: newState,
      stability: Number(newStability.toFixed(4)),
      difficulty: Number(newDifficulty.toFixed(4)),
      reps: newReps,
      lapses: newLapses,
      last_review: now,
      due: newDue,
      rating,
      retrievability: 1.0,
      interval_days: Number((intervalSec / 86400.0).toFixed(2))
    };
  }

  // 2. Subsequent Review
  const rCurrent = retrievability(stability, elapsedDays);

  const deltaD = -w[6] * (rating - 3);
  const dPrime = w[7] * (w[4] - Math.exp(w[5] * (3 - 1)) + 1.0) + (1.0 - w[7]) * (difficulty + deltaD);
  const newDifficulty = Math.max(1.0, Math.min(10.0, dPrime));

  let newStability: number;
  let newState: CardState;
  let newLapses = lapses;
  let intervalSec: number;

  if (rating === RATING_AGAIN) {
    const sForget = w[11] * Math.pow(newDifficulty, -w[12]) * (Math.pow(stability + 1.0, w[13]) - 1.0) * Math.exp(w[14] * (1.0 - rCurrent));
    newStability = Math.max(0.1, Math.min(stability, sForget));
    newState = "relearning";
    newLapses = lapses + 1;
    intervalSec = 600; // 10 min
  } else {
    const hardPenalty = rating === RATING_HARD ? w[15] : 1.0;
    const sRecall = stability * (1.0 + Math.exp(w[8]) * (11.0 - newDifficulty) * Math.pow(stability, -w[9]) * (Math.exp(w[10] * (1.0 - rCurrent)) - 1.0) * hardPenalty);
    newStability = Math.max(0.1, sRecall);
    newState = "review";
    let days = nextInterval(newStability, requestRetention);
    if (rating === RATING_HARD) {
      days = Math.max(1, Math.round(days * 0.7));
    }
    intervalSec = 86400 * days;
  }

  const newReps = reps + 1;
  const newDue = now + intervalSec;

  return {
    word: card.word,
    state: newState,
    stability: Number(newStability.toFixed(4)),
    difficulty: Number(newDifficulty.toFixed(4)),
    reps: newReps,
    lapses: newLapses,
    last_review: now,
    due: newDue,
    rating,
    retrievability: Number(rCurrent.toFixed(4)),
    interval_days: Number((intervalSec / 86400.0).toFixed(2))
  };
}
