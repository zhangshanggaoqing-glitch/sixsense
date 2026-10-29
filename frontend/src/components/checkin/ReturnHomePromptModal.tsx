"use client";

import React, { useEffect } from "react";
import { X, Sparkles, ArrowRight } from "lucide-react";

interface ReturnHomePromptModalProps {
  isOpen: boolean;
  onClose: () => void;
  onConfirmPunch: () => void;
  sessionMinutes: number;
  completedRatio: number;
}

export function ReturnHomePromptModal({
  isOpen,
  onClose,
  onConfirmPunch,
  sessionMinutes,
  completedRatio,
}: ReturnHomePromptModalProps) {
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

  const percent = Math.min(100, Math.round(completedRatio * 100));

  return (
    <div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center p-3 sm:p-4 bg-black/40 backdrop-blur-sm animate-in fade-in duration-200"
      onClick={onClose}
    >
      <div
        className="relative w-full max-w-sm sm:max-w-md bg-white dark:bg-[#1c1c1e] rounded-t-3xl sm:rounded-3xl shadow-2xl p-5 sm:p-6 flex flex-col gap-4 border border-black/[0.08] dark:border-white/[0.12] animate-in slide-in-from-bottom-4 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top Header */}
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-full bg-[#0071e3]/10 dark:bg-[#0a84ff]/20 flex items-center justify-center text-[#0071e3] dark:text-[#0a84ff]">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
                本次精听已达标
              </h3>
              <p className="text-[11px] text-[#86868b]">
                本次有效练习 {sessionMinutes.toFixed(1)} 分钟{percent > 0 ? ` · 进度 ${percent}%` : ""}
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="w-7 h-7 flex items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/10 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
            aria-label="关闭"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <div className="text-xs text-[#86868b] dark:text-[#a1a1a6] leading-relaxed">
          你刚刚完成了一次认真的精听训练，已达成今日打卡标准。是否打卡记录今天的努力，并生成今日专属分享卡片？
        </div>

        {/* Action Buttons */}
        <div className="flex items-center gap-2.5 pt-1">
          <button
            onClick={onClose}
            className="flex-1 py-2.5 px-3 rounded-full text-xs font-medium bg-black/[0.04] dark:bg-white/[0.08] hover:bg-black/[0.08] dark:hover:bg-white/[0.14] text-[#1d1d1f] dark:text-[#f5f5f7] transition-all active:scale-95 text-center"
          >
            稍后再说
          </button>

          <button
            onClick={onConfirmPunch}
            className="flex-1 inline-flex items-center justify-center gap-1.5 py-2.5 px-4 rounded-full text-xs font-semibold bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] shadow-sm transition-all active:scale-95"
          >
            <span>打卡并分享</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
}
