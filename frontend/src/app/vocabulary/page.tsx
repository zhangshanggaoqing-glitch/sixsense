"use client";

import React, { useState, useEffect, useRef, useMemo, useCallback } from "react";
import Link from "next/link";
import {
  ChevronLeft,
  Volume2,
  Check,
  Play,
  X,
  Search,
  ChevronDown,
  ChevronUp,
  Bookmark,
  Settings,
  CheckCircle2,
  ArrowRight
} from "lucide-react";
import {
  api,
  FreqVocabItem,
  FreqSentenceExample,
  VocabItem,
  FreqVocabListResponse,
  VocabDailySummary,
  VocabSettings,
  StudySessionItem
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";
import { formatExamTitleZh } from "@/lib/formatters";

export default function VocabularyPage() {
  const { user } = useAuth();

  // Navigation tab
  const [activeTab, setActiveTab] = useState<"session" | "list" | "bookmarks">("session");
  const [listSubTab, setListSubTab] = useState<"unmastered" | "mastered">("unmastered");

  // Summary & Settings
  const [summary, setSummary] = useState<VocabDailySummary>({
    new_today: 0,
    new_quota: 20,
    review_total: 0,
    due_count: 0,
    mastered_count: 0,
    summary_text: "新词 0/20 · 复习 0 · 到期 0"
  });
  const [settings, setSettings] = useState<VocabSettings>({
    daily_new_quota: 20,
    autoplay_audio: true,
    algorithm_version: "FSRS-5.0.0"
  });
  const [showSettingsModal, setShowSettingsModal] = useState<boolean>(false);
  const [customQuotaInput, setCustomQuotaInput] = useState<string>("20");

  // Study Session (Phase 2 Daily Quantified Queue)
  const [sessionQueue, setSessionQueue] = useState<StudySessionItem[]>([]);
  const [currentSessionIndex, setCurrentSessionIndex] = useState<number>(0);
  const [isLoadingSession, setIsLoadingSession] = useState<boolean>(true);

  // Card Interactive Stage
  // 'front' -> initial review
  // 'reveal_feedback' -> after clicking 不会 or 模糊
  // 'quiz' -> after clicking 会了, entering 4-choice listening quiz
  // 'quiz_result' -> after answering quiz
  const [cardStage, setCardStage] = useState<"front" | "reveal_feedback" | "quiz" | "quiz_result">("front");
  const [lastRatingChoice, setLastRatingChoice] = useState<number>(1);
  const [quizListenCount, setQuizListenCount] = useState<number>(1);
  const [selectedQuizOption, setSelectedQuizOption] = useState<string | null>(null);
  const [isQuizCorrect, setIsQuizCorrect] = useState<boolean | null>(null);
  const [shuffledQuizOptions, setShuffledQuizOptions] = useState<string[]>([]);

  // List View state
  const [freqItems, setFreqItems] = useState<FreqVocabItem[]>([]);
  const [bookmarkedList, setBookmarkedList] = useState<VocabItem[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoadingList, setIsLoadingList] = useState(false);
  const [listPage, setListPage] = useState(1);
  const [hasMoreList, setHasMoreList] = useState(false);
  const [expandedExamplesWord, setExpandedExamplesWord] = useState<string | null>(null);

  // Audio state
  const [playingVoiceWord, setPlayingVoiceWord] = useState<string | null>(null);
  const [voiceErrorWord, setVoiceErrorWord] = useState<string | null>(null);
  const [playingSentenceId, setPlayingSentenceId] = useState<string | null>(null);

  // Audio refs
  const voiceAudioRef = useRef<HTMLAudioElement | null>(null);
  const clipAudioRef = useRef<HTMLAudioElement | null>(null);

  // Active word in current session
  const activeSessionItem = useMemo(() => {
    if (sessionQueue.length === 0 || currentSessionIndex >= sessionQueue.length) return null;
    return sessionQueue[currentSessionIndex];
  }, [sessionQueue, currentSessionIndex]);

  // ---------------------------------------------------------------------------
  // 1. Initial Load: Settings, Daily Summary, & Session Queue
  // ---------------------------------------------------------------------------
  const loadSummaryAndSettings = useCallback(async () => {
    try {
      const [sumRes, setRes] = await Promise.all([
        api.getVocabSummary().catch(() => null),
        api.getVocabSettings().catch(() => null),
      ]);
      if (sumRes) setSummary(sumRes);
      if (setRes) {
        setSettings(setRes);
        setCustomQuotaInput(String(setRes.daily_new_quota));
      }
    } catch (e) {
      console.error("Failed to load vocab settings/summary", e);
    }
  }, []);

  const loadSessionQueue = useCallback(async () => {
    setIsLoadingSession(true);
    try {
      const sessionData = await api.getVocabStudySession();
      setSessionQueue(sessionData.items);
      setCurrentSessionIndex(0);
      setCardStage("front");
    } catch (e) {
      console.error("Failed to load study session", e);
    } finally {
      setIsLoadingSession(false);
    }
  }, []);

  useEffect(() => {
    loadSummaryAndSettings();
    loadSessionQueue();
  }, [loadSummaryAndSettings, loadSessionQueue, user]);

  // ---------------------------------------------------------------------------
  // 2. Pronunciation Audio Playback
  // ---------------------------------------------------------------------------
  const playWordAudio = useCallback((word: string, voiceType: 1 | 2 = 2) => {
    if (voiceAudioRef.current) {
      voiceAudioRef.current.pause();
      voiceAudioRef.current = null;
    }

    setPlayingVoiceWord(word);
    setVoiceErrorWord(null);

    const primaryUrl = api.getVoiceUrl(word, voiceType);
    const audio = new Audio(primaryUrl);
    voiceAudioRef.current = audio;

    const fallbackSpeech = () => {
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(word);
        utterance.lang = voiceType === 1 ? "en-GB" : "en-US";
        utterance.rate = 0.9;
        utterance.onend = () => setPlayingVoiceWord(null);
        utterance.onerror = () => {
          setPlayingVoiceWord(null);
          setVoiceErrorWord("暂时没声音，点重试。");
        };
        window.speechSynthesis.speak(utterance);
      } else {
        setPlayingVoiceWord(null);
        setVoiceErrorWord("暂时没声音，点重试。");
      }
    };

    audio.onended = () => setPlayingVoiceWord(null);
    audio.onerror = () => {
      const directUrl = `https://dict.youdao.com/dictvoice?audio=${encodeURIComponent(word)}&type=${voiceType}`;
      const directAudio = new Audio(directUrl);
      voiceAudioRef.current = directAudio;
      directAudio.onended = () => setPlayingVoiceWord(null);
      directAudio.onerror = () => fallbackSpeech();
      directAudio.play().catch(() => fallbackSpeech());
    };

    audio.play().catch(() => fallbackSpeech());
  }, []);

  // ---------------------------------------------------------------------------
  // 3. Real Exam Sentence Clip Playback
  // ---------------------------------------------------------------------------
  const playSentenceAudio = useCallback((example: FreqSentenceExample) => {
    if (playingSentenceId === example.sentence_id) {
      clipAudioRef.current?.pause();
      setPlayingSentenceId(null);
      return;
    }

    if (clipAudioRef.current) {
      clipAudioRef.current.pause();
    }

    const audioUrl = api.getAudioUrl(example.audio_file);
    const audio = new Audio(audioUrl);
    clipAudioRef.current = audio;

    audio.currentTime = example.start_time;
    audio.play().then(() => {
      setPlayingSentenceId(example.sentence_id);
    }).catch(() => {
      setPlayingSentenceId(null);
    });

    audio.ontimeupdate = () => {
      if (audio.currentTime >= example.end_time) {
        audio.pause();
        setPlayingSentenceId(null);
      }
    };

    audio.onended = () => setPlayingSentenceId(null);
  }, [playingSentenceId]);

  // Auto-play audio when entering new card
  useEffect(() => {
    if (activeTab === "session" && activeSessionItem && cardStage === "front") {
      if (settings.autoplay_audio) {
        playWordAudio(activeSessionItem.word);
      }
    }
  }, [activeTab, activeSessionItem, cardStage, settings.autoplay_audio, playWordAudio]);

  // ---------------------------------------------------------------------------
  // 4. Session Action Flow: 不会 (Again), 模糊 (Hard), 会了 (Quiz)
  // ---------------------------------------------------------------------------
  const handleAdvanceNextCard = useCallback(() => {
    setCardStage("front");
    setSelectedQuizOption(null);
    setIsQuizCorrect(null);
    setVoiceErrorWord(null);

    if (currentSessionIndex + 1 < sessionQueue.length) {
      setCurrentSessionIndex((i) => i + 1);
    } else {
      // Finished batch, reload summary and session
      loadSummaryAndSettings();
      loadSessionQueue();
    }
  }, [currentSessionIndex, sessionQueue.length, loadSummaryAndSettings, loadSessionQueue]);

  const prepareQuiz = useCallback((item: StudySessionItem) => {
    setCardStage("quiz");
    setQuizListenCount(1);
    setSelectedQuizOption(null);
    setIsQuizCorrect(null);

    // Shuffle target word with 3 distractors
    const distractors = item.distractors && item.distractors.length >= 3
      ? item.distractors.slice(0, 3)
      : ["other", "point", "state"]; // emergency fallback

    const opts = [item.word, ...distractors].sort(() => Math.random() - 0.5);
    setShuffledQuizOptions(opts);

    // Auto-play question audio
    playWordAudio(item.word);
    api.logVocabEvent("quiz_start", item.word);
  }, [playWordAudio]);

  const handleRatingChoice = useCallback(async (rating: 1 | 2 | 3) => {
    if (!activeSessionItem) return;
    const word = activeSessionItem.word;
    setLastRatingChoice(rating);

    if (rating === 1) {
      // 不会 -> Reveal definition + 1 real exam example -> Schedule Again
      setCardStage("reveal_feedback");
      api.logVocabEvent("rate_again", word);
      await api.rateVocabCard(word, 1, undefined, 1);
    } else if (rating === 2) {
      // 模糊 -> Reveal definition + 1 real exam example -> Schedule Hard
      setCardStage("reveal_feedback");
      api.logVocabEvent("rate_hard", word);
      await api.rateVocabCard(word, 2, undefined, 1);
    } else {
      // 会了 -> Enter Listening Discrimination Quiz (四选一)
      api.logVocabEvent("rate_good_intent", word);
      prepareQuiz(activeSessionItem);
    }
  }, [activeSessionItem, prepareQuiz]);

  const handleSelectQuizOption = useCallback(async (option: string) => {
    if (selectedQuizOption !== null || !activeSessionItem) return;

    setSelectedQuizOption(option);
    const correct = option.toLowerCase() === activeSessionItem.word.toLowerCase();
    setIsQuizCorrect(correct);
    setCardStage("quiz_result");

    if (correct) {
      api.logVocabEvent("quiz_correct", activeSessionItem.word, { listen_count: quizListenCount });
      // Schedule Good (Rating 3)
      await api.rateVocabCard(activeSessionItem.word, 3, true, quizListenCount);
      // Auto advance to next card after short feedback
      setTimeout(() => {
        handleAdvanceNextCard();
      }, 850);
    } else {
      api.logVocabEvent("quiz_wrong", activeSessionItem.word, { selected: option, listen_count: quizListenCount });
      // Schedule Again (Rating 1) because listening discrimination failed
      await api.rateVocabCard(activeSessionItem.word, 1, false, quizListenCount);
      // Replay correct audio for ear alignment
      playWordAudio(activeSessionItem.word);
    }
  }, [selectedQuizOption, activeSessionItem, quizListenCount, handleAdvanceNextCard, playWordAudio]);

  // Keyboard navigation for Session Mode
  useEffect(() => {
    if (activeTab !== "session") return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.target instanceof HTMLInputElement || e.target instanceof HTMLTextAreaElement) return;

      if (cardStage === "front") {
        if (e.key === "1" || e.key === "ArrowLeft") {
          e.preventDefault();
          handleRatingChoice(1); // 不会
        } else if (e.key === "2" || e.key === "ArrowDown") {
          e.preventDefault();
          handleRatingChoice(2); // 模糊
        } else if (e.key === "3" || e.key === "ArrowRight") {
          e.preventDefault();
          handleRatingChoice(3); // 会了
        } else if (e.key === " ") {
          e.preventDefault();
          if (activeSessionItem) playWordAudio(activeSessionItem.word);
        }
      } else if (cardStage === "reveal_feedback" || (cardStage === "quiz_result" && isQuizCorrect === false)) {
        if (e.key === "Enter" || e.key === " " || e.key === "ArrowRight") {
          e.preventDefault();
          handleAdvanceNextCard();
        }
      } else if (cardStage === "quiz" && selectedQuizOption === null) {
        if (["1", "2", "3", "4"].includes(e.key)) {
          const idx = parseInt(e.key, 10) - 1;
          if (shuffledQuizOptions[idx]) {
            e.preventDefault();
            handleSelectQuizOption(shuffledQuizOptions[idx]);
          }
        } else if (e.key === " ") {
          e.preventDefault();
          if (activeSessionItem) {
            setQuizListenCount((c) => c + 1);
            playWordAudio(activeSessionItem.word);
          }
        }
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [
    activeTab,
    cardStage,
    activeSessionItem,
    selectedQuizOption,
    shuffledQuizOptions,
    isQuizCorrect,
    playWordAudio,
    handleAdvanceNextCard,
    handleRatingChoice,
    handleSelectQuizOption,
  ]);

  // ---------------------------------------------------------------------------
  // 5. Settings Save & Quota Update
  // ---------------------------------------------------------------------------
  const handleSaveSettings = async (quotaVal: number, autoPlayVal: boolean) => {
    const quota = Math.min(100, Math.max(1, quotaVal));
    try {
      await api.saveVocabSettings(quota, autoPlayVal);
      setSettings((prev) => ({ ...prev, daily_new_quota: quota, autoplay_audio: autoPlayVal }));
      setSummary((prev) => ({ ...prev, new_quota: quota }));
      api.logVocabEvent("new_quota_set", undefined, { quota, autoPlayVal });
      setShowSettingsModal(false);
      // Reload session queue for next round
      loadSessionQueue();
    } catch (e) {
      console.error("Failed to save settings", e);
    }
  };

  // ---------------------------------------------------------------------------
  // 6. List View Loading (Phase 1 Compatibility)
  // ---------------------------------------------------------------------------
  const loadFrequencyWords = useCallback(async (tabTarget = listSubTab, pageTarget = 1, queryTarget = searchQuery) => {
    setIsLoadingList(true);
    try {
      const res: FreqVocabListResponse = await api.getFreqVocabulary(
        tabTarget,
        pageTarget,
        35,
        queryTarget.trim() || undefined
      );
      if (pageTarget === 1) {
        setFreqItems(res.items);
      } else {
        setFreqItems((prev) => [...prev, ...res.items]);
      }
      setHasMoreList(res.has_more);
      setListPage(pageTarget);
    } catch (e) {
      console.error("Failed to load frequency vocabulary list", e);
    } finally {
      setIsLoadingList(false);
    }
  }, [listSubTab, searchQuery]);

  const loadBookmarks = useCallback(async () => {
    setIsLoadingList(true);
    try {
      const items = await api.getVocabulary().catch(() => [] as VocabItem[]);
      setBookmarkedList(items);
    } catch (e) {
      console.error("Failed to load bookmarks", e);
    } finally {
      setIsLoadingList(false);
    }
  }, []);

  useEffect(() => {
    if (activeTab === "list") {
      loadFrequencyWords(listSubTab, 1, searchQuery);
    } else if (activeTab === "bookmarks") {
      loadBookmarks();
    }
  }, [activeTab, listSubTab, searchQuery, loadFrequencyWords, loadBookmarks]);

  return (
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] selection:bg-[#0071e3]/20 select-none pb-24">
      {/* ------------------------------------------------------------------- */}
      {/* Sticky Top Header Bar                                               */}
      {/* ------------------------------------------------------------------- */}
      <header className="sticky top-0 z-30 bg-[#f5f5f7]/85 dark:bg-[#000000]/85 backdrop-blur-md border-b border-black/[0.06] dark:border-white/[0.08]">
        <div className="max-w-2xl mx-auto px-4 h-14 flex items-center justify-between">
          <Link
            href="/studio"
            className="flex items-center gap-1 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors -ml-1 py-1 px-2 rounded-full active:scale-95"
          >
            <ChevronLeft className="w-4 h-4" /> 返回精听
          </Link>

          {/* Daily Quantified Numbers Bar */}
          <div className="flex items-center gap-2">
            <span className="text-xs font-mono font-medium text-[#1d1d1f] dark:text-[#f5f5f7] bg-white dark:bg-[#1c1c1e] px-2.5 py-1 rounded-full border border-black/[0.06] dark:border-white/[0.08] shadow-sm">
              {summary.summary_text}
            </span>

            <button
              onClick={() => setShowSettingsModal(true)}
              className="p-1.5 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] rounded-full hover:bg-black/5 dark:hover:bg-white/10 transition-all active:scale-90"
              title="学习量与算法设置"
            >
              <Settings className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* ------------------------------------------------------------------- */}
      {/* Main Container                                                      */}
      {/* ------------------------------------------------------------------- */}
      <main className="max-w-2xl mx-auto px-4 pt-4 sm:pt-6">
        {/* Navigation Tabs */}
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-1 bg-black/[0.04] dark:bg-white/[0.06] p-1 rounded-xl">
            <button
              onClick={() => setActiveTab("session")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === "session"
                  ? "bg-white dark:bg-[#1c1c1e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm font-semibold"
                  : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              }`}
            >
              今日定量 ({sessionQueue.length})
            </button>
            <button
              onClick={() => setActiveTab("list")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === "list"
                  ? "bg-white dark:bg-[#1c1c1e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm font-semibold"
                  : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              }`}
            >
              全部词表
            </button>
            <button
              onClick={() => setActiveTab("bookmarks")}
              className={`px-3.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
                activeTab === "bookmarks"
                  ? "bg-white dark:bg-[#1c1c1e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm font-semibold"
                  : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              }`}
            >
              精听生词
            </button>
          </div>

          <div className="text-[11px] text-[#86868b] font-mono hidden sm:block">
            FSRS-5 记忆曲线
          </div>
        </div>

        {/* ----------------------------------------------------------------- */}
        {/* TAB 1: 今日定量学习 (Session Mode with FSRS + Listening Quiz)     */}
        {/* ----------------------------------------------------------------- */}
        {activeTab === "session" && (
          <div>
            {isLoadingSession ? (
              <div className="py-24 text-center text-xs text-[#86868b] font-mono">
                正在调度今日记忆队列...
              </div>
            ) : !activeSessionItem ? (
              /* Empty State */
              <div className="py-24 text-center bg-white dark:bg-[#1c1c1e] rounded-3xl p-8 border border-black/[0.04] dark:border-white/[0.06] shadow-sm">
                <CheckCircle2 className="w-12 h-12 text-[#34c759] mx-auto mb-3 opacity-90" />
                <h3 className="text-base font-bold text-[#1d1d1f] dark:text-[#f5f5f7]">
                  今日新词已完成
                </h3>
                <p className="text-xs text-[#86868b] mt-1 max-w-xs mx-auto">
                  {summary.due_count === 0 ? "暂无到期复习。记忆曲线已更新，明天再来！" : "复习任务已清理完毕。"}
                </p>
                <div className="mt-5 flex items-center justify-center gap-2">
                  <button
                    onClick={() => handleSaveSettings(settings.daily_new_quota + 10, settings.autoplay_audio)}
                    className="px-4 py-2 rounded-full text-xs font-semibold bg-[#0071e3] text-white hover:bg-[#0077ed] transition-all active:scale-95 shadow-sm"
                  >
                    加学 10 个新词
                  </button>
                  <button
                    onClick={() => setActiveTab("list")}
                    className="px-4 py-2 rounded-full text-xs font-medium border border-black/[0.08] dark:border-white/[0.1] text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
                  >
                    查阅全部词表
                  </button>
                </div>
              </div>
            ) : (
              /* Active Study Card */
              <div className="bg-white dark:bg-[#1c1c1e] rounded-3xl border border-black/[0.04] dark:border-white/[0.06] shadow-sm p-6 sm:p-8 flex flex-col justify-between min-h-[460px] animate-in fade-in duration-200">
                {/* Top status bar inside card */}
                <div className="flex items-center justify-between text-xs text-[#86868b]">
                  <div className="flex items-center gap-2">
                    <span className="font-mono font-medium">
                      {currentSessionIndex + 1} / {sessionQueue.length}
                    </span>
                    {activeSessionItem.is_review ? (
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#ff9500]/10 text-[#ff9500] font-semibold">
                        复习到期
                      </span>
                    ) : (
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] font-semibold">
                        今日新词
                      </span>
                    )}
                  </div>

                  <span className="text-[11px] font-mono">
                    真题 {activeSessionItem.frequency}次 · {activeSessionItem.exam_count}套
                  </span>
                </div>

                {/* ----------------------------------------------------------- */}
                {/* Stage 1: Card Front (Word + Pronounce)                      */}
                {/* ----------------------------------------------------------- */}
                {cardStage === "front" && (
                  <div className="flex-1 flex flex-col items-center justify-center text-center my-6">
                    <h2 className="text-4xl sm:text-5xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                      {activeSessionItem.word}
                    </h2>

                    {activeSessionItem.phonetic && (
                      <p className="mt-2 text-sm sm:text-base font-mono text-[#86868b]">
                        /{activeSessionItem.phonetic}/
                      </p>
                    )}

                    {/* Prominent Audio Speaker Button */}
                    <div className="my-6">
                      <button
                        type="button"
                        onClick={() => playWordAudio(activeSessionItem.word)}
                        className={`w-18 h-18 sm:w-20 sm:h-20 rounded-full flex items-center justify-center transition-all shadow-md active:scale-95 ${
                          playingVoiceWord === activeSessionItem.word
                            ? "bg-[#0071e3] text-white ring-8 ring-[#0071e3]/20 animate-pulse"
                            : "bg-[#f5f5f7] dark:bg-white/5 text-[#0071e3] dark:text-[#0a84ff] hover:scale-105"
                        }`}
                        title="听发音 (空格键)"
                      >
                        <Volume2 className="w-8 h-8" />
                      </button>
                      {voiceErrorWord && (
                        <p className="text-xs text-[#ff453a] mt-2 font-medium">
                          {voiceErrorWord}
                        </p>
                      )}
                    </div>

                    <p className="text-xs text-[#86868b]">
                      听清发音后，请选择对该词的掌握感
                    </p>
                  </div>
                )}

                {/* ----------------------------------------------------------- */}
                {/* Stage 2: Reveal Feedback (When clicked 不会 or 模糊)        */}
                {/* ----------------------------------------------------------- */}
                {cardStage === "reveal_feedback" && (
                  <div className="flex-1 flex flex-col justify-center my-4 animate-in fade-in duration-150">
                    <div className="text-center mb-4">
                      <h2 className="text-3xl sm:text-4xl font-bold text-[#1d1d1f] dark:text-[#f5f5f7]">
                        {activeSessionItem.word}
                      </h2>
                      {activeSessionItem.phonetic && (
                        <p className="text-xs font-mono text-[#86868b] mt-1">
                          /{activeSessionItem.phonetic}/
                        </p>
                      )}
                    </div>

                    {/* Definition */}
                    <div className="p-4 bg-[#f5f5f7] dark:bg-black/30 rounded-2xl border border-black/[0.04] dark:border-white/[0.06] mb-3">
                      <p className="text-xs font-semibold text-[#0071e3] dark:text-[#0a84ff] font-mono mb-1">
                        {activeSessionItem.pos || "释义"}
                      </p>
                      <p className="text-base font-medium text-[#1d1d1f] dark:text-[#f5f5f7]">
                        {activeSessionItem.definition_zh || "核心真题考义"}
                      </p>
                    </div>

                    {/* Real Exam Sentence Clip */}
                    {activeSessionItem.examples && activeSessionItem.examples.length > 0 && (
                      <div className="p-3.5 bg-black/[0.02] dark:bg-white/[0.03] rounded-2xl border border-black/[0.04] dark:border-white/[0.06]">
                        <div className="flex items-start justify-between gap-2">
                          <p className="text-xs text-[#1d1d1f] dark:text-[#f5f5f7] leading-relaxed flex-1">
                            {activeSessionItem.examples[0].english}
                          </p>
                          <button
                            type="button"
                            onClick={() => playSentenceAudio(activeSessionItem.examples[0])}
                            className={`p-1.5 rounded-full shrink-0 transition-all ${
                              playingSentenceId === activeSessionItem.examples[0].sentence_id
                                ? "bg-[#0071e3] text-white animate-pulse"
                                : "bg-black/5 dark:bg-white/10 text-[#0071e3] dark:text-[#0a84ff]"
                            }`}
                            title="听真题原声切片"
                          >
                            <Play className="w-3.5 h-3.5 fill-current" />
                          </button>
                        </div>
                        <p className="text-[11px] text-[#86868b] mt-1">
                          {activeSessionItem.examples[0].chinese}
                        </p>
                        <div className="text-[10px] text-[#86868b] font-mono mt-1">
                          真题出处: {formatExamTitleZh(activeSessionItem.examples[0].exam_id)}
                        </div>
                      </div>
                    )}

                    <div className="mt-3 text-center text-[11px] text-[#86868b]">
                      {lastRatingChoice === 1 ? "已排入今日短周期重听队列" : "已根据遗忘曲线排入复习"}
                    </div>
                  </div>
                )}

                {/* ----------------------------------------------------------- */}
                {/* Stage 3: Listening Discrimination Quiz (听辨四选一)         */}
                {/* ----------------------------------------------------------- */}
                {(cardStage === "quiz" || cardStage === "quiz_result") && (
                  <div className="flex-1 flex flex-col justify-center my-4 animate-in fade-in duration-200">
                    <div className="text-center mb-5">
                      <span className="text-[11px] font-semibold tracking-wider text-[#0071e3] dark:text-[#0a84ff] uppercase">
                        听辨检验 · 选出所听单词
                      </span>

                      {/* Prominent Listening Audio Center */}
                      <div className="my-4 flex items-center justify-center gap-3">
                        <button
                          type="button"
                          onClick={() => {
                            setQuizListenCount((c) => c + 1);
                            playWordAudio(activeSessionItem.word);
                          }}
                          className={`w-16 h-16 rounded-full flex items-center justify-center transition-all shadow-md active:scale-95 ${
                            playingVoiceWord === activeSessionItem.word
                              ? "bg-[#0071e3] text-white ring-6 ring-[#0071e3]/20 animate-pulse"
                              : "bg-[#f5f5f7] dark:bg-white/5 text-[#0071e3] dark:text-[#0a84ff] hover:scale-105"
                          }`}
                          title="再听一次音频"
                        >
                          <Volume2 className="w-7 h-7" />
                        </button>
                      </div>

                      <button
                        type="button"
                        onClick={() => {
                          setQuizListenCount((c) => c + 1);
                          playWordAudio(activeSessionItem.word);
                        }}
                        className="text-[11px] text-[#86868b] hover:text-[#0071e3] dark:hover:text-[#0a84ff] transition-colors"
                      >
                        再听一次 {quizListenCount > 1 ? `(${quizListenCount}次)` : ""}
                      </button>
                    </div>

                    {/* 2x2 Word Options Grid */}
                    <div className="grid grid-cols-2 gap-3 max-w-md mx-auto w-full">
                      {shuffledQuizOptions.map((opt) => {
                        const isSelected = selectedQuizOption === opt;
                        const isTarget = opt.toLowerCase() === activeSessionItem.word.toLowerCase();

                        let btnStyle = "bg-[#f5f5f7] dark:bg-white/5 border-black/[0.06] dark:border-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7]";
                        if (cardStage === "quiz_result") {
                          if (isTarget) {
                            btnStyle = "bg-[#34c759] text-white border-[#34c759] font-bold shadow-md shadow-[#34c759]/20";
                          } else if (isSelected && !isTarget) {
                            btnStyle = "bg-[#ff3b30] text-white border-[#ff3b30] font-bold";
                          } else {
                            btnStyle = "opacity-40 border-transparent";
                          }
                        } else {
                          btnStyle += " hover:border-[#0071e3] hover:text-[#0071e3] active:scale-95";
                        }

                        return (
                          <button
                            key={opt}
                            disabled={cardStage === "quiz_result"}
                            onClick={() => handleSelectQuizOption(opt)}
                            className={`py-3.5 px-4 rounded-2xl border text-sm font-semibold transition-all flex items-center justify-center text-center ${btnStyle}`}
                          >
                            {opt}
                          </button>
                        );
                      })}
                    </div>

                    {/* Quiz Result Reveal */}
                    {cardStage === "quiz_result" && (
                      <div className="mt-4 text-center animate-in fade-in duration-150">
                        {isQuizCorrect ? (
                          <p className="text-xs font-semibold text-[#34c759] flex items-center justify-center gap-1">
                            <Check className="w-3.5 h-3.5" /> 正确！已记录掌握并安排下一复习点
                          </p>
                        ) : (
                          <div className="space-y-1">
                            <p className="text-xs font-semibold text-[#ff3b30]">
                              听辨未通过，正确单词为：{activeSessionItem.word}
                            </p>
                            <p className="text-[11px] text-[#86868b]">
                              释义：{activeSessionItem.definition_zh}
                            </p>
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                )}

                {/* ----------------------------------------------------------- */}
                {/* Bottom Dock Buttons                                         */}
                {/* ----------------------------------------------------------- */}
                <div className="pt-4 border-t border-black/[0.04] dark:border-white/[0.06]">
                  {cardStage === "front" ? (
                    /* 3 Equal-Width Buttons: 不会 | 模糊 | 会了 */
                    <div className="grid grid-cols-3 gap-2.5">
                      <button
                        type="button"
                        onClick={() => handleRatingChoice(1)}
                        className="py-3.5 rounded-2xl bg-[#f5f5f7] dark:bg-white/5 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] border border-black/[0.06] dark:border-white/[0.08] text-xs font-semibold transition-all active:scale-95"
                      >
                        不会 <span className="text-[10px] opacity-60 hidden sm:inline">(1)</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => handleRatingChoice(2)}
                        className="py-3.5 rounded-2xl bg-[#f5f5f7] dark:bg-white/5 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] border border-black/[0.06] dark:border-white/[0.08] text-xs font-semibold transition-all active:scale-95"
                      >
                        模糊 <span className="text-[10px] opacity-60 hidden sm:inline">(2)</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => handleRatingChoice(3)}
                        className="py-3.5 rounded-2xl bg-[#0071e3] text-white hover:bg-[#0077ed] text-xs font-semibold transition-all active:scale-95 shadow-sm shadow-[#0071e3]/20"
                      >
                        会了 <span className="text-[10px] opacity-80 hidden sm:inline">(3)</span>
                      </button>
                    </div>
                  ) : cardStage === "reveal_feedback" || (cardStage === "quiz_result" && isQuizCorrect === false) ? (
                    /* Advance Next Button */
                    <button
                      type="button"
                      onClick={handleAdvanceNextCard}
                      className="w-full py-3.5 rounded-2xl bg-[#0071e3] text-white hover:bg-[#0077ed] text-xs font-semibold transition-all active:scale-95 shadow-sm shadow-[#0071e3]/20 flex items-center justify-center gap-1.5"
                    >
                      <span>下一词 (空格键)</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                  ) : null}
                </div>
              </div>
            )}
          </div>
        )}

        {/* ----------------------------------------------------------------- */}
        {/* TAB 2: 全部词表清单 (List View)                                   */}
        {/* ----------------------------------------------------------------- */}
        {activeTab === "list" && (
          <div>
            {/* Sub-tabs: 待学 vs 已掌握 */}
            <div className="flex items-center justify-between gap-3 mb-4">
              <div className="flex items-center gap-1 bg-black/[0.04] dark:bg-white/[0.06] p-1 rounded-xl">
                <button
                  onClick={() => {
                    setListSubTab("unmastered");
                    setListPage(1);
                  }}
                  className={`px-3 py-1 rounded-lg text-xs font-medium ${
                    listSubTab === "unmastered"
                      ? "bg-white dark:bg-[#1c1c1e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm font-semibold"
                      : "text-[#86868b]"
                  }`}
                >
                  待学清单
                </button>
                <button
                  onClick={() => {
                    setListSubTab("mastered");
                    setListPage(1);
                  }}
                  className={`px-3 py-1 rounded-lg text-xs font-medium ${
                    listSubTab === "mastered"
                      ? "bg-white dark:bg-[#1c1c1e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm font-semibold"
                      : "text-[#86868b]"
                  }`}
                >
                  已掌握 ({summary.mastered_count})
                </button>
              </div>

              {/* Search box */}
              <div className="relative w-48">
                <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-[#86868b]" />
                <input
                  type="text"
                  placeholder="检索真题词汇"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full pl-8 pr-7 py-1.5 bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-xl text-xs text-[#1d1d1f] dark:text-[#f5f5f7] placeholder-[#86868b] focus:outline-none focus:border-[#0071e3]"
                />
              </div>
            </div>

            {/* List items */}
            {isLoadingList && freqItems.length === 0 ? (
              <div className="py-20 text-center text-xs text-[#86868b] font-mono">加载中...</div>
            ) : freqItems.length === 0 ? (
              <div className="py-16 text-center text-xs text-[#86868b]">
                {listSubTab === "mastered" ? "暂无已掌握单词" : "听一套真题，生词会自动出现在这里。"}
              </div>
            ) : (
              <div className="divide-y divide-black/[0.05] dark:divide-white/[0.06] bg-white dark:bg-[#1c1c1e] rounded-2xl border border-black/[0.04] dark:border-white/[0.06] overflow-hidden shadow-sm">
                {freqItems.map((item) => (
                  <div key={item.word} className="p-4 hover:bg-black/[0.015] dark:hover:bg-white/[0.02] transition-colors">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1">
                        <div className="flex items-center gap-2 flex-wrap">
                          <span className="text-base font-bold text-[#1d1d1f] dark:text-[#f5f5f7]">
                            {item.word}
                          </span>
                          {item.phonetic && (
                            <span className="font-mono text-xs text-[#86868b]">
                              /{item.phonetic}/
                            </span>
                          )}
                          <button
                            type="button"
                            onClick={() => playWordAudio(item.word)}
                            className="p-1 text-[#86868b] hover:text-[#0071e3]"
                            title="听发音"
                          >
                            <Volume2 className="w-3.5 h-3.5" />
                          </button>
                          <span className="text-[10px] font-mono text-[#86868b] bg-black/[0.03] dark:bg-white/[0.06] px-1.5 py-0.5 rounded-full">
                            真题 {item.frequency}次
                          </span>
                        </div>
                        <p className="text-xs text-[#1d1d1f] dark:text-[#f5f5f7] mt-1 line-clamp-1">
                          {item.pos ? `${item.pos} ` : ""}{item.definition_zh}
                        </p>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        {item.example_count > 0 && (
                          <button
                            type="button"
                            onClick={() =>
                              setExpandedExamplesWord((curr) => (curr === item.word ? null : item.word))
                            }
                            className="text-[11px] text-[#86868b] hover:text-[#0071e3] flex items-center gap-1"
                          >
                            例句 ({item.example_count})
                            {expandedExamplesWord === item.word ? (
                              <ChevronUp className="w-3 h-3" />
                            ) : (
                              <ChevronDown className="w-3 h-3" />
                            )}
                          </button>
                        )}
                      </div>
                    </div>

                    {/* Inline expanded real exam sentences */}
                    {expandedExamplesWord === item.word && (
                      <div className="mt-3 pt-3 border-t border-black/[0.04] dark:border-white/[0.06] space-y-2 animate-in fade-in duration-150">
                        {(item.examples || []).map((ex) => (
                          <div key={ex.sentence_id} className="p-2.5 bg-[#f5f5f7] dark:bg-black/30 rounded-xl text-xs space-y-1">
                            <div className="flex items-start justify-between gap-2">
                              <p className="text-[#1d1d1f] dark:text-[#f5f5f7] leading-relaxed flex-1">
                                {ex.english}
                              </p>
                              <button
                                type="button"
                                onClick={() => playSentenceAudio(ex)}
                                className="p-1 text-[#0071e3] shrink-0"
                              >
                                <Play className="w-3 h-3 fill-current" />
                              </button>
                            </div>
                            <p className="text-[#86868b] text-[11px]">{ex.chinese}</p>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                ))}

                {/* Pagination load more */}
                {hasMoreList && (
                  <div className="p-4 text-center border-t border-black/[0.04] dark:border-white/[0.06]">
                    <button
                      type="button"
                      onClick={() => loadFrequencyWords(listSubTab, listPage + 1, searchQuery)}
                      disabled={isLoadingList}
                      className="text-xs text-[#0071e3] font-medium hover:underline disabled:opacity-50"
                    >
                      {isLoadingList ? "加载中..." : "加载更多单词"}
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {/* ----------------------------------------------------------------- */}
        {/* TAB 3: 精听生词 (Bookmarks View)                                  */}
        {/* ----------------------------------------------------------------- */}
        {activeTab === "bookmarks" && (
          <div className="bg-white dark:bg-[#1c1c1e] rounded-2xl border border-black/[0.04] dark:border-white/[0.06] divide-y divide-black/[0.05] dark:divide-white/[0.06] overflow-hidden shadow-sm">
            {isLoadingList ? (
              <div className="py-20 text-center text-xs text-[#86868b] font-mono">加载中...</div>
            ) : bookmarkedList.length === 0 ? (
              <div className="py-16 text-center text-xs text-[#86868b]">
                <Bookmark className="w-8 h-8 mx-auto mb-2 opacity-30" />
                <p>听一套真题，生词会自动出现在这里。</p>
              </div>
            ) : (
              bookmarkedList.map((item) => (
                <div key={item.id} className="p-4 flex items-center justify-between gap-3">
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="text-base font-bold text-[#1d1d1f] dark:text-[#f5f5f7]">
                        {item.word}
                      </span>
                      {item.phonetic && (
                        <span className="font-mono text-xs text-[#86868b]">
                          /{item.phonetic}/
                        </span>
                      )}
                      <button
                        type="button"
                        onClick={() => playWordAudio(item.word)}
                        className="p-1 text-[#86868b] hover:text-[#0071e3]"
                      >
                        <Volume2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                    <p className="text-xs text-[#1d1d1f] dark:text-[#f5f5f7] mt-1">
                      {item.definition_zh}
                    </p>
                  </div>
                  <button
                    type="button"
                    onClick={async () => {
                      await api.deleteVocabulary(item.id);
                      setBookmarkedList((prev) => prev.filter((v) => v.id !== item.id));
                    }}
                    className="text-xs text-[#86868b] hover:text-[#ff3b30]"
                  >
                    移出
                  </button>
                </div>
              ))
            )}
          </div>
        )}
      </main>

      {/* ------------------------------------------------------------------- */}
      {/* Settings Modal (每日新词量、自动播放、FSRS只读版本)                 */}
      {/* ------------------------------------------------------------------- */}
      {showSettingsModal && (
        <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4 animate-in fade-in duration-150">
          <div className="bg-white dark:bg-[#1c1c1e] rounded-3xl max-w-sm w-full p-6 border border-black/[0.06] dark:border-white/[0.08] shadow-2xl space-y-5">
            <div className="flex items-center justify-between pb-2 border-b border-black/[0.06] dark:border-white/[0.08]">
              <h3 className="text-sm font-bold text-[#1d1d1f] dark:text-[#f5f5f7]">
                词频学习设置
              </h3>
              <button
                onClick={() => setShowSettingsModal(false)}
                className="p-1 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Daily New Words Quota */}
            <div>
              <label className="text-xs font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] block mb-2">
                每日新词量（配额）
              </label>
              <div className="grid grid-cols-5 gap-1.5 mb-2.5">
                {[5, 10, 20, 30, 50].map((num) => (
                  <button
                    key={num}
                    type="button"
                    onClick={() => setCustomQuotaInput(String(num))}
                    className={`py-2 rounded-xl text-xs font-semibold border transition-all ${
                      Number(customQuotaInput) === num
                        ? "bg-[#0071e3] text-white border-[#0071e3]"
                        : "bg-[#f5f5f7] dark:bg-white/5 border-transparent text-[#1d1d1f] dark:text-[#f5f5f7]"
                    }`}
                  >
                    {num}
                  </button>
                ))}
              </div>
              <div className="flex items-center gap-2 text-xs text-[#86868b]">
                <span>自定义 (≤100):</span>
                <input
                  type="number"
                  min="1"
                  max="100"
                  value={customQuotaInput}
                  onChange={(e) => setCustomQuotaInput(e.target.value)}
                  className="w-16 px-2 py-1 rounded-lg bg-[#f5f5f7] dark:bg-white/5 border border-black/[0.06] dark:border-white/[0.08] text-xs font-mono text-[#1d1d1f] dark:text-[#f5f5f7] text-center"
                />
              </div>
            </div>

            {/* Auto Play Audio Switch */}
            <div className="flex items-center justify-between py-2 border-t border-b border-black/[0.04] dark:border-white/[0.06]">
              <div>
                <p className="text-xs font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">进入卡片自动发音</p>
                <p className="text-[10px] text-[#86868b]">翻到新词时立刻播放标准音</p>
              </div>
              <button
                type="button"
                onClick={() => setSettings((s) => ({ ...s, autoplay_audio: !s.autoplay_audio }))}
                className={`w-11 h-6 rounded-full transition-colors relative ${
                  settings.autoplay_audio ? "bg-[#34c759]" : "bg-black/15 dark:bg-white/20"
                }`}
              >
                <div
                  className={`w-5 h-5 rounded-full bg-white transition-transform absolute top-0.5 ${
                    settings.autoplay_audio ? "right-0.5" : "left-0.5"
                  }`}
                />
              </button>
            </div>

            {/* Algorithm Info (Read Only) */}
            <div className="text-[11px] text-[#86868b] space-y-1">
              <p className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                开源间隔重复引擎
              </p>
              <p className="font-mono text-[10px]">
                {settings.algorithm_version} · 90% 目标留存率
              </p>
              <p className="text-[10px] leading-relaxed text-[#86868b]/80">
                优先保障到期复习队列出清，剩余配额自动抽取真题高频新词。
              </p>
            </div>

            {/* Save Button */}
            <button
              type="button"
              onClick={() => handleSaveSettings(Number(customQuotaInput) || 20, settings.autoplay_audio)}
              className="w-full py-3 rounded-2xl bg-[#0071e3] text-white text-xs font-semibold hover:bg-[#0077ed] transition-all active:scale-95 shadow-sm"
            >
              保存设置
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
