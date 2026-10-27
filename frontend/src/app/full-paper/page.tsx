"use client";

import React, { useState, useEffect, Suspense } from "react";
import Link from "next/link";
import { useSearchParams } from "next/navigation";
import {
  ChevronLeft,
  Download,
  Headphones,
  CheckCircle2,
  ChevronDown,
  ChevronUp,
} from "lucide-react";
import { api, FullPaperDetail } from "@/lib/api";
import { FullAudioBar } from "@/components/full-paper/FullAudioBar";

function FullPaperContent() {
  const searchParams = useSearchParams();
  const paperId = searchParams.get("id") || searchParams.get("paper_id") || searchParams.get("exam_id") || "2026-06-set1";

  const [paper, setPaper] = useState<FullPaperDetail | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isError, setIsError] = useState(false);

  // User simulated answers { [questionId]: "A" | "B" | "C" | "D" }
  const [selectedAnswers, setSelectedAnswers] = useState<Record<string, string>>({});
  // Toggled explanations { [questionId]: boolean }
  const [showExplanations, setShowExplanations] = useState<Record<string, boolean>>({});

  useEffect(() => {
    async function load() {
      setIsLoading(true);
      setIsError(false);
      try {
        const data = await api.getFullPaperDetail(paperId);
        setPaper(data);
      } catch (err) {
        console.error("Failed to load full paper", err);
        setIsError(true);
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, [paperId]);

  const handleSelectOption = (questionId: string, optionKey: string) => {
    setSelectedAnswers((prev) => ({
      ...prev,
      [questionId]: prev[questionId] === optionKey ? "" : optionKey,
    }));
  };

  const toggleExplanation = (questionId: string) => {
    setShowExplanations((prev) => ({
      ...prev,
      [questionId]: !prev[questionId],
    }));
  };

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7] dark:bg-[#000000]">
        <div className="flex flex-col items-center gap-3">
          <div className="w-7 h-7 border-2 border-[#0071e3] border-t-transparent rounded-full animate-spin" />
          <span className="text-sm font-medium text-[#86868b]">正在准备完整真题考卷与音频…</span>
        </div>
      </div>
    );
  }

  if (isError || !paper) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7] dark:bg-[#000000] p-6 text-center">
        <div className="flex flex-col items-center gap-3 max-w-sm">
          <p className="text-sm font-medium text-[#86868b]">未找到该套完整真题或网络异常</p>
          <Link
            href="/"
            className="px-5 py-2 text-xs font-semibold rounded-full bg-[#1d1d1f] dark:bg-[#f5f5f7] text-white dark:text-[#1d1d1f] transition-opacity"
          >
            返回首页
          </Link>
        </div>
      </div>
    );
  }

  const answeredCount = Object.values(selectedAnswers).filter(Boolean).length;
  const audioSrc = api.getAudioUrl(paper.audio_file);
  const downloadUrl = `${api.getAudioUrl(paper.audio_file)}?download=1`;

  return (
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] flex flex-col justify-between">
      {/* Top Header */}
      <header className="sticky top-0 z-40 bg-[#f5f5f7]/85 dark:bg-[#000000]/85 backdrop-blur-md border-b border-black/[0.04] dark:border-white/[0.06] px-4 sm:px-8 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between gap-3">
          <div className="flex items-center gap-2 sm:gap-3 min-w-0">
            <Link
              href="/"
              className="flex items-center gap-0.5 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] p-1 -ml-1 rounded-full transition-colors active:scale-95"
            >
              <ChevronLeft className="w-4 h-4" />
              <span>首页</span>
            </Link>
            <span className="text-black/10 dark:text-white/10">·</span>
            <div className="flex items-center gap-2 truncate">
              <h1 className="text-xs sm:text-sm font-semibold truncate">
                {paper.title_zh}
              </h1>
              <span className="hidden sm:inline-flex px-2 py-0.5 text-[11px] font-semibold rounded-full bg-[#0071e3]/10 text-[#0071e3] dark:bg-[#0a84ff]/20 dark:text-[#0a84ff]">
                官方模考
              </span>
            </div>
          </div>

          {/* Right Action Tools */}
          <div className="flex items-center gap-2 shrink-0">
            <Link
              href={`/studio?exam_id=${paper.id}`}
              className="hidden sm:inline-flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] bg-black/[0.04] dark:bg-white/[0.06] transition-colors"
              title="前往精听切片工作室"
            >
              <Headphones className="w-3.5 h-3.5" />
              <span>切片精听</span>
            </Link>

            <a
              href={downloadUrl}
              download
              className="inline-flex items-center gap-1 px-3.5 py-1.5 rounded-full text-xs font-semibold bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] shadow-xs active:scale-95 transition-all"
              title="下载完整音频 MP3"
            >
              <Download className="w-3.5 h-3.5" />
              <span>下载音频</span>
            </a>
          </div>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="flex-1 w-full max-w-4xl mx-auto px-4 sm:px-8 py-6 pb-36 space-y-8">
        {/* Exam Overview Banner */}
        <div className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl p-5 sm:p-6 shadow-xs">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
            <div>
              <div className="flex items-center gap-2">
                <span className="text-xs font-semibold text-[#0071e3] dark:text-[#0a84ff]">
                  完整真题卷模考
                </span>
                <span className="text-black/10 dark:text-white/10">·</span>
                <span className="text-xs text-[#86868b]">官方全真听力原音</span>
              </div>
              <h2 className="text-lg sm:text-xl font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] mt-1">
                {paper.title_zh}
              </h2>
              <p className="text-xs text-[#86868b] mt-1">
                整套音频包含标准考试停顿与指令 · 共 25 道全真选择题 · 已作答 {answeredCount} / 25 题
              </p>
            </div>

            <div className="flex items-center gap-2 self-start sm:self-auto">
              <span className="px-3 py-1 rounded-full text-xs font-mono font-medium bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b]">
                音频时长：{Math.floor(paper.duration_sec / 60)}分{Math.floor(paper.duration_sec % 60)}秒
              </span>
            </div>
          </div>
        </div>

        {/* Sections and Questions */}
        <div className="space-y-10">
          {paper.sections.map((sec, secIdx) => (
            <section key={sec.id || secIdx} className="space-y-4">
              <div className="border-b border-black/[0.06] dark:border-white/[0.08] pb-2">
                <h3 className="text-base font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                  {sec.title}
                </h3>
              </div>

              {/* Subparts within Section */}
              <div className="space-y-6">
                {sec.subparts.map((sp) => (
                  <div key={sp.id} className="space-y-4">
                    {/* Subpart Title Tag */}
                    <div className="flex items-center gap-2">
                      <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-[#0071e3]/10 text-[#0071e3] dark:bg-[#0a84ff]/15 dark:text-[#0a84ff]">
                        {sp.question_range || "题目"}
                      </span>
                      <span className="text-xs font-medium text-[#86868b]">
                        {sp.title}
                      </span>
                    </div>

                    {/* Question Cards */}
                    <div className="grid grid-cols-1 gap-4">
                      {sp.questions.map((q) => {
                        const userChoice = selectedAnswers[q.id];
                        const isExpanded = showExplanations[q.id];

                        return (
                          <div
                            key={q.id}
                            className="bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-2xl p-4 sm:p-5 shadow-xs space-y-3"
                          >
                            {/* Question Header & Prompt */}
                            <div className="flex items-start gap-2.5">
                              <span className="w-6 h-6 rounded-full bg-black/[0.05] dark:bg-white/[0.08] text-xs font-semibold flex items-center justify-center shrink-0 mt-0.5">
                                {q.question_num}
                              </span>
                              <p className="text-sm font-medium leading-relaxed text-[#1d1d1f] dark:text-[#f5f5f7]">
                                {q.prompt}
                              </p>
                            </div>

                            {/* 4 Options (A, B, C, D) */}
                            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 pl-0 sm:pl-8">
                              {(["A", "B", "C", "D"] as const).map((optKey) => {
                                const optText = q.options[optKey];
                                if (!optText) return null;
                                const isSelected = userChoice === optKey;

                                return (
                                  <button
                                    key={optKey}
                                    type="button"
                                    onClick={() => handleSelectOption(q.id, optKey)}
                                    className={`w-full flex items-start gap-2 p-2.5 rounded-xl text-left text-xs transition-all active:scale-[0.99] border ${
                                      isSelected
                                        ? "border-[#0071e3] bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] font-medium shadow-xs"
                                        : "border-black/[0.05] dark:border-white/[0.06] hover:bg-black/[0.02] dark:hover:bg-white/[0.04] text-[#1d1d1f] dark:text-[#f5f5f7]"
                                    }`}
                                  >
                                    <span
                                      className={`w-5 h-5 rounded-full text-[11px] font-semibold flex items-center justify-center shrink-0 border ${
                                        isSelected
                                          ? "border-[#0071e3] bg-[#0071e3] text-white"
                                          : "border-black/20 dark:border-white/20 text-[#86868b]"
                                      }`}
                                    >
                                      {optKey}
                                    </span>
                                    <span className="leading-relaxed mt-0.5">
                                      {optText}
                                    </span>
                                  </button>
                                );
                              })}
                            </div>

                            {/* Explanation Toggle */}
                            <div className="pl-0 sm:pl-8 pt-1">
                              <button
                                type="button"
                                onClick={() => toggleExplanation(q.id)}
                                className="inline-flex items-center gap-1 text-[11px] text-[#86868b] hover:text-[#0071e3] dark:hover:text-[#0a84ff] transition-colors"
                              >
                                <span>{isExpanded ? "收起答案解析" : "查看参考答案与解析"}</span>
                                {isExpanded ? (
                                  <ChevronUp className="w-3.5 h-3.5" />
                                ) : (
                                  <ChevronDown className="w-3.5 h-3.5" />
                                )}
                              </button>

                              {isExpanded && (
                                <div className="mt-2 p-3 bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.06] rounded-xl text-xs space-y-1.5 animate-in fade-in duration-150">
                                  <div className="flex items-center gap-2">
                                    <span className="font-semibold text-[#34c759] flex items-center gap-1">
                                      <CheckCircle2 className="w-3.5 h-3.5" />
                                      正确答案：{q.correct_answer}
                                    </span>
                                  </div>
                                  {q.explanation && (
                                    <p className="text-[#86868b] dark:text-[#a1a1a6] leading-relaxed">
                                      {q.explanation}
                                    </p>
                                  )}
                                </div>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </section>
          ))}
        </div>

        {/* Minimal Copyright / Learning Note */}
        <div className="pt-6 border-t border-black/[0.04] dark:border-white/[0.06] text-center">
          <p className="text-[11px] text-[#86868b]">
            六级听力真题音频与试卷仅供个人学习与模考检测使用
          </p>
        </div>
      </main>

      {/* Floating Bottom Decoupled Audio Player */}
      <footer className="fixed bottom-0 inset-x-0 pb-[max(1.25rem,calc(env(safe-area-inset-bottom)+0.6rem))] pt-1 px-3 sm:px-4 z-40">
        <FullAudioBar
          audioSrc={audioSrc}
          downloadUrl={downloadUrl}
          title={paper.title_zh}
          defaultDuration={paper.duration_sec}
        />
      </footer>
    </div>
  );
}

export default function FullPaperPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7] dark:bg-[#000000]">
          <div className="flex flex-col items-center gap-3">
            <div className="w-7 h-7 border-2 border-[#0071e3] border-t-transparent rounded-full animate-spin" />
            <span className="text-sm font-medium text-[#86868b]">正在准备模考考场…</span>
          </div>
        </div>
      }
    >
      <FullPaperContent />
    </Suspense>
  );
}
