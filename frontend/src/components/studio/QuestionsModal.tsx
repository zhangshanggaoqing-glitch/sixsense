"use client";

import React, { useState } from "react";
import { X, CheckCircle2, AlertCircle, ChevronDown, ChevronUp } from "lucide-react";
import { Question } from "@/lib/api";

interface QuestionsModalProps {
  isOpen: boolean;
  onClose: () => void;
  subpartTitle: string;
  questionRange: string;
  questions: Question[];
}

export function QuestionsModal({
  isOpen,
  onClose,
  subpartTitle,
  questionRange,
  questions,
}: QuestionsModalProps) {
  // Store user's selected answers { [questionNum]: "A" }
  const [selectedAnswers, setSelectedAnswers] = useState<Record<number, string>>({});
  // Store expanded explanations { [questionNum]: boolean }
  const [expandedExplanations, setExpandedExplanations] = useState<Record<number, boolean>>({});

  if (!isOpen) return null;

  const handleSelect = (qNum: number, option: string) => {
    setSelectedAnswers((prev) => ({ ...prev, [qNum]: option }));
  };

  const toggleExplanation = (qNum: number) => {
    setExpandedExplanations((prev) => ({ ...prev, [qNum]: !prev[qNum] }));
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/40 backdrop-blur-sm p-0 sm:p-4 animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div
        className="w-full max-w-2xl max-h-[90vh] sm:max-h-[85vh] flex flex-col bg-white dark:bg-[#1c1c1e] border-t sm:border border-black/[0.08] dark:border-white/[0.1] rounded-t-[28px] sm:rounded-3xl shadow-2xl overflow-hidden animate-in slide-in-from-bottom sm:zoom-in-95 duration-200 pb-[env(safe-area-inset-bottom)]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* iOS Drag Handle on Mobile */}
        <div className="w-10 h-1 bg-black/15 dark:bg-white/20 rounded-full mx-auto mt-2.5 sm:hidden" />

        {/* Header */}
        <div className="flex items-center justify-between px-4 sm:px-6 py-3.5 sm:py-4 border-b border-black/[0.06] dark:border-white/[0.08] bg-black/[0.02] dark:bg-white/[0.02]">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 text-[11px] font-semibold rounded-full bg-[#0071e3]/10 text-[#0071e3] dark:bg-[#0a84ff]/20 dark:text-[#0a84ff]">
                官方考题 {questionRange ? `· ${questionRange}` : ""}
              </span>
              <h2 className="text-xs sm:text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] truncate max-w-[180px] sm:max-w-none">
                {subpartTitle}
              </h2>
            </div>
            <p className="text-xs text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
              全国大学英语六级官方真题与选项
            </p>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 active:scale-90 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Question List */}
        <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-4 sm:py-6 space-y-5 sm:space-y-6">
          {questions.length === 0 ? (
            <div className="text-center py-12 text-sm text-[#86868b]">
              当前分节暂无对应考题。
            </div>
          ) : (
            questions.map((q) => {
              const selected = selectedAnswers[q.question_num];
              const isAnswered = selected !== undefined;
              const isCorrect = selected === q.correct_answer;
              const showExpl = expandedExplanations[q.question_num];

              return (
                <div
                  key={q.id}
                  className="p-5 rounded-2xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.06]"
                >
                  {/* Stem / Prompt */}
                  <div className="flex items-start gap-2.5">
                    <span className="flex-shrink-0 w-6 h-6 rounded-full bg-black/[0.06] dark:bg-white/[0.1] flex items-center justify-center text-xs font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                      {q.question_num}
                    </span>
                    <p className="text-sm font-medium text-[#1d1d1f] dark:text-[#f5f5f7] leading-relaxed pt-0.5">
                      {q.prompt}
                    </p>
                  </div>

                  {/* 4 Choices */}
                  <div className="mt-4 space-y-2">
                    {(["A", "B", "C", "D"] as const).map((letter) => {
                      const optText =
                        letter === "A"
                          ? q.option_a
                          : letter === "B"
                          ? q.option_b
                          : letter === "C"
                          ? q.option_c
                          : q.option_d;

                      if (!optText) return null;

                      const isThisSelected = selected === letter;
                      const isThisCorrect = q.correct_answer === letter;

                      let btnStyle =
                        "bg-white dark:bg-[#2c2c2e] border-black/[0.06] dark:border-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7] hover:border-[#0071e3]/40";

                      if (isAnswered) {
                        if (isThisCorrect) {
                          btnStyle =
                            "bg-[#34c759]/10 border-[#34c759] text-[#34c759] dark:text-[#30d158] font-medium";
                        } else if (isThisSelected && !isCorrect) {
                          btnStyle =
                            "bg-[#ff3b30]/10 border-[#ff3b30] text-[#ff3b30] dark:text-[#ff453a]";
                        } else {
                          btnStyle =
                            "bg-white dark:bg-[#2c2c2e] border-black/[0.04] dark:border-white/[0.06] text-[#86868b] opacity-60";
                        }
                      }

                      return (
                        <button
                          key={letter}
                          onClick={() => handleSelect(q.question_num, letter)}
                          className={`w-full flex items-center justify-between text-left px-3.5 py-2.5 rounded-xl border text-xs transition-all ${btnStyle}`}
                        >
                          <div className="flex items-center gap-2.5">
                            <span className="font-semibold uppercase text-xs w-4">
                              {letter})
                            </span>
                            <span>{optText}</span>
                          </div>
                          {isAnswered && isThisCorrect && (
                            <CheckCircle2 className="w-4 h-4 text-[#34c759] shrink-0" />
                          )}
                          {isAnswered && isThisSelected && !isCorrect && (
                            <AlertCircle className="w-4 h-4 text-[#ff3b30] shrink-0" />
                          )}
                        </button>
                      );
                    })}
                  </div>

                  {/* Feedback & Explanation */}
                  {isAnswered && (
                    <div className="mt-3 pt-3 border-t border-black/[0.06] dark:border-white/[0.08] flex flex-col gap-2">
                      <div className="flex items-center justify-between">
                        <span
                          className={`text-xs font-medium flex items-center gap-1 ${
                            isCorrect ? "text-[#34c759]" : "text-[#ff3b30]"
                          }`}
                        >
                          {isCorrect ? "回答正确" : `正确答案：${q.correct_answer}`}
                        </span>
                        {q.explanation && (
                          <button
                            onClick={() => toggleExplanation(q.question_num)}
                            className="text-xs text-[#0071e3] dark:text-[#0a84ff] hover:underline flex items-center gap-0.5"
                          >
                            <span>真题解析</span>
                            {showExpl ? (
                              <ChevronUp className="w-3.5 h-3.5" />
                            ) : (
                              <ChevronDown className="w-3.5 h-3.5" />
                            )}
                          </button>
                        )}
                      </div>

                      {showExpl && q.explanation && (
                        <div className="p-3 rounded-xl bg-black/[0.02] dark:bg-white/[0.04] text-xs text-[#1d1d1f] dark:text-[#f5f5f7] leading-relaxed mt-1">
                          {q.explanation}
                        </div>
                      )}
                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

        {/* Footer */}
        <div className="px-6 py-3 border-t border-black/[0.06] dark:border-white/[0.08] bg-black/[0.02] dark:bg-white/[0.02] flex justify-end">
          <button
            onClick={onClose}
            className="px-5 py-2 text-xs font-semibold rounded-full bg-[#1d1d1f] text-white dark:bg-[#f5f5f7] dark:text-[#1d1d1f] hover:opacity-90 transition-opacity"
          >
            完成
          </button>
        </div>
      </div>
    </div>
  );
}
