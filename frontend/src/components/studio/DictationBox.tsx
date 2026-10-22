"use client";

import React, { useState, useEffect, useRef } from "react";
import { Check, RotateCcw, ArrowRight } from "lucide-react";
import { api, Sentence, DiffResult } from "@/lib/api";
import { WordPopover } from "./WordPopover";

interface DictationBoxProps {
  sentence: Sentence;
  examId?: string;
  onNext: () => void;
  onReplay: () => void;
}

export function DictationBox({ sentence, examId = "", onNext, onReplay }: DictationBoxProps) {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<DiffResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedWord, setSelectedWord] = useState<string | null>(null);
  const [popoverPos, setPopoverPos] = useState<{ top: number; left: number }>({ top: 0, left: 0 });
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);

  // Focus textarea when sentence changes
  useEffect(() => {
    setInput("");
    setResult(null);
    if (textareaRef.current) {
      textareaRef.current.focus();
    }
  }, [sentence.id]);

  const handleCheck = async () => {
    if (!input.trim() || isLoading) return;
    setIsLoading(true);
    try {
      const res = await api.checkDictation(sentence.id, sentence.english, input);
      setResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (!result) {
        handleCheck();
      } else {
        onNext();
      }
    }
  };

  const handleWordClick = (e: React.MouseEvent, wordText: string) => {
    e.stopPropagation();
    const clean = wordText.replace(/[^\w'-]+/g, "");
    if (!clean) return;
    const rect = (e.target as HTMLElement).getBoundingClientRect();
    setSelectedWord(clean);
    setPopoverPos({ top: rect.bottom, left: rect.left });
  };

  return (
    <div className="w-full max-w-2xl mx-auto flex flex-col items-center">
      {!result ? (
        <div className="w-full flex flex-col items-center animate-in fade-in duration-200">
          <p className="text-xs font-medium text-[#86868b] dark:text-[#a1a1a6] mb-3 tracking-wider">
            请聆听音频并默写英文句子
          </p>

          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={3}
            placeholder="输入听到的句子..."
            className="w-full p-5 text-base sm:text-lg bg-white dark:bg-[#1c1c1e] text-[#1d1d1f] dark:text-[#f5f5f7] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl focus:outline-none focus:border-[#0071e3] focus:ring-4 focus:ring-[#0071e3]/10 shadow-[0_2px_12px_rgba(0,0,0,0.04)] placeholder:text-[#86868b]/60 resize-none transition-all leading-relaxed"
          />

          <div className="mt-4 flex items-center gap-3">
            <button
              onClick={handleCheck}
              disabled={!input.trim() || isLoading}
              className="h-11 px-6 bg-[#0071e3] hover:bg-[#0077ed] disabled:opacity-40 text-white text-sm font-medium rounded-full shadow-sm flex items-center gap-2 active:scale-95 transition-all"
            >
              <Check className="w-4 h-4" /> 提交核对 (Enter)
            </button>
            <button
              onClick={onReplay}
              className="h-11 px-4 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 text-sm font-medium rounded-full flex items-center gap-1.5 transition-colors"
            >
              <RotateCcw className="w-4 h-4" /> 重听原句
            </button>
          </div>
        </div>
      ) : (
        <div className="w-full bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] p-6 sm:p-7 rounded-2xl shadow-[0_4px_24px_rgba(0,0,0,0.06)] animate-in fade-in duration-200 text-left">
          {/* Header: Accuracy Stat */}
          <div className="flex items-center justify-between border-b border-black/[0.06] dark:border-white/[0.08] pb-3.5 mb-5">
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold text-[#86868b] dark:text-[#a1a1a6]">听写准确率</span>
              <span
                className={`text-base font-bold ${
                  result.accuracy_score >= 0.9
                    ? "text-[#34c759]"
                    : result.accuracy_score >= 0.7
                    ? "text-[#ff9500]"
                    : "text-[#ff3b30]"
                }`}
              >
                {Math.round(result.accuracy_score * 100)}%
              </span>
            </div>

            <div className="flex items-center gap-3 text-xs text-[#86868b]">
              {result.stats.missing_words > 0 && (
                <span className="text-[#ff3b30]">漏 {result.stats.missing_words} 词</span>
              )}
              {result.stats.form_errors > 0 && (
                <span className="text-[#ff9500]">形差 {result.stats.form_errors} 处</span>
              )}
              {result.stats.extra_words > 0 && (
                <span>冗余 {result.stats.extra_words} 词</span>
              )}
            </div>
          </div>

          {/* Word-level Diff Breakdown: 正确为绿色，错误用红色下划线 */}
          <div className="text-lg sm:text-xl leading-relaxed flex flex-wrap gap-x-2 gap-y-1.5 items-center mb-6">
            {result.diff_tokens.map((tok, idx) => {
              if (tok.type === "match") {
                return (
                  <span
                    key={idx}
                    onClick={(e) => handleWordClick(e, tok.standard)}
                    className="text-[#34c759] font-medium cursor-pointer hover:opacity-80"
                    title="正确：点击查词"
                  >
                    {tok.standard}
                  </span>
                );
              }
              if (tok.type === "missing") {
                return (
                  <span
                    key={idx}
                    onClick={(e) => handleWordClick(e, tok.standard)}
                    className="text-[#ff3b30] underline decoration-[#ff3b30] decoration-2 underline-offset-4 font-semibold cursor-pointer hover:opacity-80"
                    title="漏词：点击查看正确读音与释义"
                  >
                    {tok.standard}
                  </span>
                );
              }
              if (tok.type === "form_diff") {
                return (
                  <span
                    key={idx}
                    onClick={(e) => handleWordClick(e, tok.standard)}
                    className="text-[#ff9500] underline decoration-[#ff9500] decoration-2 underline-offset-4 font-semibold cursor-pointer hover:opacity-80"
                    title={`词形差异 (输入了 '${tok.user}')：点击查看读音与释义`}
                  >
                    {tok.standard}
                  </span>
                );
              }
              if (tok.type === "extra") {
                return (
                  <span
                    key={idx}
                    onClick={(e) => handleWordClick(e, tok.user)}
                    className="text-[#86868b] line-through text-sm cursor-pointer hover:opacity-80"
                    title="冗余词"
                  >
                    {tok.user}
                  </span>
                );
              }
              return (
                <span
                  key={idx}
                  onClick={(e) => handleWordClick(e, tok.standard)}
                  className="text-[#ff3b30] underline decoration-[#ff3b30] decoration-2 underline-offset-4 cursor-pointer hover:opacity-80"
                >
                  {tok.standard}
                </span>
              );
            })}
          </div>

          {/* Standard Transcript & Translation Hint */}
          <div className="p-4 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.06] space-y-1.5 mb-6">
            <div className="text-xs font-semibold text-[#86868b]">标准听力原文</div>
            <p className="text-sm font-medium text-[#1d1d1f] dark:text-[#f5f5f7]">
              {sentence.english}
            </p>
            <p className="text-xs text-[#86868b] dark:text-[#a1a1a6] pt-1">
              {sentence.chinese}
            </p>
          </div>

          {/* Bottom Actions */}
          <div className="flex items-center justify-end gap-3">
            <button
              onClick={() => setResult(null)}
              className="h-10 px-4 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 rounded-full flex items-center gap-1.5 transition-colors"
            >
              <RotateCcw className="w-3.5 h-3.5" /> 重新默写
            </button>
            <button
              onClick={onNext}
              className="h-10 px-5 bg-[#1d1d1f] dark:bg-[#f5f5f7] text-white dark:text-[#1d1d1f] text-xs font-medium rounded-full flex items-center gap-1.5 hover:opacity-90 active:scale-95 shadow-sm transition-all"
            >
              下一句 <ArrowRight className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      )}

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
