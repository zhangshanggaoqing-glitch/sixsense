"use client";

import React from "react";
import {
  Play,
  Pause,
  RotateCcw,
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
  onReplay: () => void;
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
  onReplay,
  onNext,
  onPrev,
  onCycleLoop,
  onSetSpeed,
  onSetVolume,
}: AudioBarProps) {
  return (
    <div className="w-full max-w-2xl mx-auto flex items-center justify-between px-6 py-3.5 bg-white/80 dark:bg-[#151821]/80 backdrop-blur-md border border-gray-200/80 dark:border-gray-800/80 rounded-2xl shadow-lg">
      {/* Left: Speed & Loop controls */}
      <div className="flex items-center gap-2">
        {/* Speed toggle dropdown/button */}
        <div className="flex items-center bg-gray-100 dark:bg-gray-800/80 rounded-lg p-0.5 text-xs font-mono">
          {SPEED_OPTIONS.map((spd) => (
            <button
              key={spd}
              onClick={() => onSetSpeed(spd)}
              className={`px-2 py-1 rounded-md transition-all ${
                playbackRate === spd
                  ? "bg-white dark:bg-gray-700 text-blue-600 dark:text-blue-400 font-bold shadow-xs"
                  : "text-gray-500 hover:text-gray-800 dark:hover:text-gray-200"
              }`}
            >
              {spd}×
            </button>
          ))}
        </div>

        {/* Loop mode badge */}
        <button
          onClick={onCycleLoop}
          className={`flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all ${
            loopMode !== "off"
              ? "bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 border border-blue-200 dark:border-blue-900"
              : "text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          }`}
          title="Cycle Sentence Loop (L)"
        >
          <Repeat className="w-3.5 h-3.5" />
          <span>{loopMode === "off" ? "Loop" : loopMode}</span>
        </button>
      </div>

      {/* Center: Playback Transport Buttons */}
      <div className="flex items-center gap-3">
        <button
          onClick={onPrev}
          disabled={currentIndex <= 0}
          className="p-2 text-gray-500 hover:text-gray-900 dark:hover:text-gray-100 disabled:opacity-30 transition-colors"
          title="Previous Sentence (←)"
        >
          <SkipBack className="w-5 h-5" />
        </button>

        <button
          onClick={onReplay}
          className="p-2 text-gray-500 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
          title="Replay Sentence (R)"
        >
          <RotateCcw className="w-4 h-4" />
        </button>

        <button
          onClick={onTogglePlay}
          className="w-12 h-12 flex items-center justify-center bg-gray-900 hover:bg-gray-800 dark:bg-white dark:hover:bg-gray-100 text-white dark:text-gray-900 rounded-full shadow-md transition-transform active:scale-95"
          title="Play / Pause (Space)"
        >
          {isPlaying ? <Pause className="w-5 h-5 fill-current" /> : <Play className="w-5 h-5 fill-current ml-0.5" />}
        </button>

        <button
          onClick={onNext}
          disabled={currentIndex >= totalSentences - 1}
          className="p-2 text-gray-500 hover:text-gray-900 dark:hover:text-gray-100 disabled:opacity-30 transition-colors"
          title="Next Sentence (→)"
        >
          <SkipForward className="w-5 h-5" />
        </button>
      </div>

      {/* Right: Sentence Progress Indicator & Volume */}
      <div className="flex items-center gap-3">
        <div className="text-right">
          <span className="font-mono text-sm font-semibold text-gray-800 dark:text-gray-200">
            {currentIndex + 1}
          </span>
          <span className="text-xs text-gray-400 font-mono ml-1">/ {totalSentences}</span>
        </div>

        {/* Volume toggle */}
        <button
          onClick={() => onSetVolume(volume > 0 ? 0 : 1)}
          className="text-gray-400 hover:text-gray-600 dark:hover:text-gray-300"
          title="Toggle Volume Mute"
        >
          {volume === 0 ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
        </button>
      </div>
    </div>
  );
}
