"use client";

import React from "react";
import { X, Keyboard } from "lucide-react";

interface KeyboardHelpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const SHORTCUTS = [
  { key: "空格", desc: "播放 / 暂停音频" },
  { key: "←", desc: "切换到上一句" },
  { key: "→", desc: "切换到下一句" },
  { key: "R", desc: "开启 / 关闭单句循环" },
  { key: "1", desc: "切换到【盲听】模式" },
  { key: "2", desc: "切换到【双语】模式" },
  { key: "3", desc: "切换到【听写】模式" },
  { key: "[  /  ]", desc: "减速 / 加速（0.7× – 1.2×）" },
  { key: "Esc", desc: "退出听写或关闭浮窗" },
];

export function KeyboardHelpModal({ isOpen, onClose }: KeyboardHelpModalProps) {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-sm p-4 animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div
        className="w-full max-w-sm bg-white dark:bg-[#1c1c1e] border border-black/[0.08] dark:border-white/[0.1] rounded-3xl shadow-2xl p-6 overflow-hidden animate-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between pb-3.5 border-b border-black/[0.06] dark:border-white/[0.08]">
          <div className="flex items-center gap-2">
            <Keyboard className="w-4 h-4 text-[#0071e3] dark:text-[#0a84ff]" />
            <h3 className="text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">快捷键指南</h3>
          </div>
          <button
            onClick={onClose}
            className="w-7 h-7 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 transition-colors"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="mt-3 divide-y divide-black/[0.04] dark:divide-white/[0.06] max-h-[60vh] overflow-y-auto">
          {SHORTCUTS.map((s, idx) => (
            <div key={idx} className="py-2.5 flex items-center justify-between text-xs">
              <span className="text-[#86868b] dark:text-[#a1a1a6]">{s.desc}</span>
              <kbd className="px-2 py-0.5 bg-black/[0.04] dark:bg-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7] font-mono font-medium rounded-md">
                {s.key}
              </kbd>
            </div>
          ))}
        </div>

        <div className="mt-4 pt-3 border-t border-black/[0.06] dark:border-white/[0.08] text-center">
          <p className="text-[11px] text-[#86868b]">专为纯键盘专注沉浸精听而设计</p>
        </div>
      </div>
    </div>
  );
}
