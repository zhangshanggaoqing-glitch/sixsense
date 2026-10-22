"use client";

import React, { useState, useEffect } from "react";
import { Headphones, Eye, EyeOff } from "lucide-react";
import { Sentence } from "@/lib/api";
import { formatSpeakerZh } from "@/lib/formatters";
import { WordPopover } from "./WordPopover";
import { DictationBox } from "./DictationBox";

interface SentenceCardProps {
  sentence: Sentence;
  displayMode: "blind" | "bilingual" | "dictation" | "A" | "B" | "C" | "D";
  isPlaying: boolean;
  examId: string;
  onNext: () => void;
  onReplay: () => void;
  onTogglePlay?: () => void;
  isConversation?: boolean;
}

export function SentenceCard({
  sentence,
  displayMode,
  isPlaying,
  examId,
  onNext,
  onReplay,
  onTogglePlay,
  isConversation = false,
}: SentenceCardProps) {
  const [selectedWord, setSelectedWord] = useState<string | null>(null);
  const [popoverPos, setPopoverPos] = useState<{
    top: number;
    left: number;
    wordTop?: number;
    wordHeight?: number;
  }>({ top: 0, left: 0 });
  const [showBlindTranscript, setShowBlindTranscript] = useState(false);

  // Reset blind transcript reveal when sentence changes
  useEffect(() => {
    setShowBlindTranscript(false);
  }, [sentence.id]);

  const handleWordClick = (e: React.MouseEvent, word: string) => {
    e.stopPropagation();
    const rect = (e.target as HTMLElement).getBoundingClientRect();
    setSelectedWord(word);
    setPopoverPos({
      top: rect.bottom,
      left: rect.left,
      wordTop: rect.top,
      wordHeight: rect.height,
    });
  };

  // Normalization for 3 modes
  const isDictation = displayMode === "dictation" || displayMode === "D";
  const isBlind = displayMode === "blind" || displayMode === "C";

  // 1. Dictation Mode
  if (isDictation) {
    return <DictationBox sentence={sentence} examId={examId} onNext={onNext} onReplay={onReplay} />;
  }

  // Tokenize sentence for word lookup
  const words = sentence.english.split(/(\s+)/);
  const speakerZh = isConversation ? formatSpeakerZh(sentence.speaker) : "";

  return (
    <div className="w-full max-w-3xl mx-auto flex flex-col items-center text-center px-4 py-6 sm:py-10 select-none">
      {/* Speaker Tag: 男 / 女 */}
      {speakerZh && (
        <div className="mb-5 animate-in fade-in duration-200">
          <span className="text-[12px] font-medium tracking-wider text-[#86868b] dark:text-[#a1a1a6] px-3 py-1 rounded-full bg-black/[0.04] dark:bg-white/[0.06]">
            {speakerZh}
          </span>
        </div>
      )}

      {/* Main Focus Area */}
      <div className="min-h-[160px] flex items-center justify-center w-full">
        {isBlind && !showBlindTranscript ? (
          // Blind Mode: Absolute focus on hearing
          <div className="flex flex-col items-center justify-center animate-in fade-in duration-300 py-4">
            <button
              onClick={onTogglePlay}
              className={`p-6 rounded-full transition-all duration-300 ${
                isPlaying
                  ? "bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] scale-105 shadow-[0_0_30px_rgba(0,113,227,0.25)]"
                  : "bg-black/[0.03] dark:bg-white/[0.05] text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              }`}
              title="点击播放 / 暂停"
            >
              <Headphones className="w-9 h-9" />
            </button>
            <p className="mt-4 text-base font-normal text-[#86868b] dark:text-[#a1a1a6]">
              静心聆听，捕捉语音细节
            </p>
            <button
              onClick={() => setShowBlindTranscript(true)}
              className="mt-3 text-xs font-medium text-[#0071e3] dark:text-[#0a84ff] hover:underline flex items-center gap-1.5 px-3 py-1 rounded-full hover:bg-[#0071e3]/5 transition-colors"
            >
              <Eye className="w-3.5 h-3.5" /> 显示原文
            </button>
          </div>
        ) : (
          // Bilingual Mode (or revealed Blind transcript): English Hero text
          <div className="flex flex-col items-center justify-center animate-in fade-in duration-200">
            <div className="text-2xl sm:text-[28px] font-medium tracking-tight leading-relaxed text-[#1d1d1f] dark:text-[#f5f5f7] flex flex-wrap justify-center gap-x-2 gap-y-1">
              {words.map((item, idx) => {
                if (/^\s+$/.test(item)) {
                  return <span key={idx}>{item}</span>;
                }
                const clean = item.replace(/[^\w'-]+/g, "");
                if (!clean) return <span key={idx}>{item}</span>;

                return (
                  <span
                    key={idx}
                    onClick={(e) => handleWordClick(e, clean)}
                    className="cursor-pointer hover:text-[#0071e3] dark:hover:text-[#0a84ff] hover:underline decoration-[#0071e3]/30 decoration-2 underline-offset-4 rounded transition-colors"
                  >
                    {item}
                  </span>
                );
              })}
            </div>

            {/* Translation underneath in lighter, secondary size */}
            <p className="mt-4 text-base sm:text-lg text-[#86868b] dark:text-[#a1a1a6] font-normal leading-relaxed max-w-2xl">
              {sentence.chinese}
            </p>

            {/* If in Blind mode but revealed, offer re-hide option */}
            {isBlind && showBlindTranscript && (
              <button
                onClick={() => setShowBlindTranscript(false)}
                className="mt-4 text-xs text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] flex items-center gap-1 transition-colors"
              >
                <EyeOff className="w-3.5 h-3.5" /> 隐去原文
              </button>
            )}
          </div>
        )}
      </div>

      {/* Word Popover Anchor */}
      {selectedWord && (
        <WordPopover
          word={selectedWord}
          currentSentence={sentence}
          examId={examId}
          onClose={() => setSelectedWord(null)}
          position={popoverPos}
        />
      )}
    </div>
  );
}
