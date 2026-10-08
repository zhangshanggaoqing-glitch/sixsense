"use client";

import React, { useState, useEffect, useRef } from "react";
import { Check, RotateCcw, ArrowRight } from "lucide-react";
import { api, Sentence, DiffResult } from "@/lib/api";

interface DictationBoxProps {
  sentence: Sentence;
  onNext: () => void;
  onReplay: () => void;
}

export function DictationBox({ sentence, onNext, onReplay }: DictationBoxProps) {
  const [input, setInput] = useState("");
  const [result, setResult] = useState<DiffResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
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

  return (
    <div className="w-full max-w-2xl mx-auto flex flex-col items-center">
      {!result ? (
        <div className="w-full flex flex-col items-center">
          <p className="text-sm font-medium text-gray-400 dark:text-gray-500 mb-4 tracking-wide uppercase">
            Type what you hear
          </p>

          <textarea
            ref={textareaRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            rows={3}
            placeholder="Listen and write the sentence..."
            className="w-full p-4 text-lg bg-gray-50 dark:bg-[#13161f] border border-gray-200 dark:border-gray-800 rounded-2xl focus:outline-none focus:ring-2 focus:ring-blue-500/40 focus:border-blue-500 text-gray-900 dark:text-gray-100 placeholder:text-gray-400 resize-none shadow-sm"
          />

          <div className="mt-4 flex items-center gap-3">
            <button
              onClick={handleCheck}
              disabled={!input.trim() || isLoading}
              className="px-6 py-2.5 bg-blue-600 hover:bg-blue-700 disabled:opacity-40 text-white text-sm font-medium rounded-xl shadow-sm flex items-center gap-2"
            >
              <Check className="w-4 h-4" /> Check (Enter)
            </button>
            <button
              onClick={onReplay}
              className="px-4 py-2.5 border border-gray-200 dark:border-gray-800 hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300 text-sm font-medium rounded-xl flex items-center gap-1.5"
            >
              <RotateCcw className="w-4 h-4" /> Replay
            </button>
          </div>
        </div>
      ) : (
        <div className="w-full bg-white dark:bg-[#151821] border border-gray-200 dark:border-gray-800/80 p-6 rounded-2xl shadow-md animate-in fade-in duration-200">
          <div className="flex items-center justify-between border-b border-gray-100 dark:border-gray-800/80 pb-3 mb-4">
            <div className="flex items-center gap-2">
              <span className="text-xs uppercase font-bold text-gray-400 tracking-wider">Accuracy</span>
              <span
                className={`text-sm font-bold ${
                  result.accuracy_score >= 0.9
                    ? "text-green-600 dark:text-green-400"
                    : result.accuracy_score >= 0.7
                    ? "text-amber-500"
                    : "text-red-500"
                }`}
              >
                {Math.round(result.accuracy_score * 100)}%
              </span>
            </div>

            <div className="flex items-center gap-2 text-xs text-gray-400">
              {result.stats.missing_words > 0 && (
                <span className="text-red-500">{result.stats.missing_words} missing</span>
              )}
              {result.stats.form_errors > 0 && (
                <span className="text-amber-500">{result.stats.form_errors} form</span>
              )}
              {result.stats.extra_words > 0 && (
                <span className="text-gray-400">{result.stats.extra_words} extra</span>
              )}
            </div>
          </div>

          {/* Word-level Diff Breakdown */}
          <div className="text-lg leading-relaxed flex flex-wrap gap-1.5 items-center mb-6">
            {result.diff_tokens.map((tok, idx) => {
              if (tok.type === "match") {
                return (
                  <span key={idx} className="text-gray-900 dark:text-gray-100 font-medium">
                    {tok.standard}
                  </span>
                );
              }
              if (tok.type === "missing") {
                return (
                  <span
                    key={idx}
                    className="px-1.5 py-0.5 bg-red-100 dark:bg-red-950/50 text-red-600 dark:text-red-400 rounded border border-red-200 dark:border-red-900/60 font-semibold"
                    title="Missing word"
                  >
                    {tok.standard}
                  </span>
                );
              }
              if (tok.type === "form_diff") {
                return (
                  <span
                    key={idx}
                    className="px-1.5 py-0.5 bg-amber-100 dark:bg-amber-950/50 text-amber-700 dark:text-amber-300 rounded border border-amber-200 dark:border-amber-900/60 font-semibold"
                    title={`Form difference: user wrote '${tok.user}'`}
                  >
                    {tok.standard}
                  </span>
                );
              }
              if (tok.type === "extra") {
                return (
                  <span
                    key={idx}
                    className="px-1.5 py-0.5 bg-gray-100 dark:bg-gray-800 text-gray-400 line-through rounded text-sm"
                    title="Extra word"
                  >
                    {tok.user}
                  </span>
                );
              }
              return (
                <span key={idx} className="text-red-500">
                  {tok.standard}
                </span>
              );
            })}
          </div>

          {/* Translation hint */}
          <p className="text-sm text-gray-500 dark:text-gray-400 border-t border-gray-100 dark:border-gray-800/80 pt-3">
            {sentence.chinese}
          </p>

          <div className="mt-5 flex items-center justify-end gap-3">
            <button
              onClick={() => setResult(null)}
              className="px-4 py-2 border border-gray-200 dark:border-gray-800 hover:bg-gray-100 dark:hover:bg-gray-800 text-gray-600 dark:text-gray-300 text-sm font-medium rounded-xl flex items-center gap-1.5"
            >
              <RotateCcw className="w-3.5 h-3.5" /> Try Again
            </button>
            <button
              onClick={onNext}
              className="px-5 py-2 bg-gray-900 dark:bg-white text-white dark:text-gray-900 hover:opacity-90 text-sm font-medium rounded-xl flex items-center gap-1.5 shadow-sm"
            >
              Next Sentence <ArrowRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
