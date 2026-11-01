"use client";

import React, { useEffect } from "react";
import { X } from "lucide-react";

export const MIGRATE_NOTICE_STORAGE_KEY = "mystone_server_migrate_notice_v1";

export function hasSeenMigrateNotice(): boolean {
  if (typeof window === "undefined") return true;
  try {
    return Boolean(localStorage.getItem(MIGRATE_NOTICE_STORAGE_KEY));
  } catch {
    return true;
  }
}

export function markMigrateNoticeSeen(): void {
  if (typeof window === "undefined") return;
  try {
    localStorage.setItem(MIGRATE_NOTICE_STORAGE_KEY, "true");
  } catch {}
}

interface ServerMigrateNoticeModalProps {
  isOpen: boolean;
  onClose: () => void;
  onGoRegister: () => void;
}

export function ServerMigrateNoticeModal({
  isOpen,
  onClose,
  onGoRegister,
}: ServerMigrateNoticeModalProps) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape" && isOpen) {
        markMigrateNoticeSeen();
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  const handleDismiss = () => {
    markMigrateNoticeSeen();
    onClose();
  };

  const handleRegister = () => {
    markMigrateNoticeSeen();
    onGoRegister();
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-in fade-in duration-200 select-none"
      onClick={handleDismiss}
    >
      <div
        className="relative w-full max-w-sm sm:max-w-md bg-white dark:bg-[#1c1c1e] rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.12)] p-6 sm:p-7 flex flex-col gap-4 border border-black/[0.06] dark:border-white/[0.08] animate-in zoom-in-95 duration-200"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Top Header */}
        <div className="flex items-center justify-between">
          <h3 className="text-base sm:text-lg font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] tracking-tight">
            服务迁移说明
          </h3>
          <button
            type="button"
            onClick={handleDismiss}
            className="w-7 h-7 flex items-center justify-center rounded-full hover:bg-black/5 dark:hover:bg-white/10 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
            aria-label="关闭"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Content Body */}
        <p className="text-xs sm:text-[13px] text-[#86868b] dark:text-[#a1a1a6] leading-relaxed">
          因云服务器调整，此前账号与学习进度暂时无法自动同步。请重新注册一个账号后再使用；注册后生词本与做题进度将正常永久保存。对由此带来的不便，我们深表歉意。
        </p>

        {/* Action Buttons */}
        <div className="flex items-center gap-2.5 pt-2">
          <button
            type="button"
            onClick={handleDismiss}
            className="flex-1 py-2.5 px-3 rounded-full text-xs font-medium bg-black/[0.04] dark:bg-white/[0.08] hover:bg-black/[0.08] dark:hover:bg-white/[0.14] text-[#1d1d1f] dark:text-[#f5f5f7] transition-all active:scale-95 text-center"
          >
            我知道了
          </button>
          <button
            type="button"
            onClick={handleRegister}
            className="flex-1 py-2.5 px-4 rounded-full text-xs font-semibold bg-[#0071e3] hover:bg-[#0077ed] text-white shadow-sm transition-all active:scale-95 text-center"
          >
            去注册
          </button>
        </div>
      </div>
    </div>
  );
}
