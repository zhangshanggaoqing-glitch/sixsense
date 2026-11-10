/**
 * Pure homepage navigation decisions.
 * Kept separate so year-switch races can be tested without a browser.
 */

export interface ResumePointer {
  exam_id?: string;
  subpart_id?: string;
  sentence_index?: number;
  has_progress?: boolean;
  is_completed?: boolean;
}

export interface ExamSubpartRef {
  id: string;
  exam_id?: string;
}

export interface ContinueTarget {
  href: string;
  label: string;
  sentenceNumber: number;
  continuesSelectedExam: boolean;
}

export function readCachedJson<T>(
  storage: { getItem(key: string): string | null } | null,
  key: string
): T | null {
  if (!storage) return null;
  try {
    const raw = storage.getItem(key);
    if (!raw) return null;
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

/** Keep the last good stats/resume when a refresh request fails. */
export function keepPreviousOnFailure<T>(current: T | null, incoming: T | null): T | null {
  return incoming ?? current;
}

export function takeLatest<T>(requestSeq: number, latestSeq: number, value: T): T | null {
  return requestSeq === latestSeq ? value : null;
}

export function subpartsMatchExam(rows: ExamSubpartRef[], examId: string): boolean {
  if (!examId || rows.length === 0) return false;
  return rows.every((row) => row.exam_id === examId);
}

export function resolveContinueTarget(args: {
  selectedExamId: string;
  resume: ResumePointer | null;
  selectedSubparts: ExamSubpartRef[];
  subpartsBelongToSelected: boolean;
}): ContinueTarget {
  const resume = args.resume;
  const sentenceIndex = Number(resume?.sentence_index);
  const safeIndex = Number.isFinite(sentenceIndex) && sentenceIndex >= 0 ? sentenceIndex : 0;
  const resumeMatches =
    Boolean(resume?.exam_id) &&
    Boolean(resume?.subpart_id) &&
    resume?.exam_id === args.selectedExamId &&
    !resume?.is_completed &&
    (safeIndex > 0 || Boolean(resume?.has_progress));

  if (resumeMatches && resume?.exam_id && resume.subpart_id) {
    const sentenceNumber = safeIndex + 1;
    return {
      href: `/studio?exam_id=${encodeURIComponent(resume.exam_id)}&subpart_id=${encodeURIComponent(resume.subpart_id)}&autoplay=1`,
      label: `继续第 ${sentenceNumber} 句`,
      sentenceNumber,
      continuesSelectedExam: true,
    };
  }

  const first = args.subpartsBelongToSelected ? args.selectedSubparts[0] : undefined;
  const href = first?.id
    ? `/studio?exam_id=${encodeURIComponent(args.selectedExamId)}&subpart_id=${encodeURIComponent(first.id)}&autoplay=1`
    : `/studio?exam_id=${encodeURIComponent(args.selectedExamId)}&autoplay=1`;
  return {
    href,
    label: "先听一句",
    sentenceNumber: 1,
    continuesSelectedExam: false,
  };
}
