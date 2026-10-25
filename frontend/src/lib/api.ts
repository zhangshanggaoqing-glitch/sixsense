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

export interface WordDefinition {
  pos?: string;
  meaning: string;
}

export interface WordLookupResult {
  word: string;
  lemma: string;
  phonetic_uk: string;
  phonetic_us: string;
  audio_uk: string;
  audio_us: string;
  audio_uk_direct?: string;
  audio_us_direct?: string;
  definitions: WordDefinition[];
  tags?: string[];
  examples?: Array<{ en: string; zh: string }>;
}

export interface VocabItem {
  id: string;
  word: string;
  lemma: string;
  phonetic: string;
  phonetic_uk?: string;
  phonetic_us?: string;
  audio_uk?: string;
  audio_us?: string;
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

export interface StatsData {
  today_minutes: number;
  this_week_minutes: number;
  streak_days: number;
  vocab_count: number;
  dictation_count: number;
  medals?: string[];
}

export interface HeartbeatResponse {
  status: string;
  today_active_seconds: number;
  today_minutes: number;
  streak_days: number;
  medals: string[];
  new_medals: string[];
}

import { getStoredToken, User } from "./auth";
import { getOrCreateGuestId } from "./guest";

async function authFetch(input: RequestInfo | URL, init?: RequestInit): Promise<Response> {
  const token = getStoredToken();
  const headers = new Headers(init?.headers || {});
  if (token && !headers.has("Authorization")) {
    headers.set("Authorization", `Bearer ${token}`);
  } else if (!token && !headers.has("X-Guest-Id")) {
    headers.set("X-Guest-Id", getOrCreateGuestId());
  }
  return fetch(input, { ...init, headers });
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
    const res = await authFetch(`${API_BASE}/progress/dictation/check`, {
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
    const res = await authFetch(`${API_BASE}/progress/resume`);
    if (!res.ok) throw new Error("Failed to fetch resume");
    return res.json();
  },

  async saveResume(state: ResumeState): Promise<void> {
    await authFetch(`${API_BASE}/progress/resume`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(state),
    });
  },

  async sendHeartbeat(
    examId: string,
    activeSeconds: number,
    keepalive = false,
    completedSentence = false
  ): Promise<HeartbeatResponse | null> {
    const token = getStoredToken();
    const guestId = getOrCreateGuestId();
    const headers: Record<string, string> = { "Content-Type": "application/json" };
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    } else {
      headers["X-Guest-Id"] = guestId;
    }
    try {
      const res = await fetch(`${API_BASE}/progress/heartbeat`, {
        method: "POST",
        headers,
        body: JSON.stringify({
          exam_id: examId,
          active_seconds: activeSeconds,
          completed_sentence: completedSentence,
        }),
        keepalive,
      });
      if (res.ok) {
        return await res.json();
      }
      return null;
    } catch {
      // Quiet fail to never disturb playback
      return null;
    }
  },

  async getStats(): Promise<StatsData> {
    const res = await authFetch(`${API_BASE}/progress/stats`);
    if (!res.ok) throw new Error("Failed to fetch stats");
    return res.json();
  },

  async getVocabulary(): Promise<VocabItem[]> {
    const res = await authFetch(`${API_BASE}/vocab`);
    if (!res.ok) throw new Error("Failed to fetch vocabulary");
    return res.json();
  },

  async addVocabulary(data: Partial<VocabItem>): Promise<{ id: string; status: string }> {
    const res = await authFetch(`${API_BASE}/vocab`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    if (!res.ok) throw new Error("Failed to add vocabulary");
    return res.json();
  },

  async deleteVocabulary(id: string): Promise<void> {
    await authFetch(`${API_BASE}/vocab/${id}`, { method: "DELETE" });
  },

  async lookupWord(word: string): Promise<WordLookupResult> {
    const res = await fetch(`${API_BASE}/dict/lookup?word=${encodeURIComponent(word)}`);
    if (!res.ok) throw new Error("Failed to look up word");
    return res.json();
  },

  getVoiceUrl(word: string, type: 1 | 2): string {
    return `${API_BASE}/dict/voice?word=${encodeURIComponent(word)}&type=${type}`;
  },

  async register(username: string, password: string, migrateGuest = true): Promise<{ token: string; user: User }> {
    const guestId = getOrCreateGuestId();
    const res = await fetch(`${API_BASE}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, migrate_guest: migrateGuest, guest_id: guestId }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "注册失败，请稍后重试");
    }
    return data;
  },

  async login(username: string, password: string, migrateGuest = true): Promise<{ token: string; user: User }> {
    const guestId = getOrCreateGuestId();
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password, migrate_guest: migrateGuest, guest_id: guestId }),
    });
    const data = await res.json();
    if (!res.ok) {
      throw new Error(data.detail || "用户名或密码错误");
    }
    return data;
  },

  async getMe(): Promise<User | null> {
    const res = await authFetch(`${API_BASE}/auth/me`);
    if (!res.ok) return null;
    const data = await res.json();
    return data.user;
  },

  async getAdminOverview(): Promise<AdminOverview> {
    const res = await authFetch(`${API_BASE}/admin/overview`);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "获取后台总览数据失败");
    }
    const data = await res.json();
    return data.data;
  },

  async getAdminUsers(query?: string): Promise<{ total: number; users: AdminUserItem[] }> {
    const url = query ? `${API_BASE}/admin/users?q=${encodeURIComponent(query)}` : `${API_BASE}/admin/users`;
    const res = await authFetch(url);
    if (!res.ok) {
      const err = await res.json().catch(() => ({}));
      throw new Error(err.detail || "获取用户列表失败");
    }
    return res.json();
  },

  async getAdminPopularWords(limit = 15): Promise<AdminPopularWord[]> {
    const res = await authFetch(`${API_BASE}/admin/popular-words?limit=${limit}`);
    if (!res.ok) throw new Error("获取热门生词失败");
    const data = await res.json();
    return data.words;
  },

  async getAdminPopularExams(limit = 10): Promise<AdminPopularExam[]> {
    const res = await authFetch(`${API_BASE}/admin/popular-exams?limit=${limit}`);
    if (!res.ok) throw new Error("获取热门试卷失败");
    const data = await res.json();
    return data.exams;
  },
};

export interface AdminOverview {
  total_pv?: number;
  total_uv?: number;
  today_pv?: number;
  today_uv?: number;
  total_users: number;
  today_new_users: number;
  active_users_today: number;
  total_listening_minutes: number;
  today_listening_minutes: number;
  total_vocab_words: number;
  today_vocab_words: number;
  total_dictation_attempts: number;
  avg_dictation_accuracy: number;
}

export interface AdminUserItem {
  id: string;
  username: string;
  created_at: number;
  last_login_at?: number;
  vocab_count: number;
  listening_minutes: number;
  dictation_count: number;
}

export interface AdminPopularWord {
  word: string;
  part_of_speech: string;
  definition_zh: string;
  phonetic_uk: string;
  phonetic_us: string;
  count: number;
}

export interface AdminPopularExam {
  exam_id: string;
  title: string;
  session_count: number;
  total_minutes: number;
}
