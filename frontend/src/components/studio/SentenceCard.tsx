"use client";

import React, { useState } from "react";
import { Headphones, Eye } from "lucide-react";
import { Sentence } from "@/lib/api";
import { WordPopover } from "./WordPopover";
import { DictationBox } from "./DictationBox";

interface SentenceCardProps {
  sentence: Sentence;
  displayMode: "A" | "B" | "C" | "D";
  isPlaying: boolean;
  examId: string;
  onNext: () => void;
  onReplay: () => void;
  onToggleTranslation: () => void;
}

export function SentenceCard({
  sentence,
  displayMode,
  isPlaying,
  examId,
  onNext,
  onReplay,
  onToggleTranslation,
}: SentenceCardProps) {
  const [selectedWord, setSelectedWord] = useState<string | null>(null);
  const [popoverPos, setPopoverPos] = useState<{ top: number; left: number }>({ top: 0, left: 0 });

  const handleWordClick = (e: React.MouseEvent, word: string) => {
    e.stopPropagation();
    const rect = (e.target as HTMLElement).getBoundingClientRect();
    setSelectedWord(word);
    setPopoverPos({ top: rect.bottom, left: rect.left });
  };

  // If in Dictation mode (Mode D)
  if (displayMode === "D") {
    return <DictationBox sentence={sentence} onNext={onNext} onReplay={onReplay} />;
  }

  // Tokenize sentence into clickable words
  const words = sentence.english.split(/(\s+)/);

  return (
    <div className="w-full max-w-3xl mx-auto flex flex-col items-center text-center px-4 py-8">
      {/* Speaker Tag if present */}
      {sentence.speaker && (
        <span className="text-[11px] font-mono tracking-widest uppercase font-semibold text-gray-400 dark:text-gray-500 mb-6 px-2.5 py-0.5 rounded-full bg-gray-100 dark:bg-gray-800/60">
          Speaker {sentence.speaker}
        </span>
      )}

      {/* Main English Sentence Area */}
      <div className="min-h-[140px] flex items-center justify-center w-full">
        {displayMode === "C" ? (
          // Blind Mode: Absolute focus on hearing
          <div className="flex flex-col items-center justify-center animate-in fade-in duration-300">
            <div className={`p-4 rounded-full transition-all duration-300 ${
              isPlaying
                ? "bg-blue-50 dark:bg-blue-950/40 text-blue-600 dark:text-blue-400 scale-105"
                : "text-gray-300 dark:text-gray-700"
            }`}>
              <Headphones className="w-8 h-8" />
            </div>
            <p className="mt-4 text-xl font-medium tracking-tight text-gray-400 dark:text-gray-500">
              Listen.
            </p>
            <p className="mt-1 text-xs text-gray-400 dark:text-gray-600 font-mono">
              Press [A] to reveal English
            </p>
          </div>
        ) : (
          // Mode A or Mode B: English Text Visible
          <div className="text-2xl sm:text-3xl font-medium tracking-tight leading-relaxed text-gray-900 dark:text-gray-50 flex flex-wrap justify-center gap-x-1.5 gap-y-1 animate-in fade-in duration-200">
            {words.map((item, idx) => {
              if (/^\s+$/.test(item)) {
                return <span key={idx}>{item}</span>;
              }
              const clean = item.replace(/[^\w']+/g, "");
              if (!clean) return <span key={idx}>{item}</span>;

              return (
                <span
                  key={idx}
                  onClick={(e) => handleWordClick(e, clean)}
                  className="cursor-pointer hover:text-blue-600 dark:hover:text-blue-400 hover:underline decoration-blue-500/30 decoration-2 underline-offset-4 rounded transition-colors"
                >
                  {item}
                </span>
              );
            })}
          </div>
        )}
      </div>

      {/* Translation Area */}
      <div className="min-h-[50px] mt-6 flex items-center justify-center">
        {displayMode === "A" ? (
          <p className="text-base sm:text-lg text-gray-500 dark:text-gray-400 font-normal tracking-wide animate-in fade-in duration-200">
            {sentence.chinese}
          </p>
        ) : displayMode === "B" ? (
          <button
            onClick={onToggleTranslation}
            className="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 flex items-center gap-1 transition-colors"
          >
            <Eye className="w-3.5 h-3.5" /> Show Translation (T)
          </button>
        ) : null}
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
