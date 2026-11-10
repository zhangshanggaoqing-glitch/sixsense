export type VocabCardStage = "front" | "reveal_feedback" | "quiz" | "quiz_result";

/** 会了 enters the listening quiz. 不会 / 模糊 reveal the gloss. */
export function stageAfterRating(rating: 1 | 2 | 3): VocabCardStage {
  return rating === 3 ? "quiz" : "reveal_feedback";
}

export function sessionCompletionCopy(dueCount: number): { title: string; detail: string } {
  if (dueCount > 0) {
    return {
      title: "本次新词已学完",
      detail: `仍有 ${dueCount} 个到期词未完成，还不能算全部完成。`,
    };
  }
  return {
    title: "今日新词已完成",
    detail: "暂无到期复习。记忆曲线已更新，明天再来！",
  };
}

/** First caller wins. Used to ignore a double click on the same card. */
export function beginExclusiveAction(lock: { current: boolean }): boolean {
  if (lock.current) return false;
  lock.current = true;
  return true;
}
