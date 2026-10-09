const API_BASE = typeof window !== "undefined"
  ? "/api"
  : (process.env.BACKEND_URL ? `${process.env.BACKEND_URL}/api` : (process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000/api"));

export interface Sentence {
  id: string;
  order_num: number;
  speaker: string;
  start_time: number;
  end_time: number;
  english: string;
  chinese: string;
  confidence: number;
}

export interface Subpart {
  id: string;
  exam_id?: string;
  section_id: string;
  section_title?: string;
  type: string;
  title: string;
  topic_zh?: string;
  question_range?: string;
  order_num: number;
  start_time: number;
  end_time: number;
  sentence_count?: number;
  duration?: number;
}

export interface Question {
  id: string;
  exam_id: string;
  subpart_id: string;
  question_num: number;
  prompt: string;
  option_a: string;
  option_b: string;
  option_c: string;
  option_d: string;
  correct_answer: string;
  explanation: string;
}

export interface Section {
  id: string;
  type: string;
  title: string;
  order_num: number;
  subparts: Subpart[];
}

export interface ExamItem {
  id: string;
  year: number;
  month: number;
  set_number: number;
  title: string;
  audio_file: string;
  audio_duration: number;
  is_golden: number;
}

export interface ExamDetail {
  id: string;
  year: number;
  month: number;
  set_number: number;
  title: string;
  audio_file: string;
  audio_duration: number;
  sections: Section[];
}

export interface DiffToken {
  type: "match" | "missing" | "extra" | "form_diff" | "spelling_diff";
  standard: string;
  user: string;
}

export interface DiffResult {
  accuracy_score: number;
  is_perfect: boolean;
  diff_tokens: DiffToken[];
  stats: {
    total_words: number;
    matched_words: number;
    missing_words: number;
    extra_words: number;
    form_errors: number;
    spelling_errors: number;
  };
}

export interface VocabItem {
  id: string;
  word: string;
  lemma: string;
  phonetic: string;
  part_of_speech: string;
  definition_zh: string;
  cet_level: string;
  source_sentence_id: string;
  source_sentence_en: string;
  source_sentence_zh: string;
  exam_id: string;
  audio_clip_start: number;
  audio_clip_end: number;
  created_at: number;
}

export interface ResumeState {
  exam_id: string;
  section_id?: string;
  subpart_id?: string;
  sentence_index: number;
  playback_rate: number;
  display_mode: "A" | "B" | "C" | "D";
  loop_mode: "off" | "1x" | "3x" | "5x" | "infinity";
  volume: number;
}

export const api = {
  getAudioUrl(filename: string): string {
    return `${API_BASE}/audio/${encodeURIComponent(filename)}`;
  },

  async getExams(): Promise<ExamItem[]> {
    const res = await fetch(`${API_BASE}/exams`);
    if (!res.ok) throw new Error("Failed to fetch exams");
    return res.json();
  },

  async getExamDetail(examId: string): Promise<ExamDetail> {
    const res = await fetch(`${API_BASE}/exams/${examId}`);
    if (!res.ok) throw new Error("Failed to fetch exam detail");
    return res.json();
  },

  async getSubparts(examId: string): Promise<Subpart[]> {
    const res = await fetch(`${API_BASE}/exams/${examId}/subparts`);
    if (!res.ok) throw new Error("Failed to fetch subparts");
    return res.json();
  },

  async getQuestions(examId: string, subpartId: string): Promise<Question[]> {
    const res = await fetch(`${API_BASE}/exams/${examId}/subparts/${subpartId}/questions`);
    if (!res.ok) throw new Error("Failed to fetch questions");
    return res.json();
  },

  async getSentences(examId: string, subpartId?: string): Promise<Sentence[]> {
    const url = subpartId
      ? `${API_BASE}/exams/${examId}/sentences?subpart_id=${subpartId}`
      : `${API_BASE}/exams/${examId}/sentences`;
    const res = await fetch(url);
    if (!res.ok) throw new Error("Failed to fetch sentences");
    return res.json();
  },

  async checkDictation(sentenceId: string, standardText: string, userInput: string): Promise<DiffResult> {
    const res = await fetch(`${API_BASE}/progress/dictation/check`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        sentence_id: sentenceId,
        standard_text: standardText,
        user_input: userInput,
      }),
    });
    if (!res.ok) throw new Error("Failed to check dictation");
    return res.json();
  },

  async getResume(): Promise<ResumeState> {
    const res = await fetch(`${API_BASE}/progress/resume`);
    if (!res.ok) throw new Error("Failed to fetch resume");
    return res.json();
  },

  async saveResume(state: ResumeState): Promise<void> {
    await fetch(`${API_BASE}/progress/resume`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state),
    });
  },

  async sendHeartbeat(examId: string, activeSeconds: number): Promise<void> {
    await fetch(`${API_BASE}/progress/heartbeat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ exam_id: examId, active_seconds: activeSeconds }),
    });
  },

  async getStats() {
    const res = await fetch(`${API_BASE}/progress/stats`);
    if (!res.ok) throw new Error("Failed to fetch stats");
    return res.json();
  },

  async getVocabulary(): Promise<VocabItem[]> {
    const res = await fetch(`${API_BASE}/vocab`);
    if (!res.ok) throw new Error("Failed to fetch vocabulary");
    return res.json();
  },

  async addVocabulary(data: Partial<VocabItem>): Promise<{ id: string; status: string }> {
    const res = await fetch(`${API_BASE}/vocab`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to add vocabulary");
    return res.json();
  },

  async deleteVocabulary(id: string): Promise<void> {
    await fetch(`${API_BASE}/vocab/${id}`, { method: "DELETE" });
  },
};
