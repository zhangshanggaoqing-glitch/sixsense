"use client";

import React, { useState, useMemo } from "react";
import { Flame, Check, Sparkles, Calendar as CalendarIcon } from "lucide-react";
import { StatsData, api } from "@/lib/api";
import { ShareCardModal } from "./ShareCardModal";

interface CheckinDataPanelProps {
  stats: StatsData | null;
  onStatsUpdate?: (newStats: StatsData) => void;
}

const MEDAL_NAMES: Record<string, string> = {
  first_listen: "首听",
  streak_3: "连续3天",
  streak_7: "连续7天",
};

/**
 * Returns current date object in Asia/Shanghai (CST, UTC+8)
 */
function getCstNow(): Date {
  const now = new Date();
  const utc = now.getTime() + now.getTimezoneOffset() * 60000;
  return new Date(utc + 3600000 * 8);
}

function formatDateKey(d: Date): string {
  const y = d.getFullYear();
  const m = String(d.getMonth() + 1).padStart(2, "0");
  const day = String(d.getDate()).padStart(2, "0");
  return `${y}-${m}-${day}`;
}

export function CheckinDataPanel({ stats, onStatsUpdate }: CheckinDataPanelProps) {
  const [isShareModalOpen, setIsShareModalOpen] = useState(false);
  const [isPunching, setIsPunching] = useState(false);
  const [punchFeedback, setPunchFeedback] = useState<string | null>(null);

  const cstNow = useMemo(() => getCstNow(), []);
  const todayStr = useMemo(() => formatDateKey(cstNow), [cstNow]);

  const todayMinutes = stats?.today_minutes ?? 0;
  const streakDays = stats?.streak_days ?? 0;
  const thisWeekMinutes = stats?.this_week_minutes ?? 0;
  const dailyHistory = useMemo(() => stats?.daily_history ?? {}, [stats?.daily_history]);

  // Eligibility: Today's active listening >= 1 minute (or already punched)
  const isPunchedToday = Boolean(stats?.today_punched || (dailyHistory[todayStr] ?? 0) >= 1.0);
  const canPunch = todayMinutes >= 1.0 || isPunchedToday;

  const earnedMedals = (stats?.medals || []).filter((m) => MEDAL_NAMES[m]);

  // Handle punch button click
  const handlePunchClick = async () => {
    if (isPunchedToday) {
      // Already punched today -> directly open share card
      setIsShareModalOpen(true);
      return;
    }

    if (!canPunch) {
      setPunchFeedback(`需精听满 1 分钟方可打卡（当前 ${todayMinutes.toFixed(1)} 分钟）`);
      setTimeout(() => setPunchFeedback(null), 3000);
      return;
    }

    setIsPunching(true);
    try {
      const res = await api.punch();
      if (res.ok) {
        if (onStatsUpdate && stats) {
          const updated: StatsData = {
            ...stats,
            today_minutes: res.today_minutes ?? todayMinutes,
            streak_days: res.streak_days ?? (streakDays || 1),
            today_punched: true,
            medals: res.medals || stats.medals,
            daily_history: {
              ...dailyHistory,
              [todayStr]: res.today_minutes ?? todayMinutes,
            },
          };
          onStatsUpdate(updated);
        }
        setIsShareModalOpen(true);
      } else {
        setPunchFeedback(res.message || "打卡未满足条件");
        setTimeout(() => setPunchFeedback(null), 3000);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : "打卡请求失败，请稍后重试";
      setPunchFeedback(msg);
      setTimeout(() => setPunchFeedback(null), 3000);
    } finally {
      setIsPunching(false);
    }
  };

  // 1. Mini Calendar Generation (Current Month in Asia/Shanghai)
  const calendarData = useMemo(() => {
    const year = cstNow.getFullYear();
    const month = cstNow.getMonth(); // 0-indexed
    const firstDayOfMonth = new Date(year, month, 1);
    const lastDayOfMonth = new Date(year, month + 1, 0);

    // Monday as first day of week: 0=Mon, 1=Tue, ..., 6=Sun
    let startDayOfWeek = firstDayOfMonth.getDay() - 1;
    if (startDayOfWeek === -1) startDayOfWeek = 6;

    const totalDays = lastDayOfMonth.getDate();
    const days: Array<{
      dayNum: number;
      dateKey: string;
      isToday: boolean;
      isPunched: boolean;
      minutes: number;
    }> = [];

    for (let d = 1; d <= totalDays; d++) {
      const dateKey = `${year}-${String(month + 1).padStart(2, "0")}-${String(d).padStart(2, "0")}`;
      const minutes = dailyHistory[dateKey] ?? 0;
      const isPunched = minutes >= 1.0;
      const isToday = d === cstNow.getDate();
      days.push({
        dayNum: d,
        dateKey,
        isToday,
        isPunched,
        minutes,
      });
    }

    return {
      monthLabel: `${year}年${month + 1}月`,
      startOffset: startDayOfWeek,
      days,
    };
  }, [cstNow, dailyHistory]);

  // 2. Heatmap Generation (Last 16 weeks ~ 112 days, Monday-Sunday columns)
  const heatmapData = useMemo(() => {
    // Current day of week (0=Mon ... 6=Sun)
    let currentDayOfWeek = cstNow.getDay() - 1;
    if (currentDayOfWeek === -1) currentDayOfWeek = 6;

    const numWeeks = 14;
    const totalDays = numWeeks * 7;
    // Calculate start date: (numWeeks - 1) weeks ago from the start of this week
    const daysToSubtract = (numWeeks - 1) * 7 + currentDayOfWeek;
    const startDate = new Date(cstNow.getTime() - daysToSubtract * 86400000);

    const weeks: Array<
      Array<{
        dateKey: string;
        minutes: number;
        isToday: boolean;
        level: number; // 0 to 4
      }>
    > = [];

    let currentWeek: Array<{
      dateKey: string;
      minutes: number;
      isToday: boolean;
      level: number;
    }> = [];

    for (let i = 0; i < totalDays; i++) {
      const d = new Date(startDate.getTime() + i * 86400000);
      const dateKey = formatDateKey(d);
      const minutes = dailyHistory[dateKey] ?? 0;
      const isToday = dateKey === todayStr;

      let level = 0;
      if (minutes >= 30) level = 4;
      else if (minutes >= 15) level = 3;
      else if (minutes >= 5) level = 2;
      else if (minutes >= 1) level = 1;

      currentWeek.push({
        dateKey,
        minutes,
        isToday,
        level,
      });

      if (currentWeek.length === 7) {
        weeks.push(currentWeek);
        currentWeek = [];
      }
    }
    if (currentWeek.length > 0) {
      weeks.push(currentWeek);
    }

    return weeks;
  }, [cstNow, dailyHistory, todayStr]);

  // Heatmap color mapper (Apple clean monochrome-blue scale)
  const getCellColor = (level: number, isToday: boolean) => {
    if (level === 0) {
      return isToday
        ? "bg-black/[0.03] dark:bg-white/[0.05] ring-1 ring-[#0071e3]/60"
        : "bg-black/[0.04] dark:bg-white/[0.06]";
    }
    if (level === 1) return "bg-[#0071e3]/25 dark:bg-[#0a84ff]/30";
    if (level === 2) return "bg-[#0071e3]/55 dark:bg-[#0a84ff]/60";
    if (level === 3) return "bg-[#0071e3]/80 dark:bg-[#0a84ff]/85";
    return "bg-[#0071e3] dark:bg-[#0a84ff]";
  };

  return (
    <>
      <div className="w-full bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl p-4 sm:p-5 shadow-[0_2px_16px_rgba(0,0,0,0.03)] space-y-4 transition-all select-none">
        {/* Top Summary Bar: Restrained typography & Direct Check-in CTA */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-black/[0.04] dark:border-white/[0.06]">
          {/* Left: Compact Stats Metrics */}
          <div className="flex items-center flex-wrap gap-x-4 sm:gap-x-6 gap-y-1.5 text-xs">
            <div className="flex items-baseline gap-1.5">
              <span className="text-[11px] text-[#86868b]">今日精听</span>
              <span className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                {stats !== null ? `${todayMinutes.toFixed(1)} 分钟` : "—"}
              </span>
            </div>

            <div className="flex items-baseline gap-1.5">
              <span className="text-[11px] text-[#86868b]">本周累计</span>
              <span className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                {stats !== null ? `${thisWeekMinutes.toFixed(1)} 分钟` : "—"}
              </span>
            </div>

            <div className="flex items-baseline gap-1.5">
              <span className="text-[11px] text-[#86868b]">连续打卡</span>
              <span className="font-semibold text-[#ff9500] flex items-center gap-1">
                <Flame className="w-3.5 h-3.5 fill-[#ff9500]" />
                {stats !== null ? `${streakDays} 天` : "—"}
              </span>
            </div>

            {/* Medals: Subtle inline badges */}
            {earnedMedals.length > 0 && (
              <div className="hidden md:flex items-center gap-1.5 text-[11px] text-[#86868b] pl-2 border-l border-black/[0.06] dark:border-white/[0.08]">
                <span>勋章：</span>
                {earnedMedals.map((m) => (
                  <span
                    key={m}
                    className="px-2 py-0.5 rounded-full bg-black/[0.04] dark:bg-white/[0.06] font-medium text-[#1d1d1f] dark:text-[#f5f5f7]"
                  >
                    {MEDAL_NAMES[m]}
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Right: Independent Punch Button */}
          <div className="flex items-center gap-2 self-start sm:self-auto">
            {punchFeedback && (
              <span className="text-[11px] text-[#ff3b30] animate-in fade-in duration-200">
                {punchFeedback}
              </span>
            )}

            <button
              onClick={handlePunchClick}
              disabled={isPunching}
              className={`inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-full text-xs font-semibold transition-all active:scale-95 shadow-sm ${
                isPunchedToday
                  ? "bg-[#1d1d1f] text-white hover:bg-black dark:bg-[#f5f5f7] dark:text-[#1d1d1f] dark:hover:bg-white"
                  : canPunch
                  ? "bg-[#0071e3] text-white hover:bg-[#0077ed]"
                  : "bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b] hover:bg-black/[0.07] dark:hover:bg-white/[0.1] border border-black/[0.04] dark:border-white/[0.06]"
              }`}
              title={
                isPunchedToday
                  ? "今日已完成打卡，点击生成分享卡片"
                  : canPunch
                  ? "点击打卡并生成今日精听卡片"
                  : `需精听满 1 分钟方可打卡（当前 ${todayMinutes.toFixed(1)} 分钟）`
              }
            >
              {isPunching ? (
                <>
                  <div className="w-3.5 h-3.5 border-2 border-current border-t-transparent rounded-full animate-spin" />
                  <span>正在打卡…</span>
                </>
              ) : isPunchedToday ? (
                <>
                  <Check className="w-3.5 h-3.5 text-[#34c759]" />
                  <span>已打卡 · 分享卡</span>
                </>
              ) : canPunch ? (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  <span>打卡</span>
                </>
              ) : (
                <>
                  <span>打卡</span>
                  <span className="text-[10px] opacity-75 font-normal">
                    ({todayMinutes.toFixed(1)}/1m)
                  </span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Lower Content: Mini Calendar + Contribution Heatmap */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-4 lg:gap-6 pt-1">
          {/* Left Column: Mini Calendar (当月小日历) */}
          <div className="lg:col-span-5 flex flex-col justify-between p-3.5 bg-black/[0.02] dark:bg-white/[0.03] rounded-2xl border border-black/[0.04] dark:border-white/[0.06]">
            <div className="flex items-center justify-between mb-2.5">
              <div className="flex items-center gap-1.5 text-xs font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                <CalendarIcon className="w-3.5 h-3.5 text-[#0071e3]" />
                <span>{calendarData.monthLabel}</span>
              </div>
              <span className="text-[10px] text-[#86868b]">
                当月已打卡{" "}
                <strong className="text-[#0071e3] dark:text-[#0a84ff] font-semibold">
                  {calendarData.days.filter((d) => d.isPunched).length}
                </strong>{" "}
                天
              </span>
            </div>

            {/* Weekday Labels (一至日) */}
            <div className="grid grid-cols-7 gap-1 text-center text-[10px] text-[#86868b] mb-1 font-medium">
              <span>一</span>
              <span>二</span>
              <span>三</span>
              <span>四</span>
              <span>五</span>
              <span>六</span>
              <span>日</span>
            </div>

            {/* Calendar Days Grid */}
            <div className="grid grid-cols-7 gap-1">
              {/* Empty placeholder cells before 1st of month */}
              {Array.from({ length: calendarData.startOffset }).map((_, i) => (
                <div key={`empty-${i}`} className="h-6 w-full" />
              ))}

              {/* Month Days */}
              {calendarData.days.map((d) => (
                <div
                  key={d.dateKey}
                  title={`${d.dateKey}: 精听 ${d.minutes.toFixed(1)} 分钟${d.isPunched ? " (已打卡)" : ""}`}
                  className={`h-6 w-full rounded-md flex items-center justify-center text-[11px] font-medium transition-all ${
                    d.isPunched
                      ? "bg-[#0071e3] text-white shadow-xs"
                      : d.isToday
                      ? "ring-1.5 ring-[#0071e3] text-[#0071e3] dark:text-[#0a84ff] font-bold"
                      : "text-[#1d1d1f] dark:text-[#a1a1a6] hover:bg-black/5 dark:hover:bg-white/5"
                  }`}
                >
                  {d.dayNum}
                </div>
              ))}
            </div>
          </div>

          {/* Right Column: GitHub-style Listening Duration Heatmap */}
          <div className="lg:col-span-7 flex flex-col justify-between p-3.5 bg-black/[0.02] dark:bg-white/[0.03] rounded-2xl border border-black/[0.04] dark:border-white/[0.06] overflow-hidden">
            <div className="flex items-center justify-between mb-2">
              <span className="text-xs font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                精听热图 (近 14 周)
              </span>
              {/* Legend */}
              <div className="flex items-center gap-1.5 text-[10px] text-[#86868b]">
                <span>少</span>
                <div className="flex items-center gap-1">
                  <span className="w-2.5 h-2.5 rounded-[2px] bg-black/[0.04] dark:bg-white/[0.06]" />
                  <span className="w-2.5 h-2.5 rounded-[2px] bg-[#0071e3]/25 dark:bg-[#0a84ff]/30" />
                  <span className="w-2.5 h-2.5 rounded-[2px] bg-[#0071e3]/55 dark:bg-[#0a84ff]/60" />
                  <span className="w-2.5 h-2.5 rounded-[2px] bg-[#0071e3]/80 dark:bg-[#0a84ff]/85" />
                  <span className="w-2.5 h-2.5 rounded-[2px] bg-[#0071e3] dark:bg-[#0a84ff]" />
                </div>
                <span>多</span>
              </div>
            </div>

            {/* Heatmap Grid: Horizontal scrollable on mobile */}
            <div className="overflow-x-auto no-scrollbar py-1">
              <div className="inline-flex gap-1.5">
                {/* 7 rows corresponding to Mon-Sun */}
                <div className="flex flex-col justify-between text-[9px] text-[#86868b] pr-1 py-0.5 select-none">
                  <span>一</span>
                  <span>三</span>
                  <span>五</span>
                  <span>日</span>
                </div>

                {heatmapData.map((week, wIdx) => (
                  <div key={`w-${wIdx}`} className="flex flex-col gap-1">
                    {week.map((day) => (
                      <div
                        key={day.dateKey}
                        title={`${day.dateKey}: 精听 ${day.minutes.toFixed(1)} 分钟`}
                        className={`w-3 h-3 rounded-[3px] transition-transform hover:scale-125 ${getCellColor(
                          day.level,
                          day.isToday
                        )}`}
                      />
                    ))}
                  </div>
                ))}
              </div>
            </div>

            <div className="flex items-center justify-between pt-1 text-[10px] text-[#86868b]">
              <span>点击打卡记录今日努力</span>
              <span>满 1 分钟即可打卡 · 保持连击</span>
            </div>
          </div>
        </div>
      </div>

      {/* Check-in Share Card Modal */}
      <ShareCardModal
        isOpen={isShareModalOpen}
        onClose={() => setIsShareModalOpen(false)}
        todayMinutes={todayMinutes}
        streakDays={streakDays}
      />
    </>
  );
}
