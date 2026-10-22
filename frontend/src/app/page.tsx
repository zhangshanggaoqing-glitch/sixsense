"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight, BookOpen, Flame, Headphones, Clock, Layers, Calendar } from "lucide-react";
import { api, ResumeState, Subpart, ExamItem } from "@/lib/api";
import { formatExamTitleZh, formatSubpartTitleZh } from "@/lib/formatters";

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
  const [selectedExamId, setSelectedExamId] = useState<string>("2016-06-set1");
  const [subparts, setSubparts] = useState<Subpart[]>([]);
  const [greeting, setGreeting] = useState("晚上好");
  const [isLoadingSubparts, setIsLoadingSubparts] = useState(false);

  useEffect(() => {
    const hour = new Date().getHours();
    if (hour < 12) setGreeting("早上好");
    else if (hour < 18) setGreeting("下午好");
    else setGreeting("晚上好");

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

        const initialExamId = resResume?.exam_id || (resExams.length > 0 ? resExams[0].id : "2016-06-set1");
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
    if (!sec) return "0分0秒";
    const m = Math.floor(sec / 60);
    const s = Math.floor(sec % 60);
    return `${m}分${s}秒`;
  };

  const availableYears = Array.from(new Set(exams.map((e) => e.year))).sort((a, b) => b - a);
  const currentExam = exams.find((e) => e.id === selectedExamId) || exams[0];
  const selectedYear = currentExam?.year || (availableYears.length > 0 ? availableYears[0] : 2016);
  const examsInSelectedYear = exams.filter((e) => e.year === selectedYear);

  const sections = [
    { id: "sec-a", suffix: "sec-a", title: "第一部分：长对话（第1–8题）", count: "2 篇 · 8 题" },
    { id: "sec-b", suffix: "sec-b", title: "第二部分：听力篇章（第9–15题）", count: "2 篇 · 7 题" },
    { id: "sec-c", suffix: "sec-c", title: "第三部分：讲座与报道（第16–25题）", count: "3 篇 · 10 题" },
  ];

  return (
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] flex flex-col justify-between p-6 sm:p-12 select-none">
      {/* Top Header */}
      <header className="w-full max-w-4xl mx-auto flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <span className="text-base font-bold tracking-tight text-[#0071e3] dark:text-[#0a84ff]">
            石头听力
          </span>
          <span className="text-black/10 dark:text-white/10">·</span>
          <span className="text-xs text-[#86868b] dark:text-[#a1a1a6]">大学英语六级真题精听</span>
        </div>

        <Link
          href="/vocabulary"
          className="text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] flex items-center gap-1.5 px-3 py-1.5 rounded-full hover:bg-black/5 dark:hover:bg-white/10 transition-all"
        >
          <BookOpen className="w-3.5 h-3.5" /> 生词本 ({stats.vocab_count})
        </Link>
      </header>

      {/* Main Container */}
      <main className="w-full max-w-4xl mx-auto py-8 flex flex-col gap-8">
        {/* Welcome & Stats Row */}
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-6">
          <div>
            <h1 className="text-3xl sm:text-4xl font-semibold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
              {greeting}，同学
            </h1>
            <p className="text-xs sm:text-sm text-[#86868b] dark:text-[#a1a1a6] mt-1.5">
              全国大学英语六级历年官方全真听力 · 题型分类精听工作台
            </p>
          </div>

          {/* Quick Metrics */}
          <div className="flex items-center gap-6 pt-2 sm:pt-0 border-t sm:border-t-0 border-black/[0.06] dark:border-white/[0.08]">
            <div>
              <span className="text-[11px] text-[#86868b]">今日精听</span>
              <p className="text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                {stats.today_minutes} 分钟
              </p>
            </div>
            <div>
              <span className="text-[11px] text-[#86868b]">本周累计</span>
              <p className="text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                {stats.this_week_minutes} 分钟
              </p>
            </div>
            <div>
              <span className="text-[11px] text-[#86868b]">连续天数</span>
              <p className="text-sm font-semibold text-[#ff9500] flex items-center gap-1">
                <Flame className="w-3.5 h-3.5 fill-[#ff9500]" /> {stats.streak_days} 天
              </p>
            </div>
          </div>
        </div>

        {/* Continue Listening Hero Card */}
        {resume && (
          <div className="p-6 sm:p-7 bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl shadow-[0_4px_24px_rgba(0,0,0,0.04)] flex flex-col sm:flex-row sm:items-center justify-between gap-6 hover:shadow-[0_8px_32px_rgba(0,0,0,0.08)] transition-all">
            <div className="flex items-start gap-4">
              <div className="w-12 h-12 rounded-2xl bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] flex items-center justify-center shrink-0">
                <Headphones className="w-6 h-6" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-[11px] font-semibold text-[#0071e3] dark:text-[#0a84ff]">
                    继续精听
                  </span>
                  <span className="text-black/10 dark:text-white/10">·</span>
                  <span className="text-xs text-[#86868b]">
                    第 { (resume.sentence_index ?? 0) + 1 } 句
                  </span>
                </div>
                <h2 className="text-lg font-medium text-[#1d1d1f] dark:text-[#f5f5f7] mt-1">
                  {formatExamTitleZh(currentExam?.title || selectedExamId)}
                </h2>
                <p className="text-xs text-[#86868b] mt-0.5">
                  模式：{resume.display_mode === "C" ? "盲听" : resume.display_mode === "D" ? "听写" : "双语"} · 倍速 {resume.playback_rate}×
                </p>
              </div>
            </div>

            <Link
              href={resume.subpart_id ? `/studio?exam_id=${resume.exam_id}&subpart_id=${resume.subpart_id}` : `/studio?exam_id=${selectedExamId}`}
              className="inline-flex items-center justify-center gap-2 px-6 py-3 bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] text-xs font-semibold rounded-full shadow-sm transition-transform active:scale-95"
            >
              进入工作台 <ArrowRight className="w-4 h-4" />
            </Link>
          </div>
        )}

        {/* Exam Navigation & Year Filter */}
        <div className="p-6 bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-[#0071e3] dark:text-[#0a84ff]" />
              <h2 className="text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                真题年份与套数选择
              </h2>
            </div>
            <span className="text-xs text-[#86868b]">
              当前：{formatExamTitleZh(currentExam?.title || selectedExamId)}
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
                  className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all ${
                    isSelectedYear
                      ? "bg-[#0071e3] text-white shadow-xs"
                      : "bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
                  }`}
                >
                  {yr} 年
                </button>
              );
            })}
          </div>

          {/* Sets within selected year */}
          <div className="flex items-center gap-2.5 flex-wrap pt-3 border-t border-black/[0.04] dark:border-white/[0.06]">
            <span className="text-xs text-[#86868b]">考卷套数：</span>
            {examsInSelectedYear.map((e) => {
              const isSelected = e.id === selectedExamId;
              const setZh = formatExamTitleZh(e.title || e.id);
              return (
                <button
                  key={e.id}
                  onClick={() => handleSelectExam(e.id)}
                  className={`px-3.5 py-1.5 rounded-full text-xs font-medium transition-all border ${
                    isSelected
                      ? "border-[#0071e3] bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] font-semibold"
                      : "border-black/[0.06] dark:border-white/[0.08] bg-white dark:bg-[#1c1c1e] text-[#86868b] hover:border-black/20"
                  }`}
                >
                  {setZh}
                </button>
              );
            })}
          </div>
        </div>

        {/* Section & Topic Categorization */}
        <div>
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <Layers className="w-4 h-4 text-[#86868b]" />
              <h2 className="text-sm font-semibold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                题型专项切片
              </h2>
            </div>
            <span className="text-xs text-[#86868b]">
              {isLoadingSubparts ? "正在加载…" : `${subparts.length} 个独立题型 · 25 道全真考题`}
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
                    <span className="text-xs font-semibold text-[#86868b] dark:text-[#a1a1a6]">
                      {sec.title}
                    </span>
                    <span className="text-[11px] text-[#86868b]">{sec.count}</span>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3.5">
                    {secSubparts.map((sp) => (
                      <Link
                        key={sp.id}
                        href={`/studio?exam_id=${selectedExamId}&subpart_id=${sp.id}`}
                        className="group flex flex-col justify-between p-4 rounded-2xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] hover:border-[#0071e3] hover:shadow-[0_4px_16px_rgba(0,113,227,0.08)] transition-all"
                      >
                        <div>
                          <div className="flex items-center justify-between">
                            <span className="px-2 py-0.5 text-[10px] font-semibold rounded-full bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b] group-hover:bg-[#0071e3]/10 group-hover:text-[#0071e3] transition-colors">
                              {formatSubpartTitleZh(sp.title, sp.question_range)}
                            </span>
                            <span className="text-[11px] text-[#86868b] flex items-center gap-1">
                              <Clock className="w-3 h-3" /> {formatDuration(sp.duration)}
                            </span>
                          </div>

                          <h3 className="text-sm font-medium text-[#1d1d1f] dark:text-[#f5f5f7] mt-2.5 leading-snug group-hover:text-[#0071e3] dark:group-hover:text-[#0a84ff] transition-colors">
                            {sp.topic_zh || sp.title}
                          </h3>
                        </div>

                        <div className="mt-4 pt-3 border-t border-black/[0.04] dark:border-white/[0.06] flex items-center justify-between text-xs text-[#86868b]">
                          <span className="text-[11px]">{sp.sentence_count} 句精听</span>
                          <span className="font-medium text-[#0071e3] dark:text-[#0a84ff] group-hover:translate-x-0.5 transition-transform flex items-center gap-1">
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
      <footer className="w-full max-w-4xl mx-auto text-center text-xs text-[#86868b] py-6 border-t border-black/[0.06] dark:border-white/[0.08] mt-12">
        石头听力 · 极简专注的大学英语六级真题精听工作台 · 一屏一事
      </footer>
    </div>
  );
}
