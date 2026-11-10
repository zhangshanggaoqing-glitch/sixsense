import assert from "node:assert/strict";
import test from "node:test";
import {
  keepPreviousOnFailure,
  readCachedJson,
  resolveContinueTarget,
  subpartsMatchExam,
  takeLatest,
} from "../src/lib/homeNavigation.ts";
import {
  consumePendingProgress,
  readResumeSentenceIndex,
  shouldCommitResumeWrite,
} from "../src/lib/resumeGuard.ts";
import {
  beginExclusiveAction,
  sessionCompletionCopy,
  stageAfterRating,
} from "../src/lib/vocabSession.ts";

test("switching the homepage to 2026 does not keep a 2025 continue link", () => {
  const target = resolveContinueTarget({
    selectedExamId: "2026-06-set1",
    resume: {
      exam_id: "2025-12-set2",
      subpart_id: "2025-12-set2-conv-1",
      sentence_index: 8,
      has_progress: true,
      is_completed: false,
    },
    selectedSubparts: [{ id: "2026-06-set1-conv-1", exam_id: "2026-06-set1" }],
    subpartsBelongToSelected: true,
  });
  assert.equal(target.continuesSelectedExam, false);
  assert.equal(target.label, "先听一句");
  assert.match(target.href, /exam_id=2026-06-set1/);
  assert.doesNotMatch(target.href, /2025/);
});

test("continue stays on the selected paper when that paper is the resume", () => {
  const target = resolveContinueTarget({
    selectedExamId: "2025-12-set2",
    resume: {
      exam_id: "2025-12-set2",
      subpart_id: "2025-12-set2-conv-1",
      sentence_index: 3,
      has_progress: true,
    },
    selectedSubparts: [{ id: "2025-12-set2-conv-1", exam_id: "2025-12-set2" }],
    subpartsBelongToSelected: true,
  });
  assert.equal(target.label, "继续第 4 句");
  assert.match(target.href, /subpart_id=2025-12-set2-conv-1/);
});

test("a slow older subpart response cannot replace the newer year", () => {
  const older = [{ id: "2025-a", exam_id: "2025-06-set1" }];
  const newer = [{ id: "2026-a", exam_id: "2026-06-set1" }];
  assert.equal(takeLatest(1, 2, older), null);
  assert.deepEqual(takeLatest(2, 2, newer), newer);
  assert.equal(subpartsMatchExam(older, "2026-06-set1"), false);
  assert.equal(subpartsMatchExam(newer, "2026-06-set1"), true);
});

test("failed refresh keeps the previous stats instead of clearing them", () => {
  const cached = { today_minutes: 12.5, streak_days: 4 };
  assert.deepEqual(keepPreviousOnFailure(cached, null), cached);
  assert.deepEqual(keepPreviousOnFailure(cached, { today_minutes: 13, streak_days: 4 }), {
    today_minutes: 13,
    streak_days: 4,
  });
});

test("broken cached json does not throw or look like an empty account", () => {
  const storage = {
    getItem(key: string) {
      return key === "bad" ? "{not-json" : null;
    },
  };
  assert.equal(readCachedJson(storage, "bad"), null);
  assert.equal(readCachedJson(null, "stone_cached_stats"), null);
});

test("resume hydration refuses to overwrite sentence 4 with sentence 1", () => {
  assert.equal(readResumeSentenceIndex(3), 3);
  assert.equal(readResumeSentenceIndex(0), 0);
  assert.equal(
    shouldCommitResumeWrite({
      resumeLoaded: true,
      suppressHydrationWrite: true,
      sentenceCount: 20,
      targetIndex: 3,
      writeIndex: 0,
    }),
    false
  );
  assert.equal(
    shouldCommitResumeWrite({
      resumeLoaded: false,
      suppressHydrationWrite: false,
      sentenceCount: 20,
      targetIndex: 3,
      writeIndex: 3,
    }),
    false
  );
  assert.equal(
    shouldCommitResumeWrite({
      resumeLoaded: true,
      suppressHydrationWrite: false,
      sentenceCount: 20,
      targetIndex: 3,
      writeIndex: 0,
    }),
    true
  );
});

test("a second heartbeat flush in the same tick does not send again", () => {
  let seconds = 10;
  let completed = true;
  const first = consumePendingProgress(seconds, completed);
  assert.equal(first.send, true);
  seconds = 0;
  completed = false;
  const second = consumePendingProgress(seconds, completed);
  assert.equal(second.send, false);
});

test("due words keep the session from claiming everything is finished", () => {
  const pending = sessionCompletionCopy(2);
  assert.match(pending.title, /新词已学完/);
  assert.match(pending.detail, /2 个到期词/);
  assert.match(pending.detail, /还不能算全部完成/);
  assert.doesNotMatch(pending.detail, /已清理完毕/);
  const clear = sessionCompletionCopy(0);
  assert.match(clear.detail, /暂无到期复习/);
});

test("会了 opens the four-choice quiz; 不会 and 模糊 do not", () => {
  assert.equal(stageAfterRating(1), "reveal_feedback");
  assert.equal(stageAfterRating(2), "reveal_feedback");
  assert.equal(stageAfterRating(3), "quiz");
});

test("duplicate rating clicks do not both acquire the card", () => {
  const lock = { current: false };
  assert.equal(beginExclusiveAction(lock), true);
  assert.equal(beginExclusiveAction(lock), false);
});
