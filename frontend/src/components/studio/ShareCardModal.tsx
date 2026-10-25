/* eslint-disable @next/next/no-img-element */
"use client";

import React, { useState, useEffect, useCallback } from "react";
import { X, Download, Copy, Check } from "lucide-react";

interface ShareCardModalProps {
  isOpen: boolean;
  onClose: () => void;
  todayMinutes: number;
  streakDays: number;
}

export function ShareCardModal({
  isOpen,
  onClose,
  todayMinutes,
  streakDays,
}: ShareCardModalProps) {
  const [imageUrl, setImageUrl] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [downloadSuccess, setDownloadSuccess] = useState(false);

  // Generate 1080x1440 Apple minimalist punch card via HTML5 Canvas
  const generateCard = useCallback(() => {
    const canvas = document.createElement("canvas");
    canvas.width = 1080;
    canvas.height = 1440;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    // 1. Crisp Apple neutral background (#fbfbfd)
    ctx.fillStyle = "#fbfbfd";
    ctx.fillRect(0, 0, 1080, 1440);

    // Subtle outer border
    ctx.strokeStyle = "rgba(0, 0, 0, 0.06)";
    ctx.lineWidth = 2;
    ctx.strokeRect(40, 40, 1000, 1360);

    // 2. Top Branding: 石头听力 · mystone.top
    ctx.fillStyle = "#86868b";
    ctx.font = "500 36px -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif";
    ctx.textAlign = "left";
    ctx.fillText("石头听力", 100, 150);

    ctx.fillStyle = "#a1a1a6";
    ctx.font = "400 32px -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif";
    ctx.textAlign = "right";
    ctx.fillText("mystone.top", 980, 150);

    // Divider line
    ctx.strokeStyle = "rgba(0, 0, 0, 0.05)";
    ctx.lineWidth = 1.5;
    ctx.beginPath();
    ctx.moveTo(100, 190);
    ctx.lineTo(980, 190);
    ctx.stroke();

    // 3. Date in Asia/Shanghai timezone
    const now = new Date();
    // Compute CST (UTC+8) date components
    const utc = now.getTime() + now.getTimezoneOffset() * 60000;
    const cstDate = new Date(utc + 3600000 * 8);
    const year = cstDate.getFullYear();
    const month = cstDate.getMonth() + 1;
    const day = cstDate.getDate();
    const weekDays = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
    const weekZh = weekDays[cstDate.getDay()];
    const dateStr = `${year}年${month}月${day}日 · ${weekZh}`;

    ctx.fillStyle = "#86868b";
    ctx.font = "400 36px -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif";
    ctx.textAlign = "left";
    ctx.fillText(dateStr, 100, 310);

    // 4. Fixed headline (Steve Jobs short human copy)
    ctx.fillStyle = "#1d1d1f";
    ctx.font = "600 68px -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif";
    ctx.fillText("今天听完一句六级", 100, 420);

    // 5. Hero Metric Card Area: 大字号数字 + 充裕留白
    ctx.fillStyle = "#86868b";
    ctx.font = "400 40px -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif";
    ctx.fillText("今日精听", 100, 620);

    // Big bold numbers
    const minutesStr = todayMinutes.toFixed(1);
    ctx.fillStyle = "#1d1d1f";
    ctx.font = "700 180px -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif";
    ctx.fillText(minutesStr, 100, 800);

    // Unit "分钟"
    const numWidth = ctx.measureText(minutesStr).width;
    ctx.fillStyle = "#86868b";
    ctx.font = "500 52px -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif";
    ctx.fillText("分钟", 100 + numWidth + 24, 780);

    // 6. Streak (连续 N 天, N >= 1 才展示)
    if (streakDays >= 1) {
      ctx.fillStyle = "#ff9500";
      ctx.font = "600 48px -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif";
      ctx.fillText(`连续 ${streakDays} 天`, 100, 930);
    }

    // 7. Footer
    ctx.fillStyle = "#86868b";
    ctx.font = "400 34px -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif";
    ctx.fillText("大学英语六级听力 · 沉浸单句精听", 100, 1260);

    ctx.fillStyle = "#a1a1a6";
    ctx.font = "400 30px -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif";
    ctx.fillText("mystone.top", 100, 1315);

    try {
      const url = canvas.toDataURL("image/png");
      setImageUrl(url);
    } catch (e) {
      console.error("Canvas export failed", e);
    }
  }, [todayMinutes, streakDays]);

  useEffect(() => {
    if (isOpen) {
      generateCard();
      setCopied(false);
      setDownloadSuccess(false);
    }
  }, [isOpen, generateCard]);

  if (!isOpen) return null;

  // Copy share text to clipboard
  const copyText = streakDays >= 1
    ? `今天听完一句六级真题精听，连续 ${streakDays} 天。mystone.top`
    : `今天听完一句六级真题精听。mystone.top`;

  const handleCopy = async () => {
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(copyText);
        setCopied(true);
        setTimeout(() => setCopied(false), 2500);
      }
    } catch {
      // Fallback
    }
  };

  const handleDownload = () => {
    if (!imageUrl) return;
    try {
      const a = document.createElement("a");
      a.href = imageUrl;
      a.download = `石头听力-打卡-${todayMinutes}分钟.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      setDownloadSuccess(true);
      setTimeout(() => setDownloadSuccess(false), 2500);
    } catch (e) {
      console.error("Download failed", e);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-in fade-in duration-200">
      <div className="relative w-full max-w-sm sm:max-w-md bg-white dark:bg-[#1c1c1e] rounded-3xl shadow-2xl p-5 sm:p-6 flex flex-col items-center gap-4">
        {/* Top Header */}
        <div className="w-full flex items-center justify-between">
          <span className="text-xs font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
            今日打卡
          </span>
          <button
            onClick={onClose}
            className="w-7 h-7 flex items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/10 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Card Preview (Mobile tap-and-hold friendly) */}
        <div className="w-full flex justify-center py-1">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt="打卡分享卡片"
              className="max-h-[50vh] sm:max-h-[55vh] w-auto rounded-2xl shadow-md border border-black/[0.06] dark:border-white/[0.08] select-none pointer-events-auto"
            />
          ) : (
            <div className="w-full h-72 flex items-center justify-center text-xs text-[#86868b]">
              正在生成打卡卡片…
            </div>
          )}
        </div>

        <p className="text-[11px] text-[#86868b] text-center">
          手机端可长按图片直接保存至相册
        </p>

        {/* Action Buttons: 极简纯黑/浅灰，不超过 1 个主 CTA */}
        <div className="w-full flex items-center gap-2.5 pt-1">
          <button
            onClick={handleCopy}
            className="flex-1 inline-flex items-center justify-center gap-1.5 py-2.5 px-4 rounded-full text-xs font-medium bg-black/[0.04] dark:bg-white/[0.08] hover:bg-black/[0.08] dark:hover:bg-white/[0.14] text-[#1d1d1f] dark:text-[#f5f5f7] transition-all active:scale-95"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-[#34c759]" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? "已复制文案" : "复制文案"}</span>
          </button>

          <button
            onClick={handleDownload}
            className="flex-1 inline-flex items-center justify-center gap-1.5 py-2.5 px-4 rounded-full text-xs font-semibold bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] shadow-sm transition-all active:scale-95"
          >
            {downloadSuccess ? <Check className="w-3.5 h-3.5 text-[#34c759]" /> : <Download className="w-3.5 h-3.5" />}
            <span>{downloadSuccess ? "已下载图片" : "保存图片"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
