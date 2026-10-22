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
      {/* Invisible backdrop to dismiss popover when clicking anywhere outside */}
      <div
        className="fixed inset-0 z-40 bg-transparent cursor-default"
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
        className="fixed z-50 p-4 sm:p-5 bg-white/95 dark:bg-[#151822]/95 border border-black/[0.08] dark:border-white/[0.1] rounded-2xl shadow-2xl w-[340px] sm:w-[360px] max-h-[min(520px,calc(100vh-28px))] overflow-y-auto backdrop-blur-xl animate-in fade-in zoom-in-95 duration-150 text-left select-text"
        style={{ top: `${coords.top}px`, left: `${coords.left}px` }}
        onClick={(e) => e.stopPropagation()}
      >
      {/* Header: Word & Tags */}
      <div className="flex items-start justify-between gap-2 border-b border-gray-100 dark:border-gray-800/80 pb-3">
        <div>
          <div className="flex items-baseline gap-2">
            <h4 className="text-xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
              {cleanWord}
            </h4>
            {data?.lemma && data.lemma !== cleanWord && (
              <span className="text-xs text-gray-400 font-mono">
                (原形: {data.lemma})
              </span>
            )}
          </div>
        </div>

        <div className="flex items-center gap-1.5 flex-wrap justify-end">
          <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 rounded-full border border-blue-200 dark:border-blue-900">
            CET-6
          </span>
          {data?.tags?.slice(0, 2).map((t, idx) => (
            t !== "CET6" && t !== "CET-6" ? (
              <span key={idx} className="text-[10px] font-medium px-1.5 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-500 dark:text-gray-400 rounded-md">
                {t}
              </span>
            ) : null
          ))}
        </div>
      </div>

      {isLoading ? (
        <div className="py-8 flex flex-col items-center justify-center gap-2 text-gray-400">
          <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
          <span className="text-xs font-mono">正在检索权威英美读音与释义...</span>
        </div>
      ) : (
        <div className="mt-3 space-y-3">
          {/* Pronunciations: UK & US */}
          <div className="grid grid-cols-2 gap-2">
            {/* UK British Accent */}
            <button
              onClick={() => playVoice("uk")}
              className={`flex items-center justify-between p-2 rounded-xl border transition-all text-left ${
                playingVoice === "uk"
                  ? "bg-indigo-50 border-indigo-300 dark:bg-indigo-950/40 dark:border-indigo-700 ring-2 ring-indigo-500/30"
                  : "bg-gray-50/80 dark:bg-[#1a1e2b] border-gray-100 dark:border-gray-800 hover:border-indigo-200 dark:hover:border-indigo-900"
              }`}
              title="播放纯正英音 (UK Pronunciation)"
            >
              <div className="flex flex-col">
                <span className="text-[10px] font-semibold uppercase tracking-wider text-indigo-600 dark:text-indigo-400">
                  🇬🇧 英音
                </span>
                <span className="text-xs font-mono text-gray-600 dark:text-gray-300 mt-0.5">
                  {data?.phonetic_uk ? `/${data.phonetic_uk}/` : `/${cleanWord}/`}
                </span>
              </div>
              <div className={`p-1.5 rounded-lg ${
                playingVoice === "uk"
                  ? "bg-indigo-600 text-white animate-pulse"
                  : "text-gray-400 hover:text-indigo-600 dark:hover:text-indigo-400"
              }`}>
                <Volume2 className="w-4 h-4" />
              </div>
            </button>

            {/* US American Accent */}
            <button
              onClick={() => playVoice("us")}
              className={`flex items-center justify-between p-2 rounded-xl border transition-all text-left ${
                playingVoice === "us"
                  ? "bg-blue-50 border-blue-300 dark:bg-blue-950/40 dark:border-blue-700 ring-2 ring-blue-500/30"
                  : "bg-gray-50/80 dark:bg-[#1a1e2b] border-gray-100 dark:border-gray-800 hover:border-blue-200 dark:hover:border-blue-900"
              }`}
              title="播放标准美音 (US Pronunciation)"
            >
              <div className="flex flex-col">
                <span className="text-[10px] font-semibold uppercase tracking-wider text-blue-600 dark:text-blue-400">
                  🇺🇸 美音
                </span>
                <span className="text-xs font-mono text-gray-600 dark:text-gray-300 mt-0.5">
                  {data?.phonetic_us ? `/${data.phonetic_us}/` : `/${cleanWord}/`}
                </span>
              </div>
              <div className={`p-1.5 rounded-lg ${
                playingVoice === "us"
                  ? "bg-blue-600 text-white animate-pulse"
                  : "text-gray-400 hover:text-blue-600 dark:hover:text-blue-400"
              }`}>
                <Volume2 className="w-4 h-4" />
              </div>
            </button>
          </div>

          {/* Definitions Section */}
          <div className="max-h-40 overflow-y-auto pr-1 space-y-1.5 text-xs text-gray-700 dark:text-gray-200">
            {data?.definitions && data.definitions.length > 0 ? (
              data.definitions.slice(0, 4).map((def, idx) => (
                <div key={idx} className="flex items-start gap-1.5 leading-relaxed">
                  {def.pos && (
                    <span className="shrink-0 font-semibold px-1 py-0.5 rounded bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 font-mono text-[11px]">
                      {def.pos}
                    </span>
                  )}
                  <span className="text-gray-800 dark:text-gray-200 font-normal">
                    {def.meaning}
                  </span>
                </div>
              ))
            ) : (
              <div className="text-gray-400 italic">暂无权威中文释义</div>
            )}
          </div>

          {/* Example Sentence if available */}
          {data?.examples && data.examples.length > 0 && (
            <div className="p-2.5 rounded-xl bg-gray-50/80 dark:bg-[#1a1e2b] border border-gray-100 dark:border-gray-800/80 text-[11px] leading-relaxed">
              <div className="flex items-center gap-1 text-[10px] font-semibold text-gray-400 uppercase tracking-wider mb-1">
                <Sparkles className="w-3 h-3 text-amber-500" /> 经典搭配例句
              </div>
              <p className="font-medium text-gray-700 dark:text-gray-300">
                {data.examples[0].en}
              </p>
              <p className="text-gray-400 dark:text-gray-500 mt-0.5">
                {data.examples[0].zh}
              </p>
            </div>
          )}
        </div>
      )}

      {/* Footer Controls */}
      <div className="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800/80 flex items-center justify-between">
        <button
          onClick={handleAdd}
          disabled={isAdded || isLoading}
          className={`flex items-center gap-1.5 text-xs font-medium px-3.5 py-1.5 rounded-xl transition-all shadow-sm ${
            isAdded
              ? "bg-green-100 dark:bg-green-950/60 text-green-700 dark:text-green-300"
              : "bg-gray-900 dark:bg-white text-white dark:text-gray-900 hover:opacity-90 disabled:opacity-40"
          }`}
        >
          {isAdded ? (
            <>
              <Check className="w-3.5 h-3.5" /> 已收入生词本
            </>
          ) : (
            <>
              <Plus className="w-3.5 h-3.5" /> 收入生词本
            </>
          )}
        </button>

        <button
          onClick={onClose}
          className="text-xs text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 px-2 py-1 transition-colors"
        >
          关闭
        </button>
      </div>
    </div>
    </>
  );
}
