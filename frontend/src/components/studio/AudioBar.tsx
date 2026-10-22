"use client";

import React, { useState, useRef, useEffect } from "react";
import {
  Play,
  Pause,
  SkipBack,
  SkipForward,
  Repeat,
  Volume2,
  VolumeX,
} from "lucide-react";
import { LoopMode } from "@/hooks/useAudioPlayer";

interface AudioBarProps {
  currentIndex: number;
  totalSentences: number;
  isPlaying: boolean;
  loopMode: LoopMode;
  playbackRate: number;
  volume: number;
  onTogglePlay: () => void;
  onNext: () => void;
  onPrev: () => void;
  onCycleLoop: () => void;
  onSetSpeed: (speed: number) => void;
  onSetVolume: (vol: number) => void;
}

const SPEED_OPTIONS = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2];

export function AudioBar({
  currentIndex,
  totalSentences,
  isPlaying,
  loopMode,
  playbackRate,
  volume,
  onTogglePlay,
  onNext,
  onPrev,
  onCycleLoop,
  onSetSpeed,
  onSetVolume,
}: AudioBarProps) {
  const [isSpeedOpen, setIsSpeedOpen] = useState(false);
  const speedRef = useRef<HTMLDivElement | null>(null);

  // Click outside to close speed menu
  useEffect(() => {
    function handleClickOutside(e: MouseEvent) {
      if (speedRef.current && !speedRef.current.contains(e.target as Node)) {
        setIsSpeedOpen(false);
      }
    }
    if (isSpeedOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [isSpeedOpen]);

  const isLooping = loopMode !== "off";

  return (
    <div className="w-full max-w-xl mx-auto relative select-none">
      {/* Floating Frosted Glass Transport Bar */}
      <div className="flex items-center justify-between px-3 sm:px-5 py-2 bg-white/80 dark:bg-[#1c1c1e]/80 backdrop-blur-xl border border-black/[0.06] dark:border-white/[0.1] rounded-full shadow-[0_8px_30px_rgb(0,0,0,0.06)] dark:shadow-[0_8px_30px_rgb(0,0,0,0.4)]">
        {/* Left: Speed & Loop */}
        <div className="flex items-center gap-1 sm:gap-1.5">
          {/* Speed Selector Popover */}
          <div className="relative" ref={speedRef}>
            <button
              onClick={() => setIsSpeedOpen((prev) => !prev)}
              className="h-10 px-2.5 sm:px-3 flex items-center justify-center rounded-full text-xs font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 transition-colors"
              title="调节播放倍速"
            >
              {playbackRate.toFixed(1)}×
            </button>

            {isSpeedOpen && (
              <div className="absolute bottom-12 left-0 z-50 p-1.5 bg-white/95 dark:bg-[#2c2c2e]/95 backdrop-blur-xl border border-black/[0.08] dark:border-white/[0.12] rounded-2xl shadow-xl flex flex-col gap-0.5 min-w-[72px] animate-in fade-in zoom-in-95 duration-150">
                <div className="text-[10px] font-semibold px-2 py-1 text-[#86868b] dark:text-[#a1a1a6] text-center">
                  倍速
                </div>
                {SPEED_OPTIONS.map((spd) => (
                  <button
                    key={spd}
                    onClick={() => {
                      onSetSpeed(spd);
                      setIsSpeedOpen(false);
                    }}
                    className={`h-8 px-2.5 rounded-xl text-xs font-medium transition-colors text-center ${
                      playbackRate === spd
                        ? "bg-[#0071e3] text-white font-semibold"
                        : "text-[#1d1d1f] dark:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10"
                    }`}
                  >
                    {spd.toFixed(1)}×
                  </button>
                ))}
              </div>
            )}
          </div>

          {/* Single Sentence Loop */}
          <button
            onClick={onCycleLoop}
            className={`h-10 px-2.5 sm:px-3 flex items-center gap-1.5 rounded-full text-xs font-medium transition-colors ${
              isLooping
                ? "bg-[#0071e3]/10 text-[#0071e3] dark:bg-[#0a84ff]/20 dark:text-[#0a84ff] font-semibold"
                : "text-[#86868b] dark:text-[#a1a1a6] hover:bg-black/5 dark:hover:bg-white/10 hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
            }`}
            title="快捷键：R"
          >
            <Repeat className="w-3.5 h-3.5" />
            <span className="hidden sm:inline">单句循环</span>
          </button>
        </div>

        {/* Center: Transport Controls (Prev, Play/Pause, Next) */}
        <div className="flex items-center gap-1 sm:gap-2">
          {/* Previous Sentence */}
          <button
            onClick={onPrev}
            disabled={currentIndex <= 0}
            className="w-11 h-11 flex items-center justify-center rounded-full text-[#1d1d1f] dark:text-[#f5f5f7] disabled:opacity-20 hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all"
            title="上一句 (←)"
          >
            <SkipBack className="w-4 h-4 fill-current" />
          </button>

          {/* Primary Play / Pause Button */}
          <button
            onClick={onTogglePlay}
            className="w-12 h-12 flex items-center justify-center rounded-full bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] shadow-sm active:scale-95 transition-all"
            title="播放 / 暂停 (空格)"
          >
            {isPlaying ? (
              <Pause className="w-5 h-5 fill-current" />
            ) : (
              <Play className="w-5 h-5 fill-current ml-0.5" />
            )}
          </button>

          {/* Next Sentence */}
          <button
            onClick={onNext}
            disabled={currentIndex >= totalSentences - 1}
            className="w-11 h-11 flex items-center justify-center rounded-full text-[#1d1d1f] dark:text-[#f5f5f7] disabled:opacity-20 hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all"
            title="下一句 (→)"
          >
            <SkipForward className="w-4 h-4 fill-current" />
          </button>
        </div>

        {/* Right: Progress Indicator & Mute */}
        <div className="flex items-center gap-1 sm:gap-2">
          {/* Progress: 第 1 句 / 共 25 句 */}
          <div className="text-right text-[12px] sm:text-[13px] font-normal text-[#86868b] dark:text-[#a1a1a6] px-1 sm:px-2">
            <span className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">
              第 {currentIndex + 1} 句
            </span>
            <span className="hidden sm:inline"> / 共 {totalSentences} 句</span>
          </div>

          {/* Mute / Unmute Button */}
          <button
            onClick={() => onSetVolume(volume > 0 ? 0 : 1)}
            className="w-10 h-10 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:text-[#a1a1a6] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 transition-colors"
            title={volume === 0 ? "取消静音" : "静音"}
          >
            {volume === 0 ? (
              <VolumeX className="w-4 h-4 text-[#ff3b30]" />
            ) : (
              <Volume2 className="w-4 h-4" />
            )}
          </button>
        </div>
      </div>
    </div>
  );
}
