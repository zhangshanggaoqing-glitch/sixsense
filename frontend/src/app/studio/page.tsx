"use client";

import React, { useState, useEffect, useRef, useCallback, Suspense } from "react";
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import {
  ChevronLeft,
  ChevronDown,
  Keyboard,
  BookOpen,
  Headphones,
  FileText,
  PenTool,
  HelpCircle,
  ArrowRight,
  CheckCircle2,
} from "lucide-react";
import { api, ExamDetail, Sentence, Subpart, Question } from "@/lib/api";
import { useAudioPlayer } from "@/hooks/useAudioPlayer";
import { useKeyboardShortcuts } from "@/hooks/useKeyboardShortcuts";
import { SentenceCard } from "@/components/studio/SentenceCard";
import { AudioBar } from "@/components/studio/AudioBar";
import { KeyboardHelpModal } from "@/components/studio/KeyboardHelpModal";
import { QuestionsModal } from "@/components/studio/QuestionsModal";

function StudioContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const urlSubpartId = searchParams.get("subpart_id") || searchParams.get("subpartId");
  const urlExamId = searchParams.get("exam_id") || searchParams.get("examId") || searchParams.get("id") || "2020-07-set1";

  const [exam, setExam] = useState<ExamDetail | null>(null);
  const [subparts, setSubparts] = useState<Subpart[]>([]);
  const [activeSubpartId, setActiveSubpartId] = useState<string>("");
  const [sentences, setSentences] = useState<Sentence[]>([]);
  const [questions, setQuestions] = useState<Question[]>([]);
  const [displayMode, setDisplayMode] = useState<"A" | "B" | "C" | "D">("C");
  const [isHelpOpen, setIsHelpOpen] = useState(false);
  const [isQuestionsOpen, setIsQuestionsOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Active time tracking
  const activeSecondsRef = useRef(0);
  const lastInteractionTimeRef = useRef(Date.now());

  // 1. Initial Load: Exam detail & Subparts
  useEffect(() => {
    async function init() {
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
        if (resume?.display_mode) setDisplayMode(resume.display_mode);
      } catch (err) {
        console.error("Failed to initialize studio", err);
      }
    }
    init();
  }, [urlExamId, urlSubpartId]);

  // 2. Load Sentences & Questions when activeSubpartId changes
  useEffect(() => {
    if (!activeSubpartId || !exam) return;

    async function loadSubpartContent() {
      setIsLoading(true);
      try {
        const [subSentences, subQuestions] = await Promise.all([
          api.getSentences(exam!.id, activeSubpartId),
          api.getQuestions(exam!.id, activeSubpartId).catch(() => []),
        ]);
        setSentences(subSentences);
        setQuestions(subQuestions);
      } catch (err) {
        console.error("Failed to load subpart content", err);
      } finally {
        setIsLoading(false);
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

  // Activity tracker
  useEffect(() => {
    const markActive = () => {
      lastInteractionTimeRef.current = Date.now();
    };
    window.addEventListener("keydown", markActive);
    window.addEventListener("mousedown", markActive);
    return () => {
      window.removeEventListener("keydown", markActive);
      window.removeEventListener("mousedown", markActive);
    };
  }, []);

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
        display_mode: displayMode,
        loop_mode: player.loopMode,
        volume: player.volume,
      });
    }, 2000);
    return () => clearTimeout(timer);
  }, [player.currentIndex, player.playbackRate, player.loopMode, player.volume, displayMode, exam, sentences, activeSubpartId]);

  // Keyboard Shortcuts
  useKeyboardShortcuts({
    onTogglePlay: player.togglePlay,
    onReplay: player.replay,
    onNext: player.nextSentence,
    onPrev: player.prevSentence,
    onToggleLoop: player.cycleLoopMode,
    onToggleEnglish: () => {
      setDisplayMode((prev) => (prev === "C" ? "B" : prev === "B" ? "C" : prev === "A" ? "C" : "B"));
    },
    onToggleTranslation: () => {
      setDisplayMode((prev) => (prev === "B" ? "A" : prev === "A" ? "B" : "A"));
    },
    onToggleDictation: () => {
      setDisplayMode((prev) => (prev === "D" ? "C" : "D"));
    },
    onSpeedDown: () => player.adjustSpeed(-0.1),
    onSpeedUp: () => player.adjustSpeed(0.1),
    onVolumeUp: () => player.adjustVolume(0.1),
    onVolumeDown: () => player.adjustVolume(-0.1),
    onToggleHelp: () => setIsHelpOpen((prev) => !prev),
    isDictating: displayMode === "D",
  });

  const currentSubpart = subparts.find((sp) => sp.id === activeSubpartId) || subparts[0];
  const isLastSentence = player.currentIndex === sentences.length - 1 && sentences.length > 0;
  const currentSubpartIndex = subparts.findIndex((sp) => sp.id === activeSubpartId);
  const nextSubpart = currentSubpartIndex >= 0 && currentSubpartIndex + 1 < subparts.length ? subparts[currentSubpartIndex + 1] : null;

  if (isLoading || !exam || sentences.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#fbfbfd] dark:bg-[#0d0f14]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
          <span className="text-sm font-medium text-gray-400 font-mono">Loading Topic Content...</span>
        </div>
      </div>
    );
  }

  const currentSentence = player.currentSentence || sentences[0];

  return (
    <div className="min-h-screen flex flex-col justify-between bg-[#fbfbfd] dark:bg-[#0d0f14] text-gray-900 dark:text-gray-100 select-none">
      {/* Top Header */}
      <header className="w-full max-w-5xl mx-auto px-6 py-4 flex items-center justify-between gap-4">
        {/* Left: Back & Topic Selector */}
        <div className="flex items-center gap-3">
          <Link
            href="/"
            className="flex items-center gap-1 text-xs font-medium text-gray-400 hover:text-gray-900 dark:hover:text-gray-200 transition-colors"
          >
            <ChevronLeft className="w-4 h-4" /> Home
          </Link>
          <span className="text-gray-300 dark:text-gray-700">/</span>

          {/* Subpart Switcher Dropdown */}
          <div className="relative">
            <select
              value={activeSubpartId}
              onChange={(e) => handleSelectSubpart(e.target.value)}
              className="appearance-none bg-gray-100 dark:bg-[#1a1e2b] border border-gray-200 dark:border-gray-800 text-xs font-medium text-gray-800 dark:text-gray-200 pl-3 pr-7 py-1.5 rounded-xl cursor-pointer hover:border-gray-300 dark:hover:border-gray-700 focus:outline-none"
            >
              {subparts.map((sp) => (
                <option key={sp.id} value={sp.id}>
                  {sp.title} ({sp.question_range})
                </option>
              ))}
            </select>
            <ChevronDown className="w-3.5 h-3.5 text-gray-400 absolute right-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
          </div>
        </div>

        {/* Center: Mode Switcher */}
        <div className="flex items-center bg-gray-200/60 dark:bg-[#1b1f2b] p-1 rounded-xl text-xs font-medium border border-gray-200/60 dark:border-gray-800">
          <button
            onClick={() => setDisplayMode("C")}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition-all ${
              displayMode === "C"
                ? "bg-white dark:bg-[#252a3a] text-blue-600 dark:text-blue-400 font-semibold shadow-2xs"
                : "text-gray-500 hover:text-gray-900 dark:hover:text-gray-200"
            }`}
            title="Blind Mode (C) - Audio Only"
          >
            <Headphones className="w-3.5 h-3.5" /> Blind
          </button>

          <button
            onClick={() => setDisplayMode("B")}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition-all ${
              displayMode === "B"
                ? "bg-white dark:bg-[#252a3a] text-blue-600 dark:text-blue-400 font-semibold shadow-2xs"
                : "text-gray-500 hover:text-gray-900 dark:hover:text-gray-200"
            }`}
            title="English Mode (B) - Transcript Only"
          >
            <FileText className="w-3.5 h-3.5" /> English (A)
          </button>

          <button
            onClick={() => setDisplayMode("A")}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition-all ${
              displayMode === "A"
                ? "bg-white dark:bg-[#252a3a] text-blue-600 dark:text-blue-400 font-semibold shadow-2xs"
                : "text-gray-500 hover:text-gray-900 dark:hover:text-gray-200"
            }`}
            title="Bilingual Mode (A) - English + Translation"
          >
            <span>Bilingual (T)</span>
          </button>

          <button
            onClick={() => setDisplayMode("D")}
            className={`flex items-center gap-1 px-3 py-1.5 rounded-lg transition-all ${
              displayMode === "D"
                ? "bg-white dark:bg-[#252a3a] text-blue-600 dark:text-blue-400 font-semibold shadow-2xs"
                : "text-gray-500 hover:text-gray-900 dark:hover:text-gray-200"
            }`}
            title="Dictation Mode (D)"
          >
            <PenTool className="w-3.5 h-3.5" /> Dictation (D)
          </button>
        </div>

        {/* Right Tools: Questions Drawer, Vocab & Keyboard */}
        <div className="flex items-center gap-2.5">
          {questions.length > 0 && (
            <button
              onClick={() => setIsQuestionsOpen(true)}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-xl text-xs font-medium bg-blue-50 text-blue-600 dark:bg-blue-950/60 dark:text-blue-400 border border-blue-100 dark:border-blue-900/60 hover:bg-blue-100 dark:hover:bg-blue-900/80 transition-all"
              title="View CET-6 Questions & Options"
            >
              <HelpCircle className="w-3.5 h-3.5" />
              <span>考题 ({currentSubpart?.question_range || "Q"})</span>
            </button>
          )}

          <Link
            href="/vocabulary"
            className="flex items-center gap-1 text-xs text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors p-1.5"
            title="Vocabulary"
          >
            <BookOpen className="w-4 h-4" />
          </Link>

          <button
            onClick={() => setIsHelpOpen(true)}
            className="p-1.5 text-gray-400 hover:text-gray-800 dark:hover:text-gray-200 transition-colors"
            title="Keyboard Shortcuts (?)"
          >
            <Keyboard className="w-4 h-4" />
          </button>
        </div>
      </header>

      {/* Main Focus Area (One Screen, One Job) */}
      <main className="flex-1 flex flex-col items-center justify-center px-4 relative">
        <SentenceCard
          sentence={currentSentence}
          displayMode={displayMode}
          isPlaying={player.isPlaying}
          examId={exam.id}
          onNext={player.nextSentence}
          onReplay={player.replay}
          onToggleTranslation={() => setDisplayMode("A")}
        />

        {/* End of Subpart Celebration / Transition Notification */}
        {isLastSentence && (
          <div className="mt-6 flex items-center gap-3 animate-in fade-in duration-300">
            <span className="text-xs text-gray-400 flex items-center gap-1 font-mono">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500" />
              本篇精听完毕 ({sentences.length} 句)
            </span>
            {nextSubpart && (
              <button
                onClick={handleNextSubpart}
                className="flex items-center gap-1 text-xs font-semibold px-3 py-1.5 rounded-xl bg-gray-900 text-white dark:bg-white dark:text-gray-900 hover:opacity-90 shadow-2xs transition-all"
              >
                下一题：{nextSubpart.topic_zh} ({nextSubpart.question_range}) <ArrowRight className="w-3 h-3" />
              </button>
            )}
          </div>
        )}
      </main>

      {/* Bottom Audio Transport Bar */}
      <footer className="w-full pb-8 pt-4 px-4">
        <AudioBar
          currentIndex={player.currentIndex}
          totalSentences={sentences.length}
          isPlaying={player.isPlaying}
          loopMode={player.loopMode}
          playbackRate={player.playbackRate}
          volume={player.volume}
          onTogglePlay={player.togglePlay}
          onReplay={player.replay}
          onNext={player.nextSentence}
          onPrev={player.prevSentence}
          onCycleLoop={player.cycleLoopMode}
          onSetSpeed={player.setPlaybackRate}
          onSetVolume={player.adjustVolume}
        />
      </footer>

      {/* Keyboard Shortcuts Modal */}
      <KeyboardHelpModal isOpen={isHelpOpen} onClose={() => setIsHelpOpen(false)} />

      {/* Official Questions & Options Modal */}
      <QuestionsModal
        isOpen={isQuestionsOpen}
        onClose={() => setIsQuestionsOpen(false)}
        subpartTitle={currentSubpart?.title || ""}
        questionRange={currentSubpart?.question_range || ""}
        questions={questions}
      />
    </div>
  );
}

export default function StudioPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-[#fbfbfd] dark:bg-[#0d0f14]">
          <div className="flex flex-col items-center gap-3">
            <div className="w-6 h-6 border-2 border-blue-600 border-t-transparent rounded-full animate-spin" />
            <span className="text-sm font-medium text-gray-400 font-mono">Loading SixSense Studio...</span>
          </div>
        </div>
      }
    >
      <StudioContent />
    </Suspense>
  );
}
