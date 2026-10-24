"use client";

import React, { useState, useEffect, useRef } from "react";
import { Plus, Check, Volume2, Loader2, Sparkles } from "lucide-react";
import { api, Sentence, WordLookupResult } from "@/lib/api";

interface WordPopoverProps {
  word: string;
  currentSentence: Sentence;
  examId: string;
  onClose: () => void;
  position: {
    top: number;
    left: number;
    wordTop?: number;
    wordHeight?: number;
  };
}

// In-memory frontend cache for instantaneous re-lookups
const localLookupCache = new Map<string, WordLookupResult>();

export function WordPopover({ word, currentSentence, examId, onClose, position }: WordPopoverProps) {
  const cleanWord = word.replace(/[^\w'-]+/g, "").toLowerCase();
  const [data, setData] = useState<WordLookupResult | null>(localLookupCache.get(cleanWord) || null);
  const [isLoading, setIsLoading] = useState<boolean>(!localLookupCache.has(cleanWord));
  const [isAdded, setIsAdded] = useState(false);
  const [playingVoice, setPlayingVoice] = useState<"uk" | "us" | null>(null);
  const currentAudioRef = useRef<HTMLAudioElement | null>(null);
  const popoverRef = useRef<HTMLDivElement | null>(null);
  const [coords, setCoords] = useState<{ top: number; left: number }>({
    top: position.top + 8,
    left: Math.max(16, position.left - 120),
  });

  // Click outside listener for immediate dismiss
  useEffect(() => {
    const handleOutsideClick = (e: MouseEvent | TouchEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(e.target as Node)) {
        onClose();
      }
    };
    document.addEventListener("mousedown", handleOutsideClick);
    document.addEventListener("touchstart", handleOutsideClick);
    return () => {
      document.removeEventListener("mousedown", handleOutsideClick);
      document.removeEventListener("touchstart", handleOutsideClick);
    };
  }, [onClose]);

  // Viewport boundary guard - ensures popover never overflows the bottom or edges of the screen
  useEffect(() => {
    const updatePosition = () => {
      if (typeof window === "undefined") return;
      const el = popoverRef.current;
      const height = el ? el.offsetHeight : 360;
      const width = el ? el.offsetWidth : 350;
      const margin = 16;
      const winH = window.innerHeight;
      const winW = window.innerWidth;

      let top = position.top + 8;
      const wordTop = position.wordTop ?? (position.top - (position.wordHeight ?? 24));

      // Check if popover exceeds screen bottom boundary
      if (top + height > winH - margin) {
        // If there's enough room above the word, position above it
        if (wordTop - height - 8 >= margin) {
          top = wordTop - height - 8;
        } else {
          // Otherwise clamp so bottom stays within viewport
          top = Math.max(margin, winH - height - margin);
        }
      }

      // Check horizontal boundaries
      let left = position.left - 120;
      if (left + width > winW - margin) {
        left = winW - width - margin;
      }
      if (left < margin) {
        left = margin;
      }

      setCoords({ top, left });
    };

    updatePosition();
    window.addEventListener("resize", updatePosition);
    return () => window.removeEventListener("resize", updatePosition);
  }, [position, data, isLoading]);

  // Fetch word definition and UK/US audio
  useEffect(() => {
    if (!cleanWord) return;

    if (localLookupCache.has(cleanWord)) {
      setData(localLookupCache.get(cleanWord)!);
      setIsLoading(false);
      return;
    }

    let isMounted = true;
    setIsLoading(true);

    api.lookupWord(cleanWord)
      .then((res) => {
        if (!isMounted) return;
        localLookupCache.set(cleanWord, res);
        setData(res);
      })
      .catch((err) => {
        console.error("Lookup error:", err);
      })
      .finally(() => {
        if (isMounted) setIsLoading(false);
      });

    return () => {
      isMounted = false;
      if (currentAudioRef.current) {
        currentAudioRef.current.pause();
        currentAudioRef.current = null;
      }
    };
  }, [cleanWord]);

  // Handle Pronunciation playback (UK or US)
  const playVoice = (type: "uk" | "us") => {
    if (!data) return;

    if (currentAudioRef.current) {
      currentAudioRef.current.pause();
      currentAudioRef.current = null;
    }

    setPlayingVoice(type);

    // Audio URL priorities: Proxy -> Direct -> Web Speech fallback
    const primaryUrl = type === "uk" ? data.audio_uk : data.audio_us;
    const directUrl = type === "uk" ? data.audio_uk_direct : data.audio_us_direct;

    const audio = new Audio(primaryUrl);
    currentAudioRef.current = audio;

    const fallbackToSpeechSynthesis = () => {
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(cleanWord);
        utterance.lang = type === "uk" ? "en-GB" : "en-US";
        utterance.rate = 0.9;
        utterance.onend = () => setPlayingVoice(null);
        utterance.onerror = () => setPlayingVoice(null);
        window.speechSynthesis.speak(utterance);
      } else {
        setPlayingVoice(null);
      }
    };

    audio.onended = () => {
      setPlayingVoice(null);
    };

    audio.onerror = () => {
      if (directUrl) {
        const directAudio = new Audio(directUrl);
        currentAudioRef.current = directAudio;
        directAudio.onended = () => setPlayingVoice(null);
        directAudio.onerror = () => fallbackToSpeechSynthesis();
        directAudio.play().catch(() => fallbackToSpeechSynthesis());
      } else {
        fallbackToSpeechSynthesis();
      }
    };

    audio.play().catch(() => {
      fallbackToSpeechSynthesis();
    });
  };

  const handleAdd = async () => {
    if (!data) return;
    try {
      const primaryDef = data.definitions.length > 0
        ? `${data.definitions[0].pos ? data.definitions[0].pos + ' ' : ''}${data.definitions[0].meaning}`
        : "六级核心语境词";
      const primaryPos = data.definitions[0]?.pos || "";

      await api.addVocabulary({
        word: cleanWord,
        lemma: data.lemma || cleanWord,
        phonetic: data.phonetic_us ? `/${data.phonetic_us}/` : (data.phonetic_uk ? `/${data.phonetic_uk}/` : `/${cleanWord}/`),
        phonetic_uk: data.phonetic_uk,
        phonetic_us: data.phonetic_us,
        audio_uk: data.audio_uk,
        audio_us: data.audio_us,
        part_of_speech: primaryPos,
        definition_zh: primaryDef,
        cet_level: "CET-6",
        source_sentence_id: currentSentence.id,
        source_sentence_en: currentSentence.english,
        source_sentence_zh: currentSentence.chinese,
        exam_id: examId,
        audio_clip_start: currentSentence.start_time,
        audio_clip_end: currentSentence.end_time,
      });
      setIsAdded(true);
      setTimeout(() => onClose(), 1200);
    } catch (e) {
      console.error(e);
    }
  };

    return (
    <>
      {/* Backdrop: translucent dim on mobile, transparent on desktop */}
      <div
        className="fixed inset-0 z-40 bg-black/30 sm:bg-transparent backdrop-blur-[2px] sm:backdrop-blur-none cursor-default transition-opacity"
        onClick={(e) => {
          e.stopPropagation();
          onClose();
        }}
        onContextMenu={(e) => {
          e.stopPropagation();
          onClose();
        }}
      />

      <div
        ref={popoverRef}
        className="fixed z-50 bg-white/95 dark:bg-[#1c1c1e]/95 border-t sm:border border-black/[0.08] dark:border-white/[0.1] shadow-2xl overflow-y-auto backdrop-blur-2xl animate-in duration-200 select-text
        inset-x-0 bottom-0 rounded-t-[28px] max-h-[82vh] p-5 pb-[max(1.75rem,calc(env(safe-area-inset-bottom)+1rem))] slide-in-from-bottom
        sm:inset-auto sm:rounded-2xl sm:w-[360px] sm:max-h-[min(520px,calc(100vh-28px))] sm:p-5 sm:fade-in sm:zoom-in-95"
        style={typeof window !== "undefined" && window.innerWidth >= 640 ? { top: `${coords.top}px`, left: `${coords.left}px` } : undefined}
        onClick={(e) => e.stopPropagation()}
      >
        {/* iOS Drag Indicator Capsule (Mobile only) */}
        <div className="w-10 h-1 bg-black/20 dark:bg-white/25 rounded-full mx-auto mb-3 sm:hidden" />

        {/* Header: Word & Tags & Mobile Close */}
        <div className="flex items-start justify-between gap-2 border-b border-black/[0.06] dark:border-white/[0.08] pb-3">
          <div>
            <div className="flex items-baseline gap-2">
              <h4 className="text-xl sm:text-2xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                {cleanWord}
              </h4>
              {data?.lemma && data.lemma !== cleanWord && (
                <span className="text-xs text-[#86868b] font-mono">
                  (原形: {data.lemma})
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-1.5 flex-wrap justify-end">
            <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] rounded-full">
              CET-6
            </span>
            {data?.tags?.slice(0, 2).map((t, idx) => (
              t !== "CET6" && t !== "CET-6" ? (
                <span key={idx} className="text-[10px] font-medium px-1.5 py-0.5 bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b] rounded-md">
                  {t}
                </span>
              ) : null
            ))}
            <button
              onClick={onClose}
              className="sm:hidden -mr-1 p-1 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
            >
              ✕
            </button>
          </div>
        </div>

        {isLoading ? (
          <div className="py-10 flex flex-col items-center justify-center gap-2 text-[#86868b]">
            <Loader2 className="w-6 h-6 animate-spin text-[#0071e3]" />
            <span className="text-xs font-mono">正在检索英美发音与释义...</span>
          </div>
        ) : (
          <div className="mt-4 space-y-3.5">
            {/* Pronunciations: UK & US */}
            <div className="grid grid-cols-2 gap-2.5">
              {/* UK British Accent */}
              <button
                type="button"
                onClick={() => playVoice("uk")}
                className={`flex items-center justify-between p-2.5 sm:p-2 rounded-2xl border transition-all text-left active:scale-[0.98] ${
                  playingVoice === "uk"
                    ? "bg-[#0071e3]/10 border-[#0071e3]/30 text-[#0071e3] dark:text-[#0a84ff] ring-2 ring-[#0071e3]/20"
                    : "bg-black/[0.02] dark:bg-white/[0.04] border-black/[0.06] dark:border-white/[0.08] hover:border-[#0071e3]/30"
                }`}
                title="播放纯正英音 (UK Pronunciation)"
              >
                <div className="flex flex-col">
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-[#0071e3] dark:text-[#0a84ff]">
                    🇬🇧 英音
                  </span>
                  <span className="text-xs font-mono text-[#1d1d1f] dark:text-[#f5f5f7] mt-0.5">
                    {data?.phonetic_uk ? `/${data.phonetic_uk}/` : `/${cleanWord}/`}
                  </span>
                </div>
                <div className={`p-1.5 rounded-xl ${
                  playingVoice === "uk"
                    ? "bg-[#0071e3] text-white animate-pulse"
                    : "text-[#86868b] hover:text-[#0071e3]"
                }`}>
                  <Volume2 className="w-4 h-4" />
                </div>
              </button>

              {/* US American Accent */}
              <button
                type="button"
                onClick={() => playVoice("us")}
                className={`flex items-center justify-between p-2.5 sm:p-2 rounded-2xl border transition-all text-left active:scale-[0.98] ${
                  playingVoice === "us"
                    ? "bg-[#0071e3]/10 border-[#0071e3]/30 text-[#0071e3] dark:text-[#0a84ff] ring-2 ring-[#0071e3]/20"
                    : "bg-black/[0.02] dark:bg-white/[0.04] border-black/[0.06] dark:border-white/[0.08] hover:border-[#0071e3]/30"
                }`}
                title="播放标准美音 (US Pronunciation)"
              >
                <div className="flex flex-col">
                  <span className="text-[10px] font-semibold uppercase tracking-wider text-[#0071e3] dark:text-[#0a84ff]">
                    🇺🇸 美音
                  </span>
                  <span className="text-xs font-mono text-[#1d1d1f] dark:text-[#f5f5f7] mt-0.5">
                    {data?.phonetic_us ? `/${data.phonetic_us}/` : `/${cleanWord}/`}
                  </span>
                </div>
                <div className={`p-1.5 rounded-xl ${
                  playingVoice === "us"
                    ? "bg-[#0071e3] text-white animate-pulse"
                    : "text-[#86868b] hover:text-[#0071e3]"
                }`}>
                  <Volume2 className="w-4 h-4" />
                </div>
              </button>
            </div>

            {/* Definitions Section */}
            <div className="max-h-48 overflow-y-auto pr-1 space-y-2 text-xs sm:text-sm text-[#1d1d1f] dark:text-[#f5f5f7]">
              {data?.definitions && data.definitions.length > 0 ? (
                data.definitions.slice(0, 4).map((def, idx) => (
                  <div key={idx} className="flex items-start gap-2 leading-relaxed">
                    {def.pos && (
                      <span className="shrink-0 font-semibold px-1.5 py-0.5 rounded bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] font-mono text-[11px]">
                        {def.pos}
                      </span>
                    )}
                    <span className="text-[#1d1d1f] dark:text-[#f5f5f7] font-normal">
                      {def.meaning}
                    </span>
                  </div>
                ))
              ) : (
                <div className="text-[#86868b] italic">暂无权威中文释义</div>
              )}
            </div>

            {/* Example Sentence if available */}
            {data?.examples && data.examples.length > 0 && (
              <div className="p-3 rounded-2xl bg-black/[0.02] dark:bg-white/[0.04] border border-black/[0.04] dark:border-white/[0.06] text-xs leading-relaxed">
                <div className="flex items-center gap-1 text-[10px] font-semibold text-[#86868b] uppercase tracking-wider mb-1">
                  <Sparkles className="w-3 h-3 text-[#ff9500]" /> 搭配例句
                </div>
                <p className="font-medium text-[#1d1d1f] dark:text-[#f5f5f7]">
                  {data.examples[0].en}
                </p>
                <p className="text-[#86868b] mt-0.5">
                  {data.examples[0].zh}
                </p>
              </div>
            )}
          </div>
        )}

        {/* Footer Controls: Full width touch button on mobile */}
        <div className="mt-5 pt-3.5 border-t border-black/[0.06] dark:border-white/[0.08] flex items-center justify-between gap-3">
          <button
            type="button"
            onClick={handleAdd}
            disabled={isAdded || isLoading}
            className={`flex-1 sm:flex-initial flex items-center justify-center gap-2 text-xs font-semibold h-11 sm:h-9 px-5 rounded-full transition-all active:scale-[0.98] shadow-sm ${
              isAdded
                ? "bg-[#34c759]/15 text-[#34c759]"
                : "bg-[#0071e3] hover:bg-[#0077ed] text-white disabled:opacity-40"
            }`}
          >
            {isAdded ? (
              <>
                <Check className="w-4 h-4" /> 已加入生词本
              </>
            ) : (
              <>
                <Plus className="w-4 h-4" /> 加入生词本
              </>
            )}
          </button>

          <button
            type="button"
            onClick={onClose}
            className="hidden sm:inline-block text-xs text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] px-3 py-1.5 transition-colors"
          >
            关闭
          </button>
        </div>
      </div>
    </>
  );
}
