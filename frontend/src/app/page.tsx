"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { ArrowRight, BookOpen, Headphones, Clock, Layers, Calendar, User as UserIcon, LogIn, Play, Download, FileText } from "lucide-react";
import { api, ResumeState, Subpart, ExamItem, StatsData, FullPaperItem } from "@/lib/api";
import { formatExamTitleZh, formatSubpartTitleZh } from "@/lib/formatters";
import { useAuth } from "@/hooks/useAuth";
import { CheckinDataPanel } from "@/components/checkin/CheckinDataPanel";

export default function HomePage() {
  const { user, isLoggedIn, logout } = useAuth();
  const [stats, setStats] = useState<StatsData | null>(null);
  const [resume, setResume] = useState<ResumeState | null>(null);
  const [exams, setExams] = useState<ExamItem[]>([]);
  const [fullPapers, setFullPapers] = useState<FullPaperItem[]>([]);
  const [selectedExamId, setSelectedExamId] = useState<string>("2026-06-set1");
  const [subparts, setSubparts] = useState<Subpart[]>([]);
  const [isLoadingSubparts, setIsLoadingSubparts] = useState(false);

  // Synchronously load cached stats & resume on client mount to prevent "flash of 0"
  useEffect(() => {
    try {
      const cachedStats = localStorage.getItem("stone_cached_stats");
      if (cachedStats) setStats(JSON.parse(cachedStats));
      const cachedResume = localStorage.getItem("stone_cached_resume");
      if (cachedResume) setResume(JSON.parse(cachedResume));
    } catch {}
  }, []);

  useEffect(() => {
    async function load() {
      try {
        const [resResume, resStats, resExams, resFullPapers] = await Promise.all([
          api.getResume().catch(() => null),
          api.getStats().catch(() => null),
          api.getExams().catch(() => []),
          api.getFullPapers().catch(() => []),
        ]);
        if (resResume) {
          setResume(resResume);
          try {
            localStorage.setItem("stone_cached_resume", JSON.stringify(resResume));
          } catch {}
        }
        if (resStats) {
          setStats(resStats);
          try {
            localStorage.setItem("stone_cached_stats", JSON.stringify(resStats));
          } catch {}
        }
        setExams(resExams);
        setFullPapers(resFullPapers);

        const latestExamId = resExams.length > 0 ? resExams[0].id : "2026-06-set1";
        const initialExamId = resResume?.exam_id || latestExamId;
        setSelectedExamId(initialExamId);

        const resSubparts = await api.getSubparts(initialExamId).catch(() => []);
        setSubparts(resSubparts);
      } catch (e) {
        console.error(e);
      }
    }
    load();
  }, [user]);

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
  const selectedYear = currentExam?.year || (availableYears.length > 0 ? availableYears[0] : 2026);
  const examsInSelectedYear = exams.filter((e) => e.year === selectedYear);

  const sections = [
    { id: "sec-a", suffix: "sec-a", title: "第一部分：长对话（第1–8题）", count: "2 篇 · 8 题" },
    { id: "sec-b", suffix: "sec-b", title: "第二部分：听力篇章（第9–15题）", count: "2 篇 · 7 题" },
    { id: "sec-c", suffix: "sec-c", title: "第三部分：讲座与报道（第16–25题）", count: "3 篇 · 10 题" },
  ];

  const hasProgress = Boolean(
    resume && (resume.sentence_index > 0 || resume.has_progress) && !resume.is_completed
  );
  const nextSentenceNum = (resume?.sentence_index ?? 0) + 1;

  return (
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] flex flex-col justify-between p-4 sm:p-12 pt-[max(0.85rem,env(safe-area-inset-top))] pb-[max(2rem,env(safe-area-inset-bottom))] select-none">
      {/* Top Header */}
      <header className="w-full max-w-4xl mx-auto flex items-center justify-between gap-2">
        <div className="flex items-center gap-2">
          <span className="text-base sm:text-lg font-bold tracking-tight text-[#0071e3] dark:text-[#0a84ff]">
            石头听力
          </span>
          <span className="text-black/10 dark:text-white/10 hidden xs:inline">·</span>
          <span className="text-xs text-[#86868b] dark:text-[#a1a1a6] hidden xs:inline">六级真题精听</span>
        </div>

        <div className="flex items-center gap-2 sm:gap-3">
          <Link
            href="/vocabulary"
            className="text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] flex items-center gap-1.5 px-3 py-1.5 rounded-full hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all"
          >
            <BookOpen className="w-3.5 h-3.5" /> 生词本 ({stats ? stats.vocab_count : "—"})
          </Link>

          {isLoggedIn ? (
            <div className="flex items-center gap-2 pl-2 border-l border-black/[0.08] dark:border-white/[0.1]">
              {user?.is_admin && (
                <Link
                  href="/admin"
                  className="text-[11px] font-semibold px-2 py-0.5 rounded-full bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] hover:bg-[#0071e3]/20 transition-all"
                  title="查看运营数据大盘"
                >
                  后台看板
                </Link>
              )}
              <span className="text-xs font-medium text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-1">
                <UserIcon className="w-3.5 h-3.5 text-[#0071e3]" /> {user?.username}
              </span>
              <button
                onClick={logout}
                className="text-[11px] text-[#86868b] hover:text-[#ff3b30] p-1 transition-colors"
                title="退出当前登录"
              >
                退出
              </button>
            </div>
          ) : (
            <Link
              href="/login"
              className="text-xs font-medium px-3.5 py-1.5 rounded-full bg-[#0071e3] hover:bg-[#0077ed] text-white flex items-center gap-1 shadow-sm active:scale-95 transition-all"
            >
              <LogIn className="w-3.5 h-3.5" /> 登录
            </Link>
          )}
        </div>
      </header>

      {/* Main Container */}
      <main className="w-full max-w-4xl mx-auto py-5 sm:py-8 flex flex-col gap-6 sm:gap-8">
        {/* Apple Minimalist Check-in & Listening Data Panel */}
        <CheckinDataPanel stats={stats} onStatsUpdate={setStats} />

        {/* Hero Card: Primary Call to Action 「继续第 N 句」 / 「先听一句」 */}
        <div className="p-5 sm:p-7 bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl shadow-[0_4px_24px_rgba(0,0,0,0.04)] flex flex-col sm:flex-row sm:items-center justify-between gap-5 hover:shadow-[0_8px_32px_rgba(0,0,0,0.08)] transition-all">
          <div className="flex items-start gap-3.5 sm:gap-4">
            <div className="w-11 h-11 sm:w-12 sm:h-12 rounded-2xl bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] flex items-center justify-center shrink-0">
              <Headphones className="w-5 h-5 sm:w-6 sm:h-6" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-[11px] font-semibold text-[#0071e3] dark:text-[#0a84ff]">
                  {hasProgress ? "继续精听" : "推荐首练 · 最新真题"}
                </span>
                <span className="text-black/10 dark:text-white/10">·</span>
                <span className="text-xs text-[#86868b]">
                  第 {hasProgress ? nextSentenceNum : 1} 句
                </span>
              </div>
              <h2 className="text-base sm:text-lg font-medium text-[#1d1d1f] dark:text-[#f5f5f7] mt-1">
                {formatExamTitleZh(currentExam?.title || selectedExamId)}
              </h2>
              <p className="text-xs text-[#86868b] mt-0.5">
                {subparts[0] ? formatSubpartTitleZh(subparts[0].title, subparts[0].question_range) : "双语对照精听"} · 沉浸单句精听
              </p>
            </div>
          </div>

          <Link
            href={
              resume?.subpart_id
                ? `/studio?exam_id=${resume.exam_id}&subpart_id=${resume.subpart_id}&autoplay=1`
                : `/studio?exam_id=${selectedExamId}&subpart_id=${subparts[0]?.id || ""}&autoplay=1`
            }
            className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] text-xs font-semibold rounded-full shadow-sm transition-transform active:scale-95"
          >
            <Play className="w-3.5 h-3.5 fill-current ml-0.5" />
            <span>{hasProgress ? `继续第 ${nextSentenceNum} 句` : "先听一句"}</span>
          </Link>
        </div>

        {/* Exam Navigation & Year Filter */}
        <div className="p-5 sm:p-6 bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl space-y-4">
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 sm:gap-3">
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

          {/* Year Pills: Swipeable horizontal track */}
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar py-1">
            {availableYears.map((yr) => {
              const isSelectedYear = yr === selectedYear;
              return (
                <button
                  key={yr}
                  onClick={() => {
                    const firstInYear = exams.find((e) => e.year === yr);
                    if (firstInYear) handleSelectExam(firstInYear.id);
                  }}
                  className={`shrink-0 px-3.5 py-1.5 rounded-full text-xs font-medium transition-all active:scale-95 ${
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
          <div className="flex items-center gap-2 overflow-x-auto no-scrollbar pt-3 border-t border-black/[0.04] dark:border-white/[0.06]">
            <span className="text-xs text-[#86868b] shrink-0">考卷：</span>
            {examsInSelectedYear.map((e) => {
              const isSelected = e.id === selectedExamId;
              const setZh = formatExamTitleZh(e.title || e.id);
              return (
                <button
                  key={e.id}
                  onClick={() => handleSelectExam(e.id)}
                  className={`shrink-0 px-3.5 py-1.5 rounded-full text-xs font-medium transition-all border active:scale-95 ${
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

        {/* Full Paper Simulation Section (Controlled by Year & Exam Selector) */}
        {fullPapers.length > 0 && (
          <div className="space-y-4 pt-4 border-t border-black/[0.04] dark:border-white/[0.06]">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1 sm:gap-4">
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4 text-[#0071e3] dark:text-[#0a84ff]" />
                <h2 className="text-sm font-semibold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                  完整卷
                </h2>
              </div>
              <span className="text-xs text-[#86868b]">
                整段播放 · 可下载 · 适合模考检测（{selectedYear} 年 · 共 {fullPapers.filter((fp) => fp.year === selectedYear).length} 套）
              </span>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              {(fullPapers.filter((fp) => fp.year === selectedYear).length > 0
                ? fullPapers.filter((fp) => fp.year === selectedYear)
                : fullPapers
              ).map((fp) => {
                const durationMin = Math.floor(fp.duration_sec / 60);
                const durationSec = Math.floor(fp.duration_sec % 60);
                const isCurrentExam = fp.id === selectedExamId;

                return (
                  <div
                    key={fp.id}
                    onClick={() => handleSelectExam(fp.id)}
                    className={`cursor-pointer flex flex-col justify-between p-4 sm:p-5 rounded-2xl bg-white dark:bg-[#1c1c1e] border transition-all ${
                      isCurrentExam
                        ? "border-[#0071e3] ring-1 ring-[#0071e3]/30 shadow-[0_4px_20px_rgba(0,113,227,0.1)]"
                        : "border-black/[0.06] dark:border-white/[0.08] hover:border-[#0071e3]/40 hover:shadow-[0_4px_16px_rgba(0,113,227,0.06)]"
                    }`}
                  >
                    <div>
                      <div className="flex items-center justify-between gap-2">
                        <span
                          className={`px-2.5 py-0.5 text-[10px] font-semibold rounded-full ${
                            isCurrentExam
                              ? "bg-[#0071e3] text-white"
                              : "bg-[#0071e3]/10 text-[#0071e3] dark:bg-[#0a84ff]/15 dark:text-[#0a84ff]"
                          }`}
                        >
                          {isCurrentExam ? "当前选中 · 25题" : "全真模考 · 25题"}
                        </span>
                        <span className="text-[11px] text-[#86868b] flex items-center gap-1 font-mono">
                          <Clock className="w-3 h-3" /> {durationMin}分{durationSec}秒
                        </span>
                      </div>

                      <h3 className="text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] mt-2.5">
                        {fp.title_zh}
                      </h3>
                      <p className="text-xs text-[#86868b] mt-1">
                        官方原版整段录音 · 包含全套 Section A/B/C
                      </p>
                    </div>

                    <div
                      className="mt-4 pt-3 border-t border-black/[0.04] dark:border-white/[0.06] flex items-center justify-between gap-2"
                      onClick={(e) => e.stopPropagation()}
                    >
                      <a
                        href={fp.download_url}
                        download
                        className="inline-flex items-center gap-1 px-3 py-1.5 rounded-full text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] bg-black/[0.03] dark:bg-white/[0.05] hover:bg-black/[0.06] transition-all"
                        title="下载本套完整 MP3 音频"
                      >
                        <Download className="w-3 h-3" />
                        <span>下载音频</span>
                      </a>

                      <Link
                        href={`/full-paper?id=${fp.id}`}
                        className="inline-flex items-center gap-1 px-4 py-1.5 rounded-full text-xs font-semibold bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] shadow-xs active:scale-95 transition-all"
                      >
                        <span>进入模考</span>
                        <ArrowRight className="w-3 h-3" />
                      </Link>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
