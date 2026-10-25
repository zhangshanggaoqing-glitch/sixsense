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
import { LoopMode, PlaybackPace } from "@/hooks/useAudioPlayer";

interface AudioBarProps {
  currentIndex: number;
  totalSentences: number;
  isPlaying: boolean;
  loopMode: LoopMode;
  playbackPace: PlaybackPace;
  playbackRate: number;
  volume: number;
  onTogglePlay: () => void;
  onNext: () => void;
  onPrev: () => void;
  onCycleLoop: () => void;
  onSetPace: (pace: PlaybackPace) => void;
  onSetSpeed: (speed: number) => void;
  onSetVolume: (vol: number) => void;
  onOpenPunchCard?: () => void;
}

const SPEED_OPTIONS = [0.7, 0.8, 0.9, 1.0, 1.1, 1.2];

export function AudioBar({
  currentIndex,
  totalSentences,
  isPlaying,
  loopMode,
  playbackPace,
  playbackRate,
  volume,
  onTogglePlay,
  onNext,
  onPrev,
  onCycleLoop,
  onSetPace,
  onSetSpeed,
  onSetVolume,
  onOpenPunchCard,
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
    <div className="w-full max-w-3xl mx-auto relative select-none touch-manipulation">
      {/* Floating Frosted Glass Transport Bar */}
      <div className="flex items-center justify-between px-3 sm:px-6 py-2 sm:py-2.5 bg-white/85 dark:bg-[#1c1c1e]/85 backdrop-blur-2xl border border-black/[0.06] dark:border-white/[0.1] rounded-full shadow-[0_8px_30px_rgb(0,0,0,0.06)] dark:shadow-[0_8px_30px_rgb(0,0,0,0.4)]">
        {/* Left: Speed, Loop & Pace */}
        <div className="flex items-center gap-1 sm:gap-2 shrink-0">
          {/* Speed Selector Popover */}
          <div className="relative shrink-0" ref={speedRef}>
            <button
              type="button"
              onClick={() => setIsSpeedOpen((prev) => !prev)}
              className="h-9 px-2 sm:px-2.5 flex items-center justify-center rounded-full text-xs font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0 whitespace-nowrap"
              title="调节播放倍速"
            >
              {playbackRate.toFixed(1)}×
            </button>

            {isSpeedOpen && (
              <div className="absolute bottom-12 left-0 z-50 p-1.5 bg-white/95 dark:bg-[#2c2c2e]/95 backdrop-blur-xl border border-black/[0.08] dark:border-white/[0.12] rounded-2xl shadow-xl flex flex-col gap-0.5 min-w-[72px] animate-in fade-in zoom-in-95 duration-150">
                <div className="text-[10px] font-semibold px-2 py-1 text-[#86868b] dark:text-[#a1a1a6] text-center whitespace-nowrap">
                  倍速
                </div>
                {SPEED_OPTIONS.map((spd) => (
                  <button
                    key={spd}
                    type="button"
                    onClick={() => {
                      onSetSpeed(spd);
                      setIsSpeedOpen(false);
                    }}
                    className={`h-8 px-2.5 rounded-xl text-xs font-medium transition-colors text-center whitespace-nowrap ${
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
            type="button"
            onClick={(e) => {
              e.preventDefault();
              e.stopPropagation();
              onCycleLoop();
            }}
            className={`h-9 px-2.5 sm:px-3 flex items-center justify-center gap-1.5 rounded-full text-xs font-medium transition-all active:scale-95 shrink-0 whitespace-nowrap ${
              isLooping
                ? "bg-[#0071e3]/10 text-[#0071e3] dark:bg-[#0a84ff]/20 dark:text-[#0a84ff] font-semibold ring-1 ring-[#0071e3]/20"
                : "text-[#86868b] dark:text-[#a1a1a6] hover:bg-black/5 dark:hover:bg-white/10 hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
            }`}
            title={isLooping ? "单句循环已开启 (快捷键 R)" : "开启单句循环 (快捷键 R)"}
          >
            <Repeat className="w-3.5 h-3.5 shrink-0" />
            <span className="hidden sm:inline whitespace-nowrap">单句循环</span>
          </button>

          {/* Playback Pace: 一句一停 (默认) | 连贯播放 */}
          {/* Desktop/Tablet: Segmented Control (两态文案：一句一停 | 连贯播放，当前态用黑底小 pill 标出) */}
          <div className="hidden sm:inline-flex items-center p-0.5 bg-black/[0.04] dark:bg-white/[0.06] rounded-full text-[11px] font-medium shrink-0 whitespace-nowrap ml-0.5">
            <button
              type="button"
              onClick={() => onSetPace("pause_each")}
              className={`px-2.5 sm:px-3 py-1 rounded-full transition-all active:scale-95 whitespace-nowrap ${
                playbackPace === "pause_each"
                  ? "bg-[#1d1d1f] text-white dark:bg-[#f5f5f7] dark:text-[#1d1d1f] font-semibold shadow-xs"
                  : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              }`}
              title="说一句停一句：当前句播完后暂停，等点击下一句"
            >
              一句一停
            </button>
            <button
              type="button"
              onClick={() => onSetPace("continuous")}
              className={`px-2.5 sm:px-3 py-1 rounded-full transition-all active:scale-95 whitespace-nowrap ${
                playbackPace === "continuous"
                  ? "bg-[#1d1d1f] text-white dark:bg-[#f5f5f7] dark:text-[#1d1d1f] font-semibold shadow-xs"
                  : "text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              }`}
              title="连贯播放：当前句播完后自动进入下一句并继续播放"
            >
              连贯播放
            </button>
          </div>

          {/* Mobile: Compact Pace Switcher */}
          <button
            type="button"
            onClick={() => onSetPace(playbackPace === "pause_each" ? "continuous" : "pause_each")}
            className="sm:hidden h-9 px-2 flex items-center justify-center rounded-full text-[11px] font-medium text-[#1d1d1f] dark:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all shrink-0 whitespace-nowrap"
            title={playbackPace === "pause_each" ? "当前：一句一停 (点击切为连贯播放)" : "当前：连贯播放 (点击切为一句一停)"}
          >
            <span className={playbackPace === "continuous" ? "font-semibold text-[#0071e3] dark:text-[#0a84ff]" : "font-medium text-[#86868b] dark:text-[#a1a1a6]"}>
              {playbackPace === "pause_each" ? "一句一停" : "连贯"}
            </span>
          </button>
        </div>

        {/* Center: Transport Controls (Prev, Play/Pause, Next) */}
        <div className="flex items-center gap-1 sm:gap-2 shrink-0">
          {/* Previous Sentence */}
          <button
            type="button"
            onClick={onPrev}
            disabled={currentIndex <= 0}
            className="w-9 h-9 sm:w-10 sm:h-10 flex items-center justify-center rounded-full text-[#1d1d1f] dark:text-[#f5f5f7] disabled:opacity-20 hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all shrink-0"
            title="上一句 (←)"
          >
            <SkipBack className="w-4 h-4 fill-current" />
          </button>

          {/* Primary Play / Pause Button */}
          <button
            type="button"
            onClick={onTogglePlay}
            className="w-11 h-11 sm:w-12 sm:h-12 flex items-center justify-center rounded-full bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] shadow-md active:scale-95 transition-all shrink-0"
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
            type="button"
            onClick={onNext}
            disabled={currentIndex >= totalSentences - 1}
            className="w-9 h-9 sm:w-10 sm:h-10 flex items-center justify-center rounded-full text-[#1d1d1f] dark:text-[#f5f5f7] disabled:opacity-20 hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all shrink-0"
            title="下一句 (→)"
          >
            <SkipForward className="w-4 h-4 fill-current" />
          </button>
        </div>

        {/* Right: Weak punch button + Progress Indicator & Mute */}
        <div className="flex items-center gap-1 sm:gap-2 shrink-0 justify-end">
          {/* Punch card trigger (stable pill, hidden on small mobile) */}
          {onOpenPunchCard && (
            <button
              type="button"
              onClick={onOpenPunchCard}
              className="hidden md:inline-flex items-center px-2.5 py-1 text-xs font-medium text-[#86868b] hover:text-[#0071e3] dark:hover:text-[#0a84ff] rounded-full hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0 whitespace-nowrap"
              title="生成今日打卡图"
            >
              打卡
            </button>
          )}

          {/* Progress: 第 1 句 / 共 25 句 */}
          <div className="text-right text-xs font-normal text-[#86868b] dark:text-[#a1a1a6] px-1 shrink-0 whitespace-nowrap">
            <span className="font-semibold text-[#1d1d1f] dark:text-[#f5f5f7] whitespace-nowrap">
              第 {currentIndex + 1} 句
            </span>
            <span className="hidden sm:inline whitespace-nowrap"> / 共 {totalSentences} 句</span>
          </div>

          {/* Mute / Unmute Button */}
          <button
            type="button"
            onClick={() => onSetVolume(volume > 0 ? 0 : 1)}
            className="w-9 h-9 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:text-[#a1a1a6] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 transition-colors shrink-0"
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
