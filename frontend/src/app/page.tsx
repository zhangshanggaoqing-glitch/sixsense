"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight, BookOpen, Flame, Headphones, Clock, Layers, Calendar } from "lucide-react";
import { api, ResumeState, Subpart, ExamItem } from "@/lib/api";

export default function HomePage() {
  const [stats, setStats] = useState({
    today_minutes: 18.0,
    this_week_minutes: 96.0,
    streak_days: 5,
    vocab_count: 0,
    dictation_count: 0,
  });
  const [resume, setResume] = useState<ResumeState | null>(null);
  const [exams, setExams] = useState<ExamItem[]>([]);
  const [selectedExamId, setSelectedExamId] = useState<string>("2024-06-set1");
  const [subparts, setSubparts] = useState<Subpart[]>([]);
  const [greeting, setGreeting] = useState("Good evening");
  const [isLoadingSubparts, setIsLoadingSubparts] = useState(false);

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting("Good morning");
    else if (hour < 18) setGreeting("Good afternoon");
    else setGreeting("Good evening");

    async function load() {
      try {
        const [resResume, resStats, resExams] = await Promise.all([
          api.getResume(),
          api.getStats().catch(() => null),
          api.getExams().catch(() => []),
        ]);
        setResume(resResume);
        if (resStats) setStats(resStats);
        setExams(resExams);

        const initialExamId = resResume?.exam_id || (resExams.length > 0 ? resExams[0].id : "2020-07-set1");
        setSelectedExamId(initialExamId);

        const resSubparts = await api.getSubparts(initialExamId).catch(() => []);
        setSubparts(resSubparts);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, []);

  const handleSelectExam = async (examId: string) => {
    setSelectedExamId(examId);
    setIsLoadingSubparts(true);
    try {
      const sps = await api.getSubparts(examId);
      setSubparts(sps);
    } catch (e) {
      console.error(e);
    } finally {
      setIsLoadingSubparts(false);
    }
  };

  const formatDuration = (sec?: number) => {
    if (!sec) return "0:00";
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}m ${s}s`;
  };

  const availableYears = Array.from(new Set(exams.map((e) => e.year))).sort((a, b) => b - a);
  const currentExam = exams.find((e) => e.id === selectedExamId) || exams[0];
  const selectedYear = currentExam?.year || (availableYears.length > 0 ? availableYears[0] : 2024);
  const examsInSelectedYear = exams.filter((e) => e.year === selectedYear);

  const sections = [
    { id: "sec-a", suffix: "sec-a", title: "Section A: 长对话 (Conversations)", count: "2 篇 · 8 题" },
    { id: "sec-b", suffix: "sec-b", title: "Section B: 听力篇章 (Passages)", count: "2 篇 · 7 题" },
    { id: "sec-c", suffix: "sec-c", title: "Section C: 讲座 / 讲话 (Talks & Lectures)", count: "3 篇 · 10 题" },
  ];

  return (
    <div className="min-h-screen bg-[#fbfbfd] dark:bg-[#0d0f14] text-gray-900 dark:text-gray-100 flex flex-col justify-between p-6 sm:p-12">
      {/* Top Header */}
      <header className="w-full max-w-4xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="font-mono text-sm font-bold tracking-widest uppercase text-blue-600 dark:text-blue-400">
            SixSense
          </span>
          <span className="text-gray-300 dark:text-gray-700">/</span>
          <span className="text-xs font-mono text-gray-400">CET-6 Intensive Studio</span>
        </div>

        <Link
          href="/vocabulary"
          className="text-xs font-medium text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-transparent hover:border-gray-200 dark:hover:border-gray-800 transition-all"
        >
          <BookOpen className="w-3.5 h-3.5" /> Vocabulary ({stats.vocab_count})
        </Link>
      </header>

      {/* Main Container */}
      <main className="w-full max-w-4xl mx-auto py-8 flex flex-col gap-8">
        {/* Welcome & Stats Row */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
          <div>
            <h1 className="text-3xl sm:text-4xl font-light tracking-tight text-gray-900 dark:text-gray-50">
              {greeting}, Stone.
            </h1>
            <p className="text-xs sm:text-sm text-gray-400 mt-1.5 font-mono">
              全国大学英语六级历年全真听力 · 题型分类精听工作台
            </p>
          </div>

          {/* Quick Metrics */}
          <div className="flex items-center gap-6 pt-2 sm:pt-0 border-t sm:border-t-0 border-gray-100 dark:border-gray-800">
            <div>
              <span className="text-[11px] text-gray-400">Today</span>
              <p className="text-sm font-mono font-semibold text-gray-800 dark:text-gray-200">
                {stats.today_minutes} min
              </p>
            </div>
            <div>
              <span className="text-[11px] text-gray-400">This Week</span>
              <p className="text-sm font-mono font-semibold text-gray-800 dark:text-gray-200">
                {stats.this_week_minutes} min
              </p>
            </div>
            <div>
              <span className="text-[11px] text-gray-400">Streak</span>
              <p className="text-sm font-mono font-semibold text-orange-500 flex items-center gap-1">
                <Flame className="w-3.5 h-3.5 fill-orange-500" /> {stats.streak_days}d
              </p>
            </div>
          </div>
        </div>

        {/* Continue Listening Hero Card */}
        {resume && (
          <div className="p-6 sm:p-7 bg-white dark:bg-[#151821] border border-gray-200/80 dark:border-gray-800/80 rounded-3xl shadow-xs flex flex-col sm:flex-row sm:items-center justify-between gap-6 hover:border-gray-300 dark:hover:border-gray-700 transition-colors">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-2xl bg-blue-50 dark:bg-blue-950/60 flex items-center justify-center text-blue-600 dark:text-blue-400 flex-shrink-0">
                <Headphones className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] uppercase font-mono font-bold tracking-wider text-blue-600 dark:text-blue-400">
                    Resume Listening
                  </span>
                  <span className="text-gray-300 dark:text-gray-700">·</span>
                  <span className="text-xs text-gray-400 font-mono">
                    Sentence #{ (resume.sentence_index ?? 0) + 1 }
                  </span>
                </div>
                <h2 className="text-lg font-medium text-gray-900 dark:text-gray-100 mt-1">
                  {currentExam?.title || "CET-6 Intensive Studio"}
                </h2>
                <p className="text-xs text-gray-400 font-mono mt-0.5">
                  Mode: {resume.display_mode === "C" ? "Blind" : resume.display_mode === "B" ? "English" : resume.display_mode === "A" ? "Bilingual" : "Dictation"} · Speed {resume.playback_rate}x
                </p>
              </div>
            </div>

            <Link
              href={resume.subpart_id ? `/studio?exam_id=${resume.exam_id}&subpart_id=${resume.subpart_id}` : `/studio?exam_id=${selectedExamId}`}
              className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-gray-900 hover:bg-gray-800 dark:bg-white dark:hover:bg-gray-100 text-white dark:text-gray-900 text-xs font-semibold rounded-2xl shadow-xs transition-transform active:scale-98"
            >
              Continue Listening <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        )}

        {/* Exam Navigation & Year Filter */}
        <div className="p-6 bg-white dark:bg-[#151821] border border-gray-200/80 dark:border-gray-800/80 rounded-3xl space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-blue-600 dark:text-blue-400" />
              <h2 className="text-sm font-semibold text-gray-900 dark:text-gray-100">
                真题年份与套数选择 (Exam Selection)
              </h2>
            </div>
            <span className="text-xs text-gray-400 font-mono">
              当前: {currentExam?.title}
            </span>
          </div>

          {/* Year Pills */}
          <div className="flex items-center gap-2 flex-wrap pt-1">
            {availableYears.map((yr) => {
              const isSelectedYear = yr === selectedYear;
              return (
                <button
                  key={yr}
                  onClick={() => {
                    const firstInYear = exams.find((e) => e.year === yr);
                    if (firstInYear) handleSelectExam(firstInYear.id);
                  }}
                  className={`px-3.5 py-1.5 rounded-xl text-xs font-mono font-medium transition-all ${
                    isSelectedYear
                      ? "bg-blue-600 text-white shadow-xs"
                      : "bg-gray-100 dark:bg-gray-800/80 text-gray-600 dark:text-gray-400 hover:bg-gray-200 dark:hover:bg-gray-700"
                  }`}
                >
                  {yr} 年
                </button>
              );
            })}
          </div>

          {/* Sets within selected year */}
          <div className="flex items-center gap-2.5 flex-wrap pt-2 border-t border-gray-100 dark:border-gray-800/80">
            <span className="text-xs text-gray-400 font-mono">考卷套数:</span>
            {examsInSelectedYear.map((e) => {
              const isSelected = e.id === selectedExamId;
              return (
                <button
                  key={e.id}
                  onClick={() => handleSelectExam(e.id)}
                  className={`px-3 py-1 rounded-xl text-xs font-mono font-medium transition-all border ${
                    isSelected
                      ? "border-blue-500 bg-blue-50/50 dark:bg-blue-950/30 text-blue-600 dark:text-blue-400"
                      : "border-gray-200 dark:border-gray-800 bg-white dark:bg-[#12141c] text-gray-600 dark:text-gray-400 hover:border-gray-300 dark:hover:border-gray-700"
                  }`}
                >
                  {e.month}月 · 第{e.set_number}套
                </button>
              );
            })}
          </div>
        </div>

        {/* Section & Topic Categorization */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-gray-400" />
              <h2 className="text-sm font-semibold tracking-tight text-gray-900 dark:text-gray-100">
                本套题型专题 (Topic Units)
              </h2>
            </div>
            <span className="text-xs text-gray-400 font-mono">
              {isLoadingSubparts ? "加载中..." : `${subparts.length} 篇独立篇章 · 25 道考题`}
            </span>
          </div>

          {/* Section Grid */}
          <div className="space-y-6">
            {sections.map((sec) => {
              const secSubparts = subparts.filter((sp) => {
                const sid = (sp.section_id || "").toLowerCase();
                const stype = (sp.type || "").toLowerCase();
                if (sec.id === "sec-a") return sid.endsWith("sec-a") || sid.endsWith("section-a") || stype === "conversation";
                if (sec.id === "sec-b") return sid.endsWith("sec-b") || sid.endsWith("section-b") || stype === "passage";
                if (sec.id === "sec-c") return sid.endsWith("sec-c") || sid.endsWith("section-c") || stype === "recording";
                return false;
              });
              if (secSubparts.length === 0) return null;

              return (
                <div key={sec.id} className="space-y-3">
                  <div className="flex items-center justify-between px-1">
                    <span className="text-xs font-mono font-bold tracking-wide text-gray-500 dark:text-gray-400 uppercase">
                      {sec.title}
                    </span>
                    <span className="text-[11px] text-gray-400 font-mono">{sec.count}</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
                    {secSubparts.map((sp) => (
                      <Link
                        key={sp.id}
                        href={`/studio?exam_id=${selectedExamId}&subpart_id=${sp.id}`}
                        className="group flex flex-col justify-between p-4 rounded-2xl bg-white dark:bg-[#151821] border border-gray-200/80 dark:border-gray-800/80 hover:border-blue-500 dark:hover:border-blue-500 hover:shadow-xs transition-all"
                      >
                        <div>
                          <div className="flex items-center justify-between">
                            <span className="px-2 py-0.5 text-[10px] font-mono font-bold uppercase rounded-md bg-gray-100 dark:bg-gray-800 text-gray-600 dark:text-gray-300 group-hover:bg-blue-50 group-hover:text-blue-600 dark:group-hover:bg-blue-950/60 dark:group-hover:text-blue-400 transition-colors">
                              {sp.question_range}
                            </span>
                            <span className="text-[11px] font-mono text-gray-400 flex items-center gap-1">
                              <Clock className="w-3 h-3" /> {formatDuration(sp.duration)}
                            </span>
                          </div>

                          <h3 className="text-sm font-medium text-gray-900 dark:text-gray-100 mt-2.5 leading-snug group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">
                            {sp.topic_zh || sp.title}
                          </h3>
                        </div>

                        <div className="mt-4 pt-3 border-t border-gray-100 dark:border-gray-800/80 flex items-center justify-between text-xs text-gray-400">
                          <span className="font-mono text-[11px]">{sp.sentence_count} 句精听</span>
                          <span className="font-medium text-blue-600 dark:text-blue-400 group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
                            开始 <ArrowRight className="w-3 h-3" />
                          </span>
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full max-w-4xl mx-auto text-center text-xs text-gray-400 font-mono py-4 border-t border-gray-100 dark:border-gray-800/80 mt-12">
        SixSense · Focused CET-6 Intensive Listening Workstation · One Sentence, One Job
      </footer>
    </div>
  );
}
