"use client";

import React, { useState, useEffect, useCallback } from "react";
import Link from "next/link";
import {
  Users,
  Clock,
  BookOpen,
  CheckCircle2,
  ChevronLeft,
  RefreshCw,
  Search,
  Sparkles,
  Flame,
  ShieldCheck,
  ShieldAlert,
  ArrowRight,
  TrendingUp,
  UserCheck,
  Globe,
  Eye,
} from "lucide-react";
import {
  api,
  AdminOverview,
  AdminUserItem,
  AdminPopularWord,
  AdminPopularExam,
} from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

export default function AdminPage() {
  const { user, isLoggedIn } = useAuth();
  const [overview, setOverview] = useState<AdminOverview | null>(null);
  const [users, setUsers] = useState<AdminUserItem[]>([]);
  const [popularWords, setPopularWords] = useState<AdminPopularWord[]>([]);
  const [popularExams, setPopularExams] = useState<AdminPopularExam[]>([]);
  const [searchQuery, setSearchQuery] = useState("");
  const [isLoading, setIsLoading] = useState(true);
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const loadData = useCallback(async (showSpin = true) => {
    if (showSpin) setIsRefreshing(true);
    setErrorMsg(null);
    try {
      const [resOverview, resUsers, resWords, resExams] = await Promise.all([
        api.getAdminOverview(),
        api.getAdminUsers(searchQuery),
        api.getAdminPopularWords(12),
        api.getAdminPopularExams(8),
      ]);
      setOverview(resOverview);
      setUsers(resUsers.users);
      setPopularWords(resWords);
      setPopularExams(resExams);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMsg(err.message);
      } else {
        setErrorMsg("获取数据失败，请确认是否具备管理员权限");
      }
    } finally {
      setIsLoading(false);
      setIsRefreshing(false);
    }
  }, [searchQuery]);

  useEffect(() => {
    if (isLoggedIn && user?.is_admin) {
      loadData(false);
    } else {
      setIsLoading(false);
    }
  }, [isLoggedIn, user, loadData]);

  const handleSearchSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    loadData(true);
  };

  const formatTimestamp = (ts?: number) => {
    if (!ts) return "—";
    const d = new Date(ts * 1000);
    const month = String(d.getMonth() + 1).padStart(2, "0");
    const day = String(d.getDate()).padStart(2, "0");
    const hours = String(d.getHours()).padStart(2, "0");
    const minutes = String(d.getMinutes()).padStart(2, "0");
    return `${month}-${day} ${hours}:${minutes}`;
  };

  // 1. Not Logged In
  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center justify-center p-6 select-none">
        <div className="w-full max-w-sm bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl p-8 shadow-xl text-center">
          <div className="w-12 h-12 rounded-2xl bg-[#0071e3]/10 text-[#0071e3] flex items-center justify-center mx-auto mb-4">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <h2 className="text-lg font-bold">请先登录管理员账号</h2>
          <p className="text-xs text-[#86868b] mt-1.5 mb-6">
            数据后台包含全站学员记录，需要管理员身份验证后方可查看。
          </p>
          <Link
            href="/login?redirect=/admin"
            className="w-full h-11 bg-[#0071e3] hover:bg-[#0077ed] text-white text-xs font-semibold rounded-full flex items-center justify-center gap-1.5 shadow-sm transition-all"
          >
            前往登录 <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>
      </div>
    );
  }

  // 2. Logged In but Not Admin
  if (!user?.is_admin) {
    return (
      <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center justify-center p-6 select-none">
        <div className="w-full max-w-sm bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] rounded-3xl p-8 shadow-xl text-center">
          <div className="w-12 h-12 rounded-2xl bg-[#ff3b30]/10 text-[#ff3b30] flex items-center justify-center mx-auto mb-4">
            <ShieldAlert className="w-6 h-6" />
          </div>
          <h2 className="text-lg font-bold">无权访问 (403 Forbidden)</h2>
          <p className="text-xs text-[#86868b] mt-1.5 mb-6 leading-relaxed">
            当前账号 <strong>{user?.username}</strong> 不是超级管理员，无法访问运营数据大盘。
          </p>
          <Link
            href="/"
            className="w-full h-11 bg-[#1d1d1f] dark:bg-[#f5f5f7] text-white dark:text-[#1d1d1f] text-xs font-semibold rounded-full flex items-center justify-center gap-1.5 shadow-sm transition-all"
          >
            返回首页
          </Link>
        </div>
      </div>
    );
  }
  // 3. Loading State
  if (isLoading && !overview) {
    return (
      <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] flex items-center justify-center p-6">
        <div className="flex flex-col items-center gap-3">
          <div className="w-7 h-7 border-2 border-[#0071e3] border-t-transparent rounded-full animate-spin" />
          <span className="text-xs text-[#86868b]">正在载入全站运营大盘…</span>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] p-4 sm:p-10 pt-[max(0.85rem,env(safe-area-inset-top))] pb-[max(2.5rem,env(safe-area-inset-bottom))] select-none">
      <div className="max-w-6xl mx-auto space-y-6">
        {/* Top Header Bar */}
        <header className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-black/[0.06] dark:border-white/[0.08]">
          <div className="flex items-center gap-3">
            <Link
              href="/"
              className="flex items-center gap-1 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] p-1.5 -ml-1.5 rounded-full transition-colors active:scale-95"
            >
              <ChevronLeft className="w-4 h-4" /> 返回首页
            </Link>
            <span className="text-black/10 dark:text-white/10 hidden sm:inline">·</span>
            <div className="flex items-center gap-2">
              <h1 className="text-base sm:text-lg font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                石头听力 · 运营数据看板
              </h1>
              <span className="px-2 py-0.5 text-[10px] font-semibold bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] rounded-full flex items-center gap-1">
                <ShieldCheck className="w-3 h-3" /> 超管
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2.5">
            <button
              onClick={() => loadData(true)}
              disabled={isRefreshing}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] bg-black/[0.03] dark:bg-white/[0.05] hover:bg-black/[0.06] transition-all active:scale-95"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? "animate-spin text-[#0071e3]" : ""}`} />
              <span>刷新数据</span>
            </button>

            <span className="text-xs text-[#86868b] px-2 py-1 bg-black/[0.02] dark:bg-white/[0.03] rounded-full border border-black/[0.04] dark:border-white/[0.06]">
              管理员: <strong>{user?.username}</strong>
            </span>
          </div>
        </header>

        {/* Error Banner if any */}
        {errorMsg && (
          <div className="p-4 rounded-2xl bg-[#ff3b30]/10 border border-[#ff3b30]/20 text-xs text-[#ff3b30] flex items-center gap-2">
            <ShieldAlert className="w-4 h-4 shrink-0" />
            <span>{errorMsg}</span>
          </div>
        )}

        {/* 1. Six Key Metrics Cards (PV, UV, Users, Listening, Vocab, Dictation) */}
        <div className="grid grid-cols-2 md:grid-cols-3 gap-3.5 sm:gap-4">
          {/* Card 1: Total PV */}
          <div className="p-4 sm:p-5 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#86868b]">
              <span className="text-xs font-medium">全站总访问请求 (PV)</span>
              <div className="w-8 h-8 rounded-xl bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] flex items-center justify-center">
                <Globe className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                {overview?.total_pv != null ? Number(overview.total_pv).toLocaleString() : "—"}{" "}
                <span className="text-xs font-normal text-[#86868b]">次</span>
              </div>
              <div className="mt-1 flex items-center gap-1.5 text-[11px] text-[#86868b] flex-wrap">
                <span className="text-[#0071e3] dark:text-[#0a84ff] font-semibold flex items-center gap-0.5">
                  <TrendingUp className="w-3 h-3" /> +{overview?.today_pv != null ? Number(overview.today_pv).toLocaleString() : 0} 今日
                </span>
                <span>·</span>
                <span>全站 HTTP 请求</span>
              </div>
            </div>
          </div>

          {/* Card 2: Total UV */}
          <div className="p-4 sm:p-5 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#86868b]">
              <span className="text-xs font-medium">独立访客 IP 数量 (UV)</span>
              <div className="w-8 h-8 rounded-xl bg-[#34c759]/10 text-[#34c759] dark:text-[#30d158] flex items-center justify-center">
                <Eye className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                {overview?.total_uv != null ? Number(overview.total_uv).toLocaleString() : "—"}{" "}
                <span className="text-xs font-normal text-[#86868b]">个独立 IP</span>
              </div>
              <div className="mt-1 flex items-center gap-1.5 text-[11px] text-[#86868b] flex-wrap">
                <span className="text-[#34c759] font-semibold flex items-center gap-0.5">
                  <TrendingUp className="w-3 h-3" /> +{overview?.today_uv != null ? Number(overview.today_uv).toLocaleString() : 0} 今日
                </span>
                <span>·</span>
                <span>排除内部开发调试</span>
              </div>
            </div>
          </div>

          {/* Card 3: Total Users */}
          <div className="p-4 sm:p-5 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#86868b]">
              <span className="text-xs font-medium">注册学员总数</span>
              <div className="w-8 h-8 rounded-xl bg-[#5856d6]/10 text-[#5856d6] dark:text-[#5e5ce6] flex items-center justify-center">
                <Users className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                {overview?.total_users ?? "—"}{" "}
                <span className="text-xs font-normal text-[#86868b]">人</span>
              </div>
              <div className="mt-1 flex items-center gap-2 text-[11px] text-[#86868b] flex-wrap">
                <span className="text-[#5856d6] dark:text-[#5e5ce6] font-semibold flex items-center gap-0.5">
                  <TrendingUp className="w-3 h-3" /> +{overview?.today_new_users ?? 0} 今日
                </span>
                <span>·</span>
                <span>今日活跃 {overview?.active_users_today ?? 0} 人</span>
              </div>
            </div>
          </div>

          {/* Card 4: Total Listening Minutes */}
          <div className="p-4 sm:p-5 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#86868b]">
              <span className="text-xs font-medium">累计精听总时长</span>
              <div className="w-8 h-8 rounded-xl bg-[#ff9500]/10 text-[#ff9500] flex items-center justify-center">
                <Clock className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                {overview ? `${overview.total_listening_minutes}m` : "—"}
              </div>
              <div className="mt-1 text-[11px] text-[#86868b]">
                今日产生 <strong className="text-[#ff9500]">{overview?.today_listening_minutes ?? 0}</strong> 分钟精听
              </div>
            </div>
          </div>

          {/* Card 5: Total Vocabulary */}
          <div className="p-4 sm:p-5 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#86868b]">
              <span className="text-xs font-medium">全网生词收集量</span>
              <div className="w-8 h-8 rounded-xl bg-[#ff2d55]/10 text-[#ff2d55] flex items-center justify-center">
                <BookOpen className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                {overview?.total_vocab_words ?? "—"}{" "}
                <span className="text-xs font-normal text-[#86868b]">词</span>
              </div>
              <div className="mt-1 text-[11px] text-[#86868b]">
                今日新增 <strong className="text-[#ff2d55]">+{overview?.today_vocab_words ?? 0}</strong> 词入生词本
              </div>
            </div>
          </div>

          {/* Card 6: Dictations & Accuracy */}
          <div className="p-4 sm:p-5 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] flex flex-col justify-between">
            <div className="flex items-center justify-between text-[#86868b]">
              <span className="text-xs font-medium">听写打卡与正确率</span>
              <div className="w-8 h-8 rounded-xl bg-[#af52de]/10 text-[#af52de] flex items-center justify-center">
                <CheckCircle2 className="w-4 h-4" />
              </div>
            </div>
            <div className="mt-3">
              <div className="text-2xl sm:text-3xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                {overview?.total_dictation_attempts ?? "—"}{" "}
                <span className="text-xs font-normal text-[#86868b]">次</span>
              </div>
              <div className="mt-1 text-[11px] text-[#86868b]">
                全站平均准确率 <strong className="text-[#af52de]">{overview?.avg_dictation_accuracy ?? 0}%</strong>
              </div>
            </div>
          </div>
        </div>

        {/* 2. Main Two Columns: User Table (Left) + Popular Words & Exams (Right) */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column: Registered Users Table (2 Cols wide on Desktop) */}
          <div className="lg:col-span-2 space-y-4">
            <div className="p-5 sm:p-6 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] space-y-4">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                <div>
                  <h2 className="text-sm sm:text-base font-bold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
                    <UserCheck className="w-4 h-4 text-[#0071e3]" /> 学员注册与活跃明细
                  </h2>
                  <p className="text-xs text-[#86868b] mt-0.5">
                    实时显示从各个渠道注册学习的用户档案与活跃数据
                  </p>
                </div>

                {/* Search Form */}
                <form onSubmit={handleSearchSubmit} className="relative max-w-xs">
                  <input
                    type="text"
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    placeholder="按用户名搜索..."
                    className="h-9 pl-8 pr-3 text-xs bg-black/[0.03] dark:bg-white/[0.05] border border-black/[0.06] dark:border-white/[0.08] rounded-full focus:outline-none focus:border-[#0071e3] text-[#1d1d1f] dark:text-[#f5f5f7] transition-all w-full"
                  />
                  <Search className="w-3.5 h-3.5 text-[#86868b] absolute left-2.5 top-1/2 -translate-y-1/2 pointer-events-none" />
                </form>
              </div>

              {/* Users Table */}
              <div className="overflow-x-auto no-scrollbar pt-1">
                {users.length === 0 ? (
                  <div className="text-center py-12 text-xs text-[#86868b]">
                    暂无符合条件的用户记录
                  </div>
                ) : (
                  <table className="w-full text-left text-xs">
                    <thead>
                      <tr className="border-b border-black/[0.06] dark:border-white/[0.08] text-[#86868b]">
                        <th className="pb-3 font-medium">用户名</th>
                        <th className="pb-3 font-medium">注册时间</th>
                        <th className="pb-3 font-medium">生词量</th>
                        <th className="pb-3 font-medium">累计精听</th>
                        <th className="pb-3 font-medium">听写次数</th>
                        <th className="pb-3 font-medium">最近活跃</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-black/[0.04] dark:divide-white/[0.05]">
                      {users.map((u) => (
                        <tr key={u.id} className="hover:bg-black/[0.02] dark:hover:bg-white/[0.02] transition-colors">
                          <td className="py-3 font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-2">
                            <span className="w-6 h-6 rounded-full bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] flex items-center justify-center text-[10px] font-bold">
                              {u.username.slice(0, 1).toUpperCase()}
                            </span>
                            <span>{u.username}</span>
                          </td>
                          <td className="py-3 text-[#86868b] font-mono">
                            {formatTimestamp(u.created_at)}
                          </td>
                          <td className="py-3">
                            <span className="px-2 py-0.5 rounded-full bg-[#34c759]/10 text-[#34c759] font-medium text-[11px]">
                              {u.vocab_count} 词
                            </span>
                          </td>
                          <td className="py-3 font-medium text-[#ff9500]">
                            {u.listening_minutes} 分钟
                          </td>
                          <td className="py-3 text-[#86868b]">
                            {u.dictation_count} 次
                          </td>
                          <td className="py-3 text-[#86868b] font-mono text-[11px]">
                            {formatTimestamp(u.last_login_at)}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </div>
          </div>

          {/* Right Column: Top Words & Popular Exams (1 Col wide) */}
          <div className="space-y-6">
            {/* Top Saved Words Widget */}
            <div className="p-5 sm:p-6 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] space-y-4">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-sm font-bold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-1.5">
                    <Sparkles className="w-4 h-4 text-[#ff9500]" /> 全网高频生词 TOP 12
                  </h3>
                  <p className="text-[11px] text-[#86868b] mt-0.5">
                    大家最容易卡壳的难词（小红书选题绝佳灵感）
                  </p>
                </div>
              </div>

              {popularWords.length === 0 ? (
                <div className="text-center py-8 text-xs text-[#86868b]">
                  用户尚未添加生词
                </div>
              ) : (
                <div className="space-y-2">
                  {popularWords.map((pw, idx) => (
                    <div
                      key={pw.word}
                      className="p-2.5 rounded-2xl bg-black/[0.02] dark:bg-white/[0.03] border border-black/[0.04] dark:border-white/[0.06] flex items-center justify-between gap-2"
                    >
                      <div className="flex items-center gap-2.5 min-w-0">
                        <span
                          className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] font-bold shrink-0 ${
                            idx === 0
                              ? "bg-[#ff9500] text-white"
                              : idx === 1
                              ? "bg-[#86868b] text-white"
                              : idx === 2
                              ? "bg-[#a2845e] text-white"
                              : "bg-black/[0.06] dark:bg-white/[0.1] text-[#86868b]"
                          }`}
                        >
                          {idx + 1}
                        </span>
                        <div className="truncate">
                          <span className="text-xs font-bold text-[#1d1d1f] dark:text-[#f5f5f7]">
                            {pw.word}
                          </span>
                          <p className="text-[11px] text-[#86868b] truncate mt-0.5">
                            {pw.definition_zh}
                          </p>
                        </div>
                      </div>

                      <span className="shrink-0 text-[10px] font-semibold px-2 py-0.5 rounded-full bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff]">
                        {pw.count} 人收藏
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Popular Exams Widget */}
            <div className="p-5 sm:p-6 rounded-3xl bg-white dark:bg-[#1c1c1e] border border-black/[0.06] dark:border-white/[0.08] shadow-[0_4px_20px_rgba(0,0,0,0.03)] space-y-3.5">
              <h3 className="text-sm font-bold text-[#1d1d1f] dark:text-[#f5f5f7] flex items-center gap-1.5">
                <Flame className="w-4 h-4 text-[#ff3b30]" /> 热门真题练习排行
              </h3>

              {popularExams.length === 0 ? (
                <div className="text-center py-6 text-xs text-[#86868b]">
                  暂无真题练习数据
                </div>
              ) : (
                <div className="space-y-2">
                  {popularExams.map((pe) => (
                    <div
                      key={pe.exam_id}
                      className="p-2.5 rounded-xl bg-black/[0.02] dark:bg-white/[0.03] flex items-center justify-between text-xs"
                    >
                      <span className="text-[#1d1d1f] dark:text-[#f5f5f7] font-medium truncate max-w-[160px]">
                        {pe.title}
                      </span>
                      <span className="text-[11px] text-[#86868b]">
                        {pe.session_count} 次 · {pe.total_minutes} 分钟
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
