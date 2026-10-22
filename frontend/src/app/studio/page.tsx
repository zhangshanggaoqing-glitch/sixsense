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
} from "lucide-react";
import { api, ExamDetail, Sentence, Subpart, Question } from "@/lib/api";
import { formatExamTitleZh, formatSubpartTitleZh } from "@/lib/formatters";
import { useAudioPlayer } from "@/hooks/useAudioPlayer";
import { useKeyboardShortcuts, StudioMode } from "@/hooks/useKeyboardShortcuts";
import { SentenceCard } from "@/components/studio/SentenceCard";
import { AudioBar } from "@/components/studio/AudioBar";
import { QuestionsModal } from "@/components/studio/QuestionsModal";
import { QuickLookupModal } from "@/components/studio/QuickLookupModal";

function StudioContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const urlSubpartId = searchParams.get("subpart_id") || searchParams.get("subpartId");
  const urlExamId = searchParams.get("exam_id") || searchParams.get("examId") || searchParams.get("id") || "2016-06-set1";

  const [exam, setExam] = useState<ExamDetail | null>(null);
  const [subparts, setSubparts] = useState<Subpart[]>([]);
  const [activeSubpartId, setActiveSubpartId] = useState<string>("");
  const [sentences, setSentences] = useState<Sentence[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [displayMode, setDisplayMode] = useState<StudioMode>("blind");
  const [isQuestionsOpen, setIsQuestionsOpen] = useState(false);
  const [isLookupOpen, setIsLookupOpen] = useState(false);
  const [showShortcutTip, setShowShortcutTip] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  // Active time tracking
  const activeSecondsRef = useRef(0);
  const lastInteractionTimeRef = useRef(Date.now());

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
        const [examData, subpartsList, resume] = await Promise.all([
          api.getExamDetail(urlExamId),
          api.getSubparts(urlExamId),
          api.getResume().catch(() => null),
        ]);

        setExam(examData);
        setSubparts(subpartsList);

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

        // Map legacy resume display_mode
        if (resume?.display_mode) {
          if (resume.display_mode === "C") setDisplayMode("blind");
          else if (resume.display_mode === "D") setDisplayMode("dictation");
          else setDisplayMode("bilingual");
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

  const handleSentenceChange = useCallback(() => {
    lastInteractionTimeRef.current = Date.now();
  }, []);

  const audioUrl = exam ? api.getAudioUrl(exam.audio_file) : "";

  const player = useAudioPlayer({
    audioUrl,
    sentences,
    initialIndex: 0,
    initialRate: 1.0,
    initialLoop: "off",
    onSentenceChange: handleSentenceChange,
  });

  // Switch Subpart Handler
  const handleSelectSubpart = (newSubpartId: string) => {
    if (newSubpartId === activeSubpartId) return;
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

  // Heartbeat tracking
  useEffect(() => {
    if (!exam) return;

    const interval = setInterval(() => {
      const now = Date.now();
      const isActive = now - lastInteractionTimeRef.current < 90000;
      if (player.isPlaying && isActive && document.visibilityState === "visible") {
        activeSecondsRef.current += 5;
        if (activeSecondsRef.current >= 30) {
          api.sendHeartbeat(exam.id, activeSecondsRef.current);
          activeSecondsRef.current = 0;
        }
      }
    }, 5000);

    return () => clearInterval(interval);
  }, [player.isPlaying, exam]);

  // Save resume state
  useEffect(() => {
    if (!exam || sentences.length === 0) return;
    const timer = setTimeout(() => {
      api.saveResume({
        exam_id: exam.id,
        subpart_id: activeSubpartId,
        sentence_index: player.currentIndex,
        playback_rate: player.playbackRate,
        display_mode: displayMode === "blind" ? "C" : displayMode === "dictation" ? "D" : "A",
        loop_mode: player.loopMode,
        volume: player.volume,
      });
    }, 2000);
    return () => clearTimeout(timer);
  }, [player.currentIndex, player.playbackRate, player.loopMode, player.volume, displayMode, exam, sentences, activeSubpartId]);

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

  return (
    <div className="min-h-screen flex flex-col justify-between bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] select-none">
      {/* Top Header: 专注设计，只显示 真题名称 · 当前分节 · 进度 */}
      <header className="w-full max-w-5xl mx-auto px-4 sm:px-6 py-3.5 flex items-center justify-between gap-2 sm:gap-4">
        {/* Left: 首页导航 + 分节下拉菜单 */}
        <div className="flex items-center gap-2 sm:gap-3 shrink-0">
          <Link
            href="/"
            className="flex items-center gap-1 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
          >
            <ChevronLeft className="w-4 h-4" />
            <span className="hidden sm:inline">首页</span>
          </Link>
          <span className="text-black/10 dark:text-white/10">·</span>

          {/* Subpart Switcher Dropdown */}
          <div className="relative">
            <select
              value={activeSubpartId}
              onChange={(e) => handleSelectSubpart(e.target.value)}
              className="appearance-none bg-black/[0.04] dark:bg-white/[0.08] hover:bg-black/[0.07] dark:hover:bg-white/[0.12] text-xs font-medium text-[#1d1d1f] dark:text-[#f5f5f7] pl-3 pr-7 py-1.5 rounded-full cursor-pointer focus:outline-none transition-colors border-none"
            >
              {subparts.map((sp) => (
                <option key={sp.id} value={sp.id} className="dark:bg-[#1c1c1e] text-[#1d1d1f] dark:text-[#f5f5f7]">
                  {examTitleZh} · {formatSubpartTitleZh(sp.title, sp.question_range)}
                </option>
              ))}
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-[#86868b] absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>

        {/* Center: Apple Segmented Control: 盲听 ｜ 双语 ｜ 听写 */}
        <div className="flex items-center bg-black/[0.05] dark:bg-white/[0.08] p-0.5 rounded-full text-xs font-medium">
          <button
            onClick={() => setDisplayMode("blind")}
            className={`px-3 sm:px-4 py-1.5 rounded-full transition-all ${
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
            className={`px-3 sm:px-4 py-1.5 rounded-full transition-all ${
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
            className={`px-3 sm:px-4 py-1.5 rounded-full transition-all ${
              displayMode === "dictation"
                ? "bg-white dark:bg-[#2c2c2e] text-[#0071e3] dark:text-[#0a84ff] font-semibold shadow-xs"
                : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
            }`}
            title="单句听写实战训练 (快捷键: 3)"
          >
            听写
          </button>
        </div>

        {/* Right Tools: 考题, 查词, 生词本 */}
        <div className="flex items-center gap-1 sm:gap-2 shrink-0">
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
        </div>
      </header>

      {/* Main Focus Area (一屏一个主角) */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 relative">
        {currentSentence ? (
          <SentenceCard
            sentence={currentSentence}
            displayMode={displayMode}
            isPlaying={player.isPlaying}
            examId={exam.id}
            onNext={player.nextSentence}
            onReplay={player.replay}
            onTogglePlay={player.togglePlay}
          />
        ) : (
          <div className="text-sm text-[#86868b]">暂无听力句子数据</div>
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

      {/* Bottom Floating Frosted Glass Audio Bar */}
      <footer className="w-full pb-7 pt-2 px-4 z-30">
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
        />
      </footer>

      {/* First-time Entry Shortcut Toast (Corner Hint) */}
      {showShortcutTip && (
        <div className="fixed bottom-24 right-6 z-40 flex items-center gap-2 px-3.5 py-2 bg-white/90 dark:bg-[#2c2c2e]/90 backdrop-blur-md border border-black/[0.08] dark:border-white/[0.1] rounded-full shadow-lg text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] animate-in fade-in slide-in-from-bottom-2 duration-200">
          <span>快捷键：空格 播放 · ←/→ 选句 · R 循环 · 1/2/3 切模式</span>
          <button
            onClick={dismissShortcutTip}
            className="p-0.5 rounded-full hover:bg-black/5 dark:hover:bg-white/10 text-[#86868b] hover:text-[#1d1d1f] transition-colors"
          >
            <X className="w-3 h-3" />
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
