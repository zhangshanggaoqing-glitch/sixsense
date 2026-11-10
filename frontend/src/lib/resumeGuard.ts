/**
 * Blocks the studio from saving sentence 0 over a restored later sentence
 * while the player is still hydrating.
 */

export interface ResumeWriteInput {
  resumeLoaded: boolean;
  suppressHydrationWrite: boolean;
  sentenceCount: number;
  targetIndex: number;
  writeIndex: number;
}

export function clampSentenceIndex(index: number, sentenceCount: number): number {
  if (!Number.isFinite(index) || index < 0) return 0;
  if (sentenceCount <= 0) return 0;
  return Math.min(Math.floor(index), sentenceCount - 1);
}

export function shouldCommitResumeWrite(input: ResumeWriteInput): boolean {
  if (!input.resumeLoaded) return false;
  if (input.sentenceCount <= 0) return false;
  if (!input.suppressHydrationWrite) return true;
  const target = clampSentenceIndex(input.targetIndex, input.sentenceCount);
  return input.writeIndex === target;
}

export function readResumeSentenceIndex(value: unknown): number {
  const index = typeof value === "number" ? value : Number(value);
  if (!Number.isFinite(index) || index < 0) return 0;
  return Math.floor(index);
}

/**
 * Heartbeat payload can be flushed from several listeners in one tick.
 * The first consumer sends; a second call with the cleared counters must not.
 */
export function consumePendingProgress(
  pendingSeconds: number,
  pendingCompleted: boolean
): { send: boolean; seconds: number; completed: boolean } {
  const seconds = pendingSeconds > 0 ? pendingSeconds : 0;
  const completed = Boolean(pendingCompleted);
  if (seconds > 0 || completed) {
    return { send: true, seconds, completed };
  }
  return { send: false, seconds: 0, completed: false };
}
