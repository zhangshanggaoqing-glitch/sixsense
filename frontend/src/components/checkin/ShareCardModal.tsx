/* eslint-disable @next/next/no-img-element */
"use client";

import React, { useState, useEffect, useCallback } from "react";
import { X, Download, Copy, Check, RefreshCw } from "lucide-react";
import QRCode from "qrcode";
import { getDailyQuote, QuoteItem, CURATED_QUOTES } from "@/lib/quotes";
import { getDailyBg, CardBgItem, CARD_BACKGROUNDS } from "@/lib/cardImages";

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
  const [isGenerating, setIsGenerating] = useState(false);
  const [currentQuote, setCurrentQuote] = useState<QuoteItem>(() => getDailyQuote());
  const [currentBg, setCurrentBg] = useState<CardBgItem>(() => getDailyBg());

  // Helper to wrap text cleanly on HTML5 canvas
  const wrapText = (
    ctx: CanvasRenderingContext2D,
    text: string,
    maxWidth: number
  ): string[] => {
    const words = text.split(" ");
    const lines: string[] = [];
    let currentLine = "";

    for (let i = 0; i < words.length; i++) {
      const word = words[i];
      const testLine = currentLine.length === 0 ? word : `${currentLine} ${word}`;
      const metrics = ctx.measureText(testLine);
      if (metrics.width > maxWidth && currentLine.length > 0) {
        lines.push(currentLine);
        currentLine = word;
      } else {
        currentLine = testLine;
      }
    }
    if (currentLine) {
      lines.push(currentLine);
    }
    return lines;
  };

  // Generate 1080x1440 Apple minimalist punch card via HTML5 Canvas
  const generateCard = useCallback(
    async (quoteToUse: QuoteItem, bgToUse: CardBgItem) => {
      setIsGenerating(true);
      const canvas = document.createElement("canvas");
      canvas.width = 1080;
      canvas.height = 1440;
      const ctx = canvas.getContext("2d");
      if (!ctx) {
        setIsGenerating(false);
        return;
      }

      // 1. Draw background image with fallback
      const loadImage = (url: string): Promise<HTMLImageElement> => {
        return new Promise((resolve, reject) => {
          const img = new Image();
          img.crossOrigin = "anonymous";
          img.onload = () => resolve(img);
          img.onerror = () => reject(new Error(`Failed to load ${url}`));
          img.src = url;
        });
      };

      let bgImg: HTMLImageElement | null = null;
      try {
        bgImg = await loadImage(bgToUse.localUrl);
      } catch {
        try {
          bgImg = await loadImage(bgToUse.unsplashUrl);
        } catch {
          // If both fail, render elegant procedural dusk gradient
          bgImg = null;
        }
      }

      if (bgImg) {
        // Draw image scaled to cover canvas maintaining aspect ratio
        const imgRatio = bgImg.width / bgImg.height;
        const canvasRatio = 1080 / 1440;
        let sWidth = bgImg.width;
        let sHeight = bgImg.height;
        let sx = 0;
        let sy = 0;

        if (imgRatio > canvasRatio) {
          sWidth = bgImg.height * canvasRatio;
          sx = (bgImg.width - sWidth) / 2;
        } else {
          sHeight = bgImg.width / canvasRatio;
          sy = (bgImg.height - sHeight) / 2;
        }
        ctx.drawImage(bgImg, sx, sy, sWidth, sHeight, 0, 0, 1080, 1440);
      } else {
        const grad = ctx.createLinearGradient(0, 0, 1080, 1440);
        grad.addColorStop(0, "#1d2333");
        grad.addColorStop(0.5, "#2a364f");
        grad.addColorStop(1, "#181b24");
        ctx.fillStyle = grad;
        ctx.fillRect(0, 0, 1080, 1440);
      }

      // 2. Subtle Vignette & Gradient Mask for Apple-grade contrast and readability
      // Top header gradient
      const topGrad = ctx.createLinearGradient(0, 0, 0, 360);
      topGrad.addColorStop(0, "rgba(0, 0, 0, 0.65)");
      topGrad.addColorStop(0.6, "rgba(0, 0, 0, 0.3)");
      topGrad.addColorStop(1, "rgba(0, 0, 0, 0)");
      ctx.fillStyle = topGrad;
      ctx.fillRect(0, 0, 1080, 360);

      // Central dark tint for quote contrast
      const midGrad = ctx.createLinearGradient(0, 360, 0, 1080);
      midGrad.addColorStop(0, "rgba(0, 0, 0, 0.2)");
      midGrad.addColorStop(0.5, "rgba(0, 0, 0, 0.45)");
      midGrad.addColorStop(1, "rgba(0, 0, 0, 0.3)");
      ctx.fillStyle = midGrad;
      ctx.fillRect(0, 360, 1080, 720);

      // Bottom footer gradient
      const btmGrad = ctx.createLinearGradient(0, 980, 0, 1440);
      btmGrad.addColorStop(0, "rgba(0, 0, 0, 0)");
      btmGrad.addColorStop(0.4, "rgba(0, 0, 0, 0.5)");
      btmGrad.addColorStop(1, "rgba(0, 0, 0, 0.85)");
      ctx.fillStyle = btmGrad;
      ctx.fillRect(0, 980, 1080, 460);

      // 3. Top Header: Brand & Date
      // Date in Asia/Shanghai timezone
      const now = new Date();
      const utc = now.getTime() + now.getTimezoneOffset() * 60000;
      const cstDate = new Date(utc + 3600000 * 8);
      const year = cstDate.getFullYear();
      const month = cstDate.getMonth() + 1;
      const day = cstDate.getDate();
      const weekDays = ["星期日", "星期一", "星期二", "星期三", "星期四", "星期五", "星期六"];
      const weekZh = weekDays[cstDate.getDay()];
      const dateStr = `${year}年${month}月${day}日 · ${weekZh}`;

      ctx.fillStyle = "rgba(255, 255, 255, 0.95)";
      ctx.font = "600 38px -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif";
      ctx.textAlign = "left";
      ctx.fillText("石头听力", 90, 140);

      ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
      ctx.font = "400 26px -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif";
      ctx.fillText(dateStr, 90, 185);

      // 4. Top Right: Tiny quiet low-contrast QR Code -> https://mystone.top
      try {
        const qrCanvas = document.createElement("canvas");
        await QRCode.toCanvas(qrCanvas, "https://mystone.top", {
          width: 96,
          margin: 1,
          color: {
            dark: "#ffffffcc", // Soft translucent white
            light: "#00000000", // Fully transparent
          },
        });
        ctx.drawImage(qrCanvas, 1080 - 90 - 96, 96, 96, 96);
      } catch (err) {
        console.error("QR Code generation error", err);
      }

      // 5. Center English Quote: Spacious, airy typography
      const quoteMaxWidth = 900;
      ctx.font = "400 48px -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'Helvetica Neue', sans-serif";
      ctx.textAlign = "center";
      const quoteLines = wrapText(ctx, `"${quoteToUse.text}"`, quoteMaxWidth);

      const lineHeight = 72;
      const totalQuoteHeight = quoteLines.length * lineHeight;
      const quoteStartY = 640 - totalQuoteHeight / 2;

      ctx.fillStyle = "#ffffff";
      quoteLines.forEach((line, idx) => {
        ctx.fillText(line, 540, quoteStartY + idx * lineHeight);
      });

      // Author line
      if (quoteToUse.author) {
        ctx.fillStyle = "rgba(255, 255, 255, 0.72)";
        ctx.font = "300 28px -apple-system, BlinkMacSystemFont, 'SF Pro Text', sans-serif";
        ctx.fillText(`— ${quoteToUse.author}`, 540, quoteStartY + quoteLines.length * lineHeight + 40);
      }

      // 6. Stats Section: Refined, modern Apple layout
      // Thin elegant horizontal hairline
      ctx.strokeStyle = "rgba(255, 255, 255, 0.16)";
      ctx.lineWidth = 1.5;
      ctx.beginPath();
      ctx.moveTo(90, 1160);
      ctx.lineTo(990, 1160);
      ctx.stroke();

      // Metrics row
      ctx.textAlign = "left";
      ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
      ctx.font = "400 26px -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif";
      ctx.fillText("今日精听", 90, 1215);

      ctx.fillStyle = "#ffffff";
      ctx.font = "600 44px -apple-system, BlinkMacSystemFont, 'SF Pro Display', sans-serif";
      const minText = `${todayMinutes.toFixed(1)} 分钟`;
      ctx.fillText(minText, 90, 1270);

      // Streak badge on right
      if (streakDays >= 1) {
        ctx.textAlign = "right";
        ctx.fillStyle = "rgba(255, 255, 255, 0.7)";
        ctx.font = "400 26px -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif";
        ctx.fillText("连续打卡", 990, 1215);

        ctx.fillStyle = "#ff9f0a"; // Warm Apple gold/orange
        ctx.font = "600 44px -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'PingFang SC', sans-serif";
        ctx.fillText(`${streakDays} 天 🔥`, 990, 1270);
      }

      // 7. Bottom Fixed Tagline: mystone.top 永远免费的精听网站
      ctx.textAlign = "center";
      ctx.fillStyle = "rgba(255, 255, 255, 0.55)";
      ctx.font = "400 24px -apple-system, BlinkMacSystemFont, 'SF Pro Text', 'PingFang SC', sans-serif";
      ctx.fillText("mystone.top 永远免费的精听网站", 540, 1370);

      try {
        const url = canvas.toDataURL("image/png");
        setImageUrl(url);
      } catch (e) {
        console.error("Canvas export failed", e);
      } finally {
        setIsGenerating(false);
      }
    },
    [todayMinutes, streakDays]
  );

  useEffect(() => {
    if (isOpen) {
      const q = getDailyQuote();
      const b = getDailyBg();
      setCurrentQuote(q);
      setCurrentBg(b);
      generateCard(q, b);
      setCopied(false);
      setDownloadSuccess(false);
    }
  }, [isOpen, generateCard]);

  // Handle manual backdrop or escape key to dismiss
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  // Cycle to another background / quote on user request
  const handleRandomize = () => {
    const nextBgIdx = (CARD_BACKGROUNDS.findIndex((b) => b.id === currentBg.id) + 1) % CARD_BACKGROUNDS.length;
    const nextBg = CARD_BACKGROUNDS[nextBgIdx];
    const nextQuoteIdx = Math.floor(Math.random() * CURATED_QUOTES.length);
    const nextQuote = CURATED_QUOTES[nextQuoteIdx];

    setCurrentBg(nextBg);
    setCurrentQuote(nextQuote);
    generateCard(nextQuote, nextBg);
  };

  const copyText = streakDays >= 1
    ? `"${currentQuote.text}" — 今天在石头听力精听 ${todayMinutes.toFixed(1)} 分钟，连续打卡 ${streakDays} 天。mystone.top 永远免费的精听网站`
    : `"${currentQuote.text}" — 今天在石头听力精听 ${todayMinutes.toFixed(1)} 分钟。mystone.top 永远免费的精听网站`;

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
      a.download = `石头听力-打卡-${todayMinutes.toFixed(1)}分钟.png`;
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
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-4 bg-black/60 backdrop-blur-md animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-sm sm:max-w-md bg-white dark:bg-[#1c1c1e] rounded-3xl shadow-2xl p-4 sm:p-6 flex flex-col items-center gap-3.5 border border-black/[0.08] dark:border-white/[0.12] transition-all"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top Header */}
        <div className="w-full flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
              今日打卡卡片
            </span>
            <span className="text-xs text-[#86868b]">
              · {todayMinutes.toFixed(1)} 分钟
            </span>
          </div>

          <div className="flex items-center gap-1">
            <button
              onClick={handleRandomize}
              disabled={isGenerating}
              className="px-2 py-1 rounded-full text-xs text-[#86868b] hover:text-[#0071e3] hover:bg-black/5 dark:hover:bg-white/10 flex items-center gap-1 transition-all active:scale-95 disabled:opacity-50"
              title="切换背景与格言"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isGenerating ? "animate-spin" : ""}`} />
              <span className="text-[11px] hidden xs:inline">换一张</span>
            </button>
            <button
              onClick={onClose}
              className="w-7 h-7 flex items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/10 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
              aria-label="关闭打卡卡片"
            >
              <X className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Card Preview with Retina Canvas Image */}
        <div className="w-full flex justify-center py-0.5">
          {imageUrl ? (
            <img
              src={imageUrl}
              alt="打卡分享卡片"
              className="max-h-[52vh] sm:max-h-[58vh] w-auto aspect-[3/4] object-cover rounded-2xl shadow-xl border border-black/[0.08] dark:border-white/[0.12] select-none pointer-events-auto"
            />
          ) : (
            <div className="w-full aspect-[3/4] max-h-[52vh] sm:max-h-[58vh] rounded-2xl bg-black/[0.04] dark:bg-white/[0.06] flex flex-col items-center justify-center gap-2 text-xs text-[#86868b]">
              <div className="w-6 h-6 border-2 border-[#0071e3] border-t-transparent rounded-full animate-spin" />
              <span>正在加载，请等候</span>
            </div>
          )}
        </div>

        <p className="text-[11px] text-[#86868b] text-center">
          手机端可长按图片直接存储至系统相册
        </p>

        {/* Action Buttons: 极简纯黑/浅灰 */}
        <div className="w-full flex items-center gap-2 pt-0.5">
          <button
            onClick={handleCopy}
            className="flex-1 inline-flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-full text-xs font-medium bg-black/[0.04] dark:bg-white/[0.08] hover:bg-black/[0.08] dark:hover:bg-white/[0.14] text-[#1d1d1f] dark:text-[#f5f5f7] transition-all active:scale-95"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-[#34c759]" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? "已复制文案" : "复制文字"}</span>
          </button>

          <button
            onClick={handleDownload}
            disabled={!imageUrl}
            className="flex-1 inline-flex items-center justify-center gap-1.5 py-2.5 px-3 rounded-full text-xs font-semibold bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] shadow-sm transition-all active:scale-95 disabled:opacity-50"
          >
            {downloadSuccess ? <Check className="w-3.5 h-3.5 text-[#34c759]" /> : <Download className="w-3.5 h-3.5" />}
            <span>{downloadSuccess ? "已保存图片" : "保存图片"}</span>
          </button>
        </div>
      </div>
    </div>
  );
}
