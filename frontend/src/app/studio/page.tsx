"use client";

import React, { useState, useEffect, useRef, useCallback, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import {
  ChevronLeft,
  ChevronDown,
  HelpCircle,
  Search,
  BookOpen,
  CheckCircle2,
  ArrowRight,
  X,
  User as UserIcon,
  LogIn,
  Play,
} from "lucide-react";
import { api, ExamDetail, Sentence, Subpart, Question, ResumeState } from "@/lib/api";
import { formatExamTitleZh, formatSubpartTitleZh } from "@/lib/formatters";
import { useAudioPlayer } from "@/hooks/useAudioPlayer";
import { useKeyboardShortcuts, StudioMode } from "@/hooks/useKeyboardShortcuts";
import { useAuth } from "@/hooks/useAuth";
import { SentenceCard } from "@/components/studio/SentenceCard";
import { AudioBar } from "@/components/studio/AudioBar";
import { QuestionsModal } from "@/components/studio/QuestionsModal";
import { QuickLookupModal } from "@/components/studio/QuickLookupModal";
import { ShareCardModal } from "@/components/studio/ShareCardModal";

function StudioContent() {
  const router = useRouter();
  const { user, isLoggedIn, logout } = useAuth();
  const searchParams = useSearchParams();
  const urlSubpartId = searchParams.get("subpart_id") || searchParams.get("subpartId");
  const urlExamId = searchParams.get("exam_id") || searchParams.get("examId") || searchParams.get("id") || "2026-06-set1";

  const [exam, setExam] = useState<ExamDetail | null>(null);
  const [subparts, setSubparts] = useState<Subpart[]>([]);
  const [activeSubpartId, setActiveSubpartId] = useState<string>("");
  const [sentences, setSentences] = useState<Sentence[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [displayMode, setDisplayMode] = useState<StudioMode>("bilingual");
  const [isQuestionsOpen, setIsQuestionsOpen] = useState(false);
  const [isLookupOpen, setIsLookupOpen] = useState(false);
  const [showShortcutTip, setShowShortcutTip] = useState(false);
  const [hasCompletedSentence, setHasCompletedSentence] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  // Retention & Punch Card states
  const [todayMinutes, setTodayMinutes] = useState(0.0);
  const [streakDays, setStreakDays] = useState(0);
  const [isPunchCardOpen, setIsPunchCardOpen] = useState(false);
  const [showDailyPunchPrompt, setShowDailyPunchPrompt] = useState(false);
  const [medalToast, setMedalToast] = useState<string | null>(null);

  // Synchronously restore initialSentenceIndex from cached resume to prevent jumping
  const [initialSentenceIndex, setInitialSentenceIndex] = useState<number>(() => {
    if (typeof window !== "undefined") {
      try {
        const cached = localStorage.getItem("stone_cached_resume");
        if (cached) {
          const parsed = JSON.parse(cached);
          if (parsed && parsed.exam_id === urlExamId && (!urlSubpartId || parsed.subpart_id === urlSubpartId)) {
            return parsed.sentence_index || 0;
          }
        }
      } catch {}
    }
    return 0;
  });

  // Active playing time tracking (guaranteed flush on pause, switch, visibility change, and unload)
  const pendingActiveSecondsRef = useRef(0);
  const pendingCompletedSentenceRef = useRef(false);
  const lastTickTimeRef = useRef<number | null>(null);

  // 1. Check first-time entry for keyboard shortcut tip
  useEffect(() => {
    try {
      const seen = localStorage.getItem("has_seen_shortcuts_tip");
      if (!seen) {
        setShowShortcutTip(true);
        const timer = setTimeout(() => {
          setShowShortcutTip(false);
          localStorage.setItem("has_seen_shortcuts_tip", "true");
        }, 6000);
        return () => clearTimeout(timer);
      }
    } catch {
      // Ignore storage errors in private browsing
    }
  }, []);

  const dismissShortcutTip = () => {
    setShowShortcutTip(false);
    try {
      localStorage.setItem("has_seen_shortcuts_tip", "true");
    } catch {}
  };

  // 2. Initial Load: Exam detail & Subparts
  useEffect(() => {
    async function init() {
      setIsLoading(true);
      setIsError(false);
      try {
        const [examData, subpartsList, resume, statsData] = await Promise.all([
          api.getExamDetail(urlExamId),
          api.getSubparts(urlExamId),
          api.getResume().catch(() => null),
          api.getStats().catch(() => null),
        ]);

        setExam(examData);
        setSubparts(subpartsList);

        if (statsData) {
          setTodayMinutes(statsData.today_minutes || 0.0);
          setStreakDays(statsData.streak_days || 0);
        }

        // Determine active subpart
        let targetSubpartId = urlSubpartId;
        if (targetSubpartId && !subpartsList.some((sp) => sp.id === targetSubpartId)) {
          targetSubpartId = null;
        }
        if (!targetSubpartId && resume?.subpart_id && resume?.exam_id === urlExamId && subpartsList.some((sp) => sp.id === resume.subpart_id)) {
          targetSubpartId = resume.subpart_id;
        }
        if (!targetSubpartId && subpartsList.length > 0) {
          targetSubpartId = subpartsList[0].id;
        }

        setActiveSubpartId(targetSubpartId || "");

        // Set initial sentence index if resume matches this subpart and exam
        if (resume && resume.exam_id === urlExamId && (!targetSubpartId || resume.subpart_id === targetSubpartId)) {
          if (typeof resume.sentence_index === "number") {
            setInitialSentenceIndex(resume.sentence_index);
          }
        }

        // Map resume display_mode (defaults to bilingual for optimal first-listen success)
        if (resume?.display_mode) {
          if (resume.display_mode === "C") setDisplayMode("blind");
          else if (resume.display_mode === "D") setDisplayMode("dictation");
          else setDisplayMode("bilingual");
        } else {
          setDisplayMode("bilingual");
        }
      } catch (err) {
        console.error("Failed to initialize studio", err);
        setIsError(true);
      } finally {
        setIsLoading(false);
      }
    }
    init();
  }, [urlExamId, urlSubpartId]);

  // 3. Load Sentences & Questions when activeSubpartId changes
  useEffect(() => {
    if (!activeSubpartId || !exam) return;

    async function loadSubpartContent() {
      try {
        const [subSentences, subQuestions] = await Promise.all([
          api.getSentences(exam!.id, activeSubpartId),
          api.getQuestions(exam!.id, activeSubpartId).catch(() => []),
        ]);
        setSentences(subSentences);
        setQuestions(subQuestions);
      } catch (err) {
        console.error("Failed to load subpart content", err);
      }
    }

    loadSubpartContent();
  }, [activeSubpartId, exam]);

  const isPlayingRef = useRef(false);
  const persistResumeRef = useRef<(targetIndex?: number, isCompleted?: boolean) => void>(() => {});

  const flushHeartbeat = useCallback((keepalive = false) => {
    if (!exam) return;
    if (isPlayingRef.current && lastTickTimeRef.current !== null) {
      const now = Date.now();
      const elapsed = Math.floor((now - lastTickTimeRef.current) / 1000);
      if (elapsed > 0) {
        pendingActiveSecondsRef.current += elapsed;
        lastTickTimeRef.current = now;
      }
    }
    const sec = pendingActiveSecondsRef.current;
    const completedSentence = pendingCompletedSentenceRef.current;
    if (sec > 0 || completedSentence) {
      pendingActiveSecondsRef.current = 0;
      pendingCompletedSentenceRef.current = false;
      api.sendHeartbeat(exam.id, sec, keepalive, completedSentence).then((res) => {
        if (res) {
          if (res.today_minutes !== undefined) setTodayMinutes(res.today_minutes);
          if (res.streak_days !== undefined) setStreakDays(res.streak_days);

          // Update local cached stats so home page has fresh numbers immediately
          try {
            const cached = localStorage.getItem("stone_cached_stats");
            const s = cached ? JSON.parse(cached) : {};
            s.today_minutes = res.today_minutes;
            s.streak_days = res.streak_days;
            if (res.medals) s.medals = res.medals;
            localStorage.setItem("stone_cached_stats", JSON.stringify(s));
          } catch {}

          // Medal unlock toast (short, non-modal, Apple-style)
          if (res.new_medals && res.new_medals.length > 0) {
            const MEDAL_MAP: Record<string, string> = {
              first_listen: "首听",
              streak_3: "连续 3 天",
              streak_7: "连续 7 天",
            };
            for (const m of res.new_medals) {
              if (MEDAL_MAP[m]) {
                setMedalToast(`已点亮：${MEDAL_MAP[m]}`);
                setTimeout(() => setMedalToast(null), 3500);
              }
            }
          }

          // Trigger B: First time today reaching >= 60s
          if (res.today_active_seconds >= 60) {
            const nowD = new Date();
            const utc = nowD.getTime() + nowD.getTimezoneOffset() * 60000;
            const cst = new Date(utc + 3600000 * 8);
            const todayStr = `${cst.getFullYear()}-${String(cst.getMonth() + 1).padStart(2, "0")}-${String(cst.getDate()).padStart(2, "0")}`;
            try {
              const promptedDate = localStorage.getItem("stone_punch_prompt_date");
              if (promptedDate !== todayStr) {
                localStorage.setItem("stone_punch_prompt_date", todayStr);
                setShowDailyPunchPrompt(true);
              }
            } catch {}
          }
        }
      });
    }
  }, [exam]);

  const handleSentenceChange = useCallback((newIdx: number) => {
    persistResumeRef.current(newIdx, false);
  }, []);

  const handleSentenceComplete = useCallback((idx: number) => {
    setHasCompletedSentence(true);
    pendingCompletedSentenceRef.current = true;
    flushHeartbeat(false);
    const nextIdx = idx < sentences.length - 1 ? idx + 1 : idx;
    const isCompleted = idx >= sentences.length - 1;
    persistResumeRef.current(nextIdx, isCompleted);
  }, [flushHeartbeat, sentences.length]);

  const audioUrl = exam ? api.getAudioUrl(exam.audio_file) : "";

  const player = useAudioPlayer({
    audioUrl,
    sentences,
    initialIndex: initialSentenceIndex,
    initialRate: 1.0,
    initialLoop: "off",
    onSentenceChange: handleSentenceChange,
    onSentenceComplete: handleSentenceComplete,
  });

  isPlayingRef.current = player.isPlaying;

  // Reliable persist resume (saves to localStorage synchronously and syncs with backend)
  const persistResume = useCallback(
    (targetIndex?: number, isCompleted = false) => {
      if (!exam || !activeSubpartId) return;
      const idx = targetIndex !== undefined ? targetIndex : player.currentIndex;
      const resumeData: ResumeState = {
        exam_id: exam.id,
        subpart_id: activeSubpartId,
        sentence_index: idx,
        playback_rate: player.playbackRate,
        display_mode: displayMode === "blind" ? "C" : displayMode === "dictation" ? "D" : "A",
        loop_mode: player.loopMode,
        volume: player.volume,
        has_progress: true,
        is_completed: isCompleted,
      };
      api.saveResume(resumeData);
    },
    [exam, activeSubpartId, player.currentIndex, player.playbackRate, player.loopMode, player.volume, displayMode]
  );

  persistResumeRef.current = persistResume;

  // Persist resume immediately whenever playback pauses
  useEffect(() => {
    if (!player.isPlaying && sentences.length > 0 && exam) {
      persistResume(player.currentIndex, false);
    }
  }, [player.isPlaying, player.currentIndex, sentences.length, exam, persistResume]);

  // Autoplay support when user arrives from "先听一句" or "继续第 N 句"
  const autoplayParam = searchParams.get("autoplay");
  const hasTriggeredAutoplayRef = useRef(false);

  useEffect(() => {
    if (
      (autoplayParam === "1" || autoplayParam === "true") &&
      !hasTriggeredAutoplayRef.current &&
      sentences.length > 0 &&
      exam &&
      player.currentSentence
    ) {
      hasTriggeredAutoplayRef.current = true;
      player.play();
    }
  }, [autoplayParam, sentences, exam, player]);

  // Real-time second counter: throttles heartbeat every 10s and flushes on pause
  useEffect(() => {
    if (!player.isPlaying) {
      lastTickTimeRef.current = null;
      return;
    }

    lastTickTimeRef.current = Date.now();
    const interval = setInterval(() => {
      const now = Date.now();
      if (lastTickTimeRef.current !== null) {
        const delta = Math.floor((now - lastTickTimeRef.current) / 1000);
        if (delta >= 1) {
          pendingActiveSecondsRef.current += delta;
          lastTickTimeRef.current = now;
        }
      }
      if (pendingActiveSecondsRef.current >= 10) {
        flushHeartbeat(false);
      }
    }, 1000);

    return () => {
      clearInterval(interval);
      flushHeartbeat(false);
    };
  }, [player.isPlaying, flushHeartbeat]);

  // Flush on visibility change, pagehide, or unmount
  useEffect(() => {
    const handleVisibility = () => {
      if (document.visibilityState === "hidden") {
        flushHeartbeat(true);
        persistResumeRef.current();
      }
    };
    const handleUnload = () => {
      flushHeartbeat(true);
      persistResumeRef.current();
    };

    document.addEventListener("visibilitychange", handleVisibility);
    window.addEventListener("pagehide", handleUnload);
    window.addEventListener("beforeunload", handleUnload);

    return () => {
      document.removeEventListener("visibilitychange", handleVisibility);
      window.removeEventListener("pagehide", handleUnload);
      window.removeEventListener("beforeunload", handleUnload);
      flushHeartbeat(true);
      persistResumeRef.current();
    };
  }, [flushHeartbeat]);

  // Switch Subpart Handler
  const handleSelectSubpart = (newSubpartId: string) => {
    if (newSubpartId === activeSubpartId) return;
    flushHeartbeat(false);
    persistResume();
    setActiveSubpartId(newSubpartId);
    router.replace(`/studio?exam_id=${exam?.id || urlExamId}&subpart_id=${newSubpartId}`);
  };

  // Switch to next subpart
  const handleNextSubpart = () => {
    const currentIndex = subparts.findIndex((sp) => sp.id === activeSubpartId);
    if (currentIndex >= 0 && currentIndex + 1 < subparts.length) {
      handleSelectSubpart(subparts[currentIndex + 1].id);
    }
  };

  // Periodic background sync of resume state (every 2s if state changed)
  useEffect(() => {
    if (!exam || sentences.length === 0) return;
    const timer = setTimeout(() => {
      persistResume();
    }, 2000);
    return () => clearTimeout(timer);
  }, [player.currentIndex, player.playbackRate, player.loopMode, player.volume, displayMode, exam, sentences, activeSubpartId, persistResume]);

  // Single-sentence Loop toggle (R shortcut)
  const handleToggleLoop = () => {
    player.cycleLoopMode();
  };

  // Keyboard Shortcuts: 空格播放暂停，←/→ 上下一句，R 循环，1/2/3 切模式
  useKeyboardShortcuts({
    onTogglePlay: player.togglePlay,
    onNext: player.nextSentence,
    onPrev: player.prevSentence,
    onToggleLoop: handleToggleLoop,
    onSelectMode: (mode) => setDisplayMode(mode),
    onSpeedDown: () => player.adjustSpeed(-0.1),
    onSpeedUp: () => player.adjustSpeed(0.1),
    isDictating: displayMode === "dictation",
  });

  const currentSubpart = subparts.find((sp) => sp.id === activeSubpartId) || subparts[0];
  const isLastSentence = player.currentIndex === sentences.length - 1 && sentences.length > 0;
  const currentSubpartIndex = subparts.findIndex((sp) => sp.id === activeSubpartId);
  const nextSubpart = currentSubpartIndex >= 0 && currentSubpartIndex + 1 < subparts.length ? subparts[currentSubpartIndex + 1] : null;

  // Loading state
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7] dark:bg-[#000000]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-7 h-7 border-2 border-[#0071e3] border-t-transparent rounded-full animate-spin" />
          <span className="text-sm font-medium text-[#86868b]">正在准备听力材料…</span>
        </div>
      </div>
    );
  }

  // Error state
  if (isError || !exam) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7] dark:bg-[#000000] p-6 text-center">
        <div className="flex flex-col items-center gap-3 max-w-sm">
          <p className="text-sm font-medium text-[#86868b]">音频材料加载失败，请检查网络</p>
          <button
            onClick={() => window.location.reload()}
            className="px-5 py-2 text-xs font-semibold rounded-full bg-[#0071e3] text-white hover:bg-[#0077ed] transition-colors"
          >
            点击重试
          </button>
        </div>
      </div>
    );
  }

  const currentSentence = player.currentSentence || sentences[0];
  const examTitleZh = formatExamTitleZh(exam.title || exam.id);
  const currentSubpartTitleZh = formatSubpartTitleZh(currentSubpart?.title, currentSubpart?.question_range);
  const isConversation = Boolean(
    currentSubpart?.type === "conversation" ||
    currentSubpart?.section_id?.toLowerCase().endsWith("sec-a") ||
    currentSubpart?.section_id?.toLowerCase().endsWith("section-a") ||
    /长对话/i.test(currentSubpartTitleZh) ||
    /conversation/i.test(currentSubpart?.title || "")
  );

  return (
    <div className="h-[100dvh] min-h-[100dvh] flex flex-col justify-between bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] select-none overflow-hidden">
      {/* Top Header: 专注设计，移动端/桌面端完美适配 */}
      <header className="w-full max-w-5xl mx-auto px-3.5 sm:px-6 pt-[max(0.6rem,env(safe-area-inset-top))] pb-2 sm:py-3.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 sm:gap-4 shrink-0 border-b border-black/[0.03] dark:border-white/[0.04] sm:border-none">
        {/* Row 1: Left Back/Subpart + Right Action Tools */}
        <div className="flex items-center justify-between w-full sm:w-auto gap-2">
          {/* Left: 首页导航 + 分节下拉菜单 */}
          <div className="flex items-center gap-1.5 sm:gap-3 shrink-0">
            <Link
              href="/"
              className="flex items-center gap-0.5 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] p-1 -ml-1 rounded-full transition-colors active:scale-95"
            >
              <ChevronLeft className="w-4 h-4" />
              <span className="hidden sm:inline">首页</span>
            </Link>
            <span className="text-black/10 dark:text-white/10 hidden sm:inline">·</span>

            {/* Subpart Switcher Dropdown */}
            <div className="relative max-w-[160px] xs:max-w-[190px] sm:max-w-none">
              <select
                value={activeSubpartId}
                onChange={(e) => handleSelectSubpart(e.target.value)}
                className="appearance-none bg-black/[0.04] dark:bg-white/[0.08] hover:bg-black/[0.07] dark:hover:bg-white/[0.12] text-xs font-medium text-[#1d1d1f] dark:text-[#f5f5f7] pl-2.5 sm:pl-3 pr-6 sm:pr-7 py-1.5 rounded-full cursor-pointer focus:outline-none transition-colors border-none truncate w-full"
              >
                {subparts.map((sp) => (
                  <option key={sp.id} value={sp.id} className="dark:bg-[#1c1c1e] text-[#1d1d1f] dark:text-[#f5f5f7]">
                    {examTitleZh} · {formatSubpartTitleZh(sp.title, sp.question_range)}
                  </option>
                ))}
              </select>
              <ChevronDown className="w-3.5 h-3.5 text-[#86868b] absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none" />
            </div>
          </div>

          {/* Right Tools (Mobile row 1 right): 考题, 查词, 生词本, 用户 */}
          <div className="flex sm:hidden items-center gap-1 shrink-0">
            {questions.length > 0 && (
              <button
                onClick={() => setIsQuestionsOpen(true)}
                className="flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-medium text-[#0071e3] dark:text-[#0a84ff] bg-[#0071e3]/10 dark:bg-[#0a84ff]/15 active:scale-95 transition-colors"
                title="查看六级官方原题与选项"
              >
                <HelpCircle className="w-3.5 h-3.5" />
                <span>考题</span>
              </button>
            )}

            <button
              onClick={() => setIsLookupOpen(true)}
              className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] active:scale-95 transition-colors"
              title="查词典"
            >
              <Search className="w-4 h-4" />
            </button>

            <Link
              href="/vocabulary"
              className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] active:scale-95 transition-colors"
              title="生词本"
            >
              <BookOpen className="w-4 h-4" />
            </Link>

            {isLoggedIn ? (
              <button
                onClick={logout}
                className="text-[11px] text-[#86868b] hover:text-[#ff3b30] px-1 py-0.5 rounded transition-colors"
                title="退出当前登录"
              >
                {user?.username}
              </button>
            ) : (
              <Link
                href={`/login?redirect=/studio?exam_id=${exam.id}&subpart_id=${activeSubpartId}`}
                className="text-xs font-medium px-2 py-1 rounded-full text-[#0071e3] bg-[#0071e3]/10 flex items-center gap-0.5"
                title="登录"
              >
                <LogIn className="w-3 h-3" />
              </Link>
            )}
          </div>
        </div>

        {/* Center: Apple Segmented Control: 盲听 ｜ 双语 ｜ 听写 (Desktop centered, Mobile full width) */}
        <div className="flex items-center justify-center bg-black/[0.05] dark:bg-white/[0.08] p-0.5 rounded-full text-xs font-medium w-full sm:w-auto mx-auto sm:mx-0">
          <button
            onClick={() => setDisplayMode("blind")}
            className={`flex-1 sm:flex-initial px-3 sm:px-4 py-1.5 rounded-full transition-all active:scale-95 ${
              displayMode === "blind"
                ? "bg-white dark:bg-[#2c2c2e] text-[#0071e3] dark:text-[#0a84ff] font-semibold shadow-xs"
                : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
            }`}
            title="纯音频听力训练 (快捷键: 1)"
          >
            盲听
          </button>

          <button
            onClick={() => setDisplayMode("bilingual")}
            className={`flex-1 sm:flex-initial px-3 sm:px-4 py-1.5 rounded-full transition-all active:scale-95 ${
              displayMode === "bilingual"
                ? "bg-white dark:bg-[#2c2c2e] text-[#0071e3] dark:text-[#0a84ff] font-semibold shadow-xs"
                : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
            }`}
            title="英中文本对照精听 (快捷键: 2)"
          >
            双语
          </button>

          <button
            onClick={() => setDisplayMode("dictation")}
            className={`flex-1 sm:flex-initial px-3 sm:px-4 py-1.5 rounded-full transition-all active:scale-95 ${
              displayMode === "dictation"
                ? "bg-white dark:bg-[#2c2c2e] text-[#0071e3] dark:text-[#0a84ff] font-semibold shadow-xs"
                : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
            }`}
            title="单句听写实战训练 (快捷键: 3)"
          >
            听写
          </button>
        </div>

        {/* Right Tools (Desktop only): 考题, 查词, 生词本, 用户 */}
        <div className="hidden sm:flex items-center gap-1 sm:gap-2 shrink-0">
          {questions.length > 0 && (
            <button
              onClick={() => setIsQuestionsOpen(true)}
              className="flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium text-[#0071e3] dark:text-[#0a84ff] bg-[#0071e3]/10 dark:bg-[#0a84ff]/15 hover:bg-[#0071e3]/20 transition-colors"
              title="查看六级官方原题与选项"
            >
              <HelpCircle className="w-3.5 h-3.5" />
              <span>考题</span>
            </button>
          )}

          <button
            onClick={() => setIsLookupOpen(true)}
            className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 transition-colors"
            title="查词典 / 英美发音与释义"
          >
            <Search className="w-4 h-4" />
          </button>

          <Link
            href="/vocabulary"
            className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 transition-colors"
            title="生词本"
          >
            <BookOpen className="w-4 h-4" />
          </Link>

          {isLoggedIn ? (
            <div className="flex items-center gap-1.5 pl-1.5 border-l border-black/[0.08] dark:border-white/[0.1]">
              <span className="text-[11px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-1">
                <UserIcon className="w-3.5 h-3.5 text-[#0071e3]" />
                <span className="hidden sm:inline">{user?.username}</span>
              </span>
              <button
                onClick={logout}
                className="text-[11px] text-[#86868b] hover:text-[#ff3b30] px-1 transition-colors"
                title="退出当前登录"
              >
                退出
              </button>
            </div>
          ) : (
            <Link
              href={`/login?redirect=/studio?exam_id=${exam.id}&subpart_id=${activeSubpartId}`}
              className="text-xs font-medium px-2.5 py-1 rounded-full text-[#86868b] hover:text-[#0071e3] hover:bg-[#0071e3]/10 transition-colors flex items-center gap-1"
              title="登录以同步生词本与进度"
            >
              <LogIn className="w-3.5 h-3.5" />
              <span className="hidden sm:inline">登录</span>
            </Link>
          )}
        </div>
      </header>

      {/* Main Focus Area (一屏一个主角) */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 relative overflow-y-auto no-scrollbar">
        {player.isBuffering && (
          <div className="absolute top-2 text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] animate-pulse">
            音频加载中…
          </div>
        )}

        {currentSentence ? (
          <SentenceCard
            sentence={currentSentence}
            displayMode={displayMode}
            isPlaying={player.isPlaying}
            examId={exam.id}
            onNext={player.nextSentence}
            onReplay={player.replay}
            onTogglePlay={player.togglePlay}
            isConversation={isConversation}
          />
        ) : (
          <div className="text-sm text-[#86868b]">暂无听力句子数据</div>
        )}

        {/* Autoplay blocked or click-to-play invitation in center of viewport */}
        {!player.isPlaying && (
          <div className="mt-4 animate-in fade-in duration-200">
            <button
              type="button"
              onClick={player.togglePlay}
              className="inline-flex items-center gap-2 px-6 py-2.5 rounded-full bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] text-xs font-semibold shadow-md active:scale-95 transition-all"
            >
              <Play className="w-3.5 h-3.5 fill-current ml-0.5" />
              <span>点击播放</span>
            </button>
          </div>
        )}

        {/* End of Subpart Transition Notification */}
        {isLastSentence && (
          <div className="mt-4 flex items-center gap-3 animate-in fade-in duration-300">
            <span className="text-xs text-[#86868b] flex items-center gap-1.5">
              <CheckCircle2 className="w-4 h-4 text-[#34c759]" />
              本篇精听完毕（共 {sentences.length} 句）
            </span>
            {nextSubpart && (
              <button
                onClick={handleNextSubpart}
                className="flex items-center gap-1 text-xs font-semibold px-4 py-1.5 rounded-full bg-[#1d1d1f] text-white dark:bg-[#f5f5f7] dark:text-[#1d1d1f] hover:opacity-90 shadow-sm transition-all"
              >
                下一题：{formatSubpartTitleZh(nextSubpart.title, nextSubpart.question_range)} <ArrowRight className="w-3 h-3" />
              </button>
            )}
          </div>
        )}
      </main>

      {/* Bottom Floating Frosted Glass Audio Bar with Safe Area */}
      <footer className="w-full pb-[max(1.25rem,calc(env(safe-area-inset-bottom)+0.6rem))] pt-1 px-3 sm:px-4 z-30 shrink-0">
        {!isLoggedIn && hasCompletedSentence && (
          <div className="pb-1.5 text-center animate-in fade-in duration-300">
            <span className="text-[11px] text-[#86868b] dark:text-[#a1a1a6]">
              进度已保存在本机 ·{" "}
              <Link
                href={`/login?redirect=/studio?exam_id=${exam.id}&subpart_id=${activeSubpartId}`}
                className="text-[#0071e3] dark:text-[#0a84ff] hover:underline"
              >
                登录保存进度
              </Link>
            </span>
          </div>
        )}
        <AudioBar
          currentIndex={player.currentIndex}
          totalSentences={sentences.length}
          isPlaying={player.isPlaying}
          loopMode={player.loopMode}
          playbackRate={player.playbackRate}
          volume={player.volume}
          onTogglePlay={player.togglePlay}
          onNext={player.nextSentence}
          onPrev={player.prevSentence}
          onCycleLoop={handleToggleLoop}
          onSetSpeed={player.setPlaybackRate}
          onSetVolume={player.adjustVolume}
          onOpenPunchCard={() => setIsPunchCardOpen(true)}
        />
      </footer>

      {/* Trigger B: First time today reaching >= 60s prompt */}
      {showDailyPunchPrompt && (
        <div className="fixed bottom-24 left-1/2 -translate-x-1/2 z-40 flex items-center gap-2.5 px-4 py-2 bg-white/95 dark:bg-[#1c1c1e]/95 backdrop-blur-xl border border-black/[0.08] dark:border-white/[0.12] rounded-full shadow-lg text-xs text-[#1d1d1f] dark:text-[#f5f5f7] animate-in fade-in slide-in-from-bottom-2 duration-200">
          <span>今日已打卡 · 生成分享图</span>
          <button
            type="button"
            onClick={() => {
              setShowDailyPunchPrompt(false);
              setIsPunchCardOpen(true);
            }}
            className="px-2.5 py-0.5 rounded-full text-xs font-semibold bg-[#1d1d1f] text-white dark:bg-[#f5f5f7] dark:text-[#1d1d1f] hover:opacity-90 transition-opacity"
          >
            生成
          </button>
          <button
            type="button"
            onClick={() => setShowDailyPunchPrompt(false)}
            className="p-0.5 rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Silent Medal Toast */}
      {medalToast && (
        <div className="fixed top-14 left-1/2 -translate-x-1/2 z-50 flex items-center gap-1.5 px-4 py-1.5 bg-[#1d1d1f]/95 dark:bg-[#f5f5f7]/95 text-white dark:text-[#1d1d1f] backdrop-blur-md rounded-full shadow-md text-xs font-medium animate-in fade-in slide-in-from-top-2 duration-200">
          <span>{medalToast}</span>
        </div>
      )}

      {/* Share Punch Card Modal */}
      <ShareCardModal
        isOpen={isPunchCardOpen}
        onClose={() => setIsPunchCardOpen(false)}
        todayMinutes={todayMinutes}
        streakDays={streakDays}
      />

      {/* First-time Entry Shortcut Toast (Corner Hint) */}
      {showShortcutTip && (
        <div className="fixed bottom-24 right-6 z-40 flex items-center gap-2 px-3.5 py-2 bg-white/90 dark:bg-[#2c2c2e]/90 backdrop-blur-md border border-black/[0.08] dark:border-white/[0.1] rounded-full shadow-lg text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] animate-in fade-in slide-in-from-bottom-2 duration-200">
          <span>快捷键：空格 播放 · ←/→ 选句 · R 循环 · 1/2/3 切模式</span>
          <button
            onClick={dismissShortcutTip}
            className="p-0.5 rounded-full hover:bg-black/5 dark:hover:bg-white/10 text-[#86868b] hover:text-[#1d1d1f] transition-colors"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* Official Questions & Options Modal */}
      <QuestionsModal
        isOpen={isQuestionsOpen}
        onClose={() => setIsQuestionsOpen(false)}
        subpartTitle={currentSubpartTitleZh}
        questionRange={currentSubpart?.question_range || ""}
        questions={questions}
      />

      {/* Quick Word Lookup & Pronunciation Modal */}
      <QuickLookupModal
        isOpen={isLookupOpen}
        onClose={() => setIsLookupOpen(false)}
        currentExamId={exam.id}
      />
    </div>
  );
}

export default function StudioPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7] dark:bg-[#000000]">
          <div className="flex flex-col items-center gap-3">
            <div className="w-7 h-7 border-2 border-[#0071e3] border-t-transparent rounded-full animate-spin" />
            <span className="text-sm font-medium text-[#86868b]">正在准备听力材料…</span>
          </div>
        </div>
      }
    >
      <StudioContent />
    </Suspense>
  );
}
