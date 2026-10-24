"use client";

import React, { useState, Suspense } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import Link from "next/link";
import { Headphones, ArrowLeft, Loader2, CheckCircle2, AlertCircle } from "lucide-react";
import { useAuth } from "@/hooks/useAuth";

function LoginForm() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectUrl = searchParams.get("redirect") || "/";

  const { login, register } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [successMsg, setSuccessMsg] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccessMsg(null);

    const cleanUser = username.trim();
    if (!cleanUser) {
      setError("请输入用户名或邮箱");
      return;
    }
    if (cleanUser.length < 2 || cleanUser.length > 30) {
      setError("用户名长度需在 2 至 30 个字符之间");
      return;
    }
    if (password.length < 6) {
      setError("密码长度至少为 6 个字符");
      return;
    }
    if (mode === "register" && password !== confirmPassword) {
      setError("两次输入的密码不一致");
      return;
    }

    setIsLoading(true);
    try {
      if (mode === "login") {
        await login(cleanUser, password);
        setSuccessMsg("登录成功，正在前往工作台…");
      } else {
        await register(cleanUser, password);
        setSuccessMsg("注册成功，已同步云端生词本…");
      }
      setTimeout(() => {
        router.push(redirectUrl);
      }, 600);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("操作失败，请检查网络后重试");
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] flex flex-col justify-between p-6 sm:p-12 select-none">
      {/* Top Bar */}
      <header className="w-full max-w-md mx-auto flex items-center justify-between">
        <Link
          href={redirectUrl}
          className="flex items-center gap-1.5 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
        >
          <ArrowLeft className="w-3.5 h-3.5" /> 返回
        </Link>
        <span className="text-xs font-medium text-[#86868b]">石头听力 · 账号体系</span>
      </header>

      {/* Main Card */}
      <main className="w-full max-w-sm mx-auto my-auto animate-in fade-in zoom-in-95 duration-200">
        <div className="bg-white/80 dark:bg-[#1c1c1e]/80 backdrop-blur-xl border border-black/[0.06] dark:border-white/[0.08] shadow-[0_8px_32px_rgba(0,0,0,0.06)] dark:shadow-[0_8px_32px_rgba(0,0,0,0.4)] rounded-3xl p-7 sm:p-8 flex flex-col items-center text-center">
          {/* Logo Badge */}
          <div className="w-12 h-12 rounded-2xl bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] flex items-center justify-center mb-3.5">
            <Headphones className="w-6 h-6" />
          </div>

          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
            石头听力
          </h1>
          <p className="text-xs text-[#86868b] dark:text-[#a1a1a6] mt-1 mb-6">
            登录以永久保存生词本与做题进度
          </p>

          {/* Mode Switcher Segmented Control */}
          <div className="w-full p-1 bg-black/[0.04] dark:bg-white/[0.06] rounded-full flex items-center mb-6">
            <button
              type="button"
              onClick={() => {
                setMode("login");
                setError(null);
              }}
              className={`flex-1 py-1.5 text-xs font-medium rounded-full transition-all ${
                mode === "login"
                  ? "bg-white dark:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm font-semibold"
                  : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              }`}
            >
              登录账号
            </button>
            <button
              type="button"
              onClick={() => {
                setMode("register");
                setError(null);
              }}
              className={`flex-1 py-1.5 text-xs font-medium rounded-full transition-all ${
                mode === "register"
                  ? "bg-white dark:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] shadow-sm font-semibold"
                  : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              }`}
            >
              免费注册
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="w-full flex flex-col gap-3.5 text-left">
            <div>
              <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] mb-1.5 px-1">
                账号 / 用户名
              </label>
              <input
                type="text"
                autoComplete="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                placeholder="例如：stone 或常用邮箱"
                className="w-full h-11 px-3.5 text-sm bg-black/[0.02] dark:bg-white/[0.04] border border-black/[0.08] dark:border-white/[0.1] rounded-2xl focus:outline-none focus:border-[#0071e3] focus:ring-4 focus:ring-[#0071e3]/10 text-[#1d1d1f] dark:text-[#f5f5f7] transition-all"
              />
            </div>

            <div>
              <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] mb-1.5 px-1">
                登录密码
              </label>
              <input
                type="password"
                autoComplete={mode === "login" ? "current-password" : "new-password"}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="至少 6 位字符"
                className="w-full h-11 px-3.5 text-sm bg-black/[0.02] dark:bg-white/[0.04] border border-black/[0.08] dark:border-white/[0.1] rounded-2xl focus:outline-none focus:border-[#0071e3] focus:ring-4 focus:ring-[#0071e3]/10 text-[#1d1d1f] dark:text-[#f5f5f7] transition-all"
              />
            </div>

            {mode === "register" && (
              <div className="animate-in fade-in duration-150">
                <label className="block text-[11px] font-medium text-[#86868b] dark:text-[#a1a1a6] mb-1.5 px-1">
                  确认密码
                </label>
                <input
                  type="password"
                  autoComplete="new-password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="再次输入密码"
                  className="w-full h-11 px-3.5 text-sm bg-black/[0.02] dark:bg-white/[0.04] border border-black/[0.08] dark:border-white/[0.1] rounded-2xl focus:outline-none focus:border-[#0071e3] focus:ring-4 focus:ring-[#0071e3]/10 text-[#1d1d1f] dark:text-[#f5f5f7] transition-all"
                />
              </div>
            )}

            {/* Error Message */}
            {error && (
              <div className="flex items-center gap-1.5 text-xs text-[#ff3b30] px-1 animate-in fade-in duration-150">
                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                <span>{error}</span>
              </div>
            )}

            {/* Success Message */}
            {successMsg && (
              <div className="flex items-center gap-1.5 text-xs text-[#34c759] px-1 animate-in fade-in duration-150">
                <CheckCircle2 className="w-3.5 h-3.5 shrink-0" />
                <span>{successMsg}</span>
              </div>
            )}

            {/* Submit Button */}
            <button
              type="submit"
              disabled={isLoading}
              className="mt-2 w-full h-11 bg-[#0071e3] hover:bg-[#0077ed] active:scale-[0.98] disabled:opacity-50 text-white text-sm font-semibold rounded-full shadow-sm flex items-center justify-center gap-2 transition-all"
            >
              {isLoading ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : mode === "login" ? (
                "登录账号"
              ) : (
                "立即注册并开始精听"
              )}
            </button>
          </form>

          {/* Guest Link */}
          <div className="mt-5 pt-4 border-t border-black/[0.04] dark:border-white/[0.06] w-full">
            <Link
              href={redirectUrl}
              className="text-xs text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
            >
              暂不登录，以访客身份继续练习 →
            </Link>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="w-full max-w-md mx-auto text-center text-[11px] text-[#86868b]/60">
        石头听力 · 极简专注 · 数据安全隔离
      </footer>
    </div>
  );
}

export default function LoginPage() {
  return (
    <Suspense
      fallback={
        <div className="min-h-screen flex items-center justify-center bg-[#f5f5f7] dark:bg-[#000000]">
          <Loader2 className="w-7 h-7 text-[#0071e3] animate-spin" />
        </div>
      }
    >
      <LoginForm />
    </Suspense>
  );
}
