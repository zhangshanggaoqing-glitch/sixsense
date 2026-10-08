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
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-xs p-4 animate-in fade-in duration-150">
      <div className="w-full max-w-2xl max-h-[85vh] flex flex-col bg-white dark:bg-[#151821] border border-gray-200 dark:border-gray-800 rounded-3xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-100 dark:border-gray-800/80 bg-gray-50/50 dark:bg-[#1a1e2a]/50">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2 py-0.5 text-[11px] font-mono font-bold uppercase rounded-md bg-blue-50 text-blue-600 dark:bg-blue-900/40 dark:text-blue-300">
                {questionRange || "Questions"}
              </span>
              <h2 className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                {subpartTitle}
              </h2>
            </div>
            <p className="text-xs text-gray-400 dark:text-gray-500 mt-0.5">
              Official CET-6 Examination Questions & Options
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 rounded-xl hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Question List */}
        <div className="flex-1 overflow-y-auto px-6 py-6 space-y-8">
          {questions.length === 0 ? (
            <div className="text-center py-12 text-sm text-gray-400">
              No questions found for this topic.
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
                  className="p-5 rounded-2xl bg-gray-50/70 dark:bg-[#181c27] border border-gray-100 dark:border-gray-800"
                >
                  {/* Stem / Prompt */}
                  <div className="flex items-start gap-2.5">
                    <span className="flex-shrink-0 w-6 h-6 rounded-lg bg-gray-200 dark:bg-gray-800 flex items-center justify-center text-xs font-mono font-bold text-gray-700 dark:text-gray-300">
                      {q.question_num}
                    </span>
                    <p className="text-sm font-medium text-gray-900 dark:text-gray-100 leading-snug pt-0.5">
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
                        "bg-white dark:bg-[#202534] border-gray-200 dark:border-gray-700/80 text-gray-700 dark:text-gray-300 hover:border-gray-400 dark:hover:border-gray-500";

                      if (isAnswered) {
                        if (isThisCorrect) {
                          btnStyle =
                            "bg-emerald-50 dark:bg-emerald-950/40 border-emerald-500 text-emerald-800 dark:text-emerald-200 font-medium";
                        } else if (isThisSelected && !isCorrect) {
                          btnStyle =
                            "bg-rose-50 dark:bg-rose-950/40 border-rose-400 text-rose-800 dark:text-rose-200";
                        } else {
                          btnStyle =
                            "bg-white dark:bg-[#202534] border-gray-100 dark:border-gray-800 text-gray-400 opacity-60";
                        }
                      }

                      return (
                        <button
                          key={letter}
                          onClick={() => handleSelect(q.question_num, letter)}
                          className={`w-full flex items-center justify-between text-left px-3.5 py-2.5 rounded-xl border text-xs transition-all ${btnStyle}`}
                        >
                          <div className="flex items-center gap-2.5">
                            <span className="font-mono font-semibold uppercase text-xs w-4">
                              {letter})
                            </span>
                            <span>{optText}</span>
                          </div>
                          {isAnswered && isThisCorrect && (
                            <CheckCircle2 className="w-4 h-4 text-emerald-600 flex-shrink-0" />
                          )}
                          {isAnswered && isThisSelected && !isCorrect && (
                            <AlertCircle className="w-4 h-4 text-rose-500 flex-shrink-0" />
                          )}
                        </button>
                      );
                    })}
                  </div>

                  {/* Feedback & Explanation */}
                  {isAnswered && (
                    <div className="mt-3 pt-3 border-t border-gray-200/50 dark:border-gray-800/80 flex flex-col gap-2">
                      <div className="flex items-center justify-between">
                        <span
                          className={`text-xs font-medium flex items-center gap-1 ${
                            isCorrect ? "text-emerald-600" : "text-rose-600"
                          }`}
                        >
                          {isCorrect ? "Correct!" : `Correct Answer: ${q.correct_answer}`}
                        </span>
                        {q.explanation && (
                          <button
                            onClick={() => toggleExplanation(q.question_num)}
                            className="text-xs text-blue-600 dark:text-blue-400 hover:underline flex items-center gap-0.5"
                          >
                            <span>Explanation</span>
                            {showExpl ? (
                              <ChevronUp className="w-3.5 h-3.5" />
                            ) : (
                              <ChevronDown className="w-3.5 h-3.5" />
                            )}
                          </button>
                        )}
                      </div>

                      {showExpl && q.explanation && (
                        <div className="p-3 rounded-xl bg-blue-50/60 dark:bg-blue-950/30 text-xs text-gray-700 dark:text-gray-300 leading-relaxed font-sans mt-1">
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
        <div className="px-6 py-3 border-t border-gray-100 dark:border-gray-800/80 bg-gray-50/50 dark:bg-[#1a1e2a]/50 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold rounded-xl bg-gray-900 text-white dark:bg-white dark:text-gray-900 hover:opacity-90 transition-opacity"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
