"use client";

import React, { useState, useEffect, useRef, useCallback } from "react";
import {
  Play,
  Pause,
  RotateCcw,
  RotateCw,
  Download,
  Volume2,
  VolumeX,
} from "lucide-react";

interface FullAudioBarProps {
  audioSrc: string;
  downloadUrl: string;
  title: string;
  defaultDuration?: number;
}

const SPEED_OPTIONS = [0.75, 1.0, 1.25, 1.5];

function formatTime(seconds: number): string {
  if (isNaN(seconds) || seconds < 0) return "00:00";
  const m = Math.floor(seconds / 60);
  const s = Math.floor(seconds % 60);
  return `${String(m).padStart(2, "0")}:${String(s).padStart(2, "0")}`;
}

export function FullAudioBar({
  audioSrc,
  downloadUrl,
  title,
  defaultDuration = 0,
}: FullAudioBarProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);

  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(defaultDuration);
  const [playbackRate, setPlaybackRate] = useState(1.0);
  const [isMuted, setIsMuted] = useState(false);
  const [isSeeking, setIsSeeking] = useState(false);
  const [seekTime, setSeekTime] = useState(0);

  // Sync defaultDuration when loaded
  useEffect(() => {
    if (defaultDuration > 0 && duration === 0) {
      setDuration(defaultDuration);
    }
  }, [defaultDuration, duration]);

  // Audio event listeners
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const onLoadedMetadata = () => {
      if (audio.duration && !isNaN(audio.duration) && audio.duration !== Infinity) {
        setDuration(audio.duration);
      }
    };

    const onTimeUpdate = () => {
      if (!isSeeking) {
        setCurrentTime(audio.currentTime);
      }
    };

    const onEnded = () => {
      setIsPlaying(false);
    };

    const onPlay = () => setIsPlaying(true);
    const onPause = () => setIsPlaying(false);

    audio.addEventListener("loadedmetadata", onLoadedMetadata);
    audio.addEventListener("timeupdate", onTimeUpdate);
    audio.addEventListener("ended", onEnded);
    audio.addEventListener("play", onPlay);
    audio.addEventListener("pause", onPause);

    return () => {
      audio.removeEventListener("loadedmetadata", onLoadedMetadata);
      audio.removeEventListener("timeupdate", onTimeUpdate);
      audio.removeEventListener("ended", onEnded);
      audio.removeEventListener("play", onPlay);
      audio.removeEventListener("pause", onPause);
    };
  }, [isSeeking]);

  // Handle Play / Pause toggle
  const togglePlay = useCallback(() => {
    const audio = audioRef.current;
    if (!audio) return;
    if (audio.paused) {
      audio.play().catch((err) => console.error("Play error:", err));
    } else {
      audio.pause();
    }
  }, []);

  // Jump relative seconds
  const jumpTime = useCallback((delta: number) => {
    const audio = audioRef.current;
    if (!audio) return;
    const target = Math.max(0, Math.min(audio.duration || duration, audio.currentTime + delta));
    audio.currentTime = target;
    setCurrentTime(target);
  }, [duration]);

  // Handle speed cycle
  const cycleSpeed = useCallback(() => {
    const idx = SPEED_OPTIONS.indexOf(playbackRate);
    const nextRate = idx >= 0 && idx + 1 < SPEED_OPTIONS.length ? SPEED_OPTIONS[idx + 1] : SPEED_OPTIONS[0];
    setPlaybackRate(nextRate);
    if (audioRef.current) {
      audioRef.current.playbackRate = nextRate;
    }
  }, [playbackRate]);

  // Scrubbing handlers
  const handleSeekChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setSeekTime(parseFloat(e.target.value));
  };

  const handleSeekEnd = () => {
    const audio = audioRef.current;
    if (audio) {
      audio.currentTime = seekTime;
      setCurrentTime(seekTime);
    }
    setIsSeeking(false);
  };

  // Keyboard shortcuts (Space = Play/Pause, ArrowLeft = -5s, ArrowRight = +5s)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const activeTag = (document.activeElement?.tagName || "").toLowerCase();
      if (activeTag === "input" || activeTag === "textarea") return;

      if (e.code === "Space") {
        e.preventDefault();
        togglePlay();
      } else if (e.code === "ArrowLeft") {
        e.preventDefault();
        jumpTime(-5);
      } else if (e.code === "ArrowRight") {
        e.preventDefault();
        jumpTime(5);
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [togglePlay, jumpTime]);

  const activeTime = isSeeking ? seekTime : currentTime;
  const progressPercent = duration > 0 ? (activeTime / duration) * 100 : 0;

  return (
    <div className="w-full max-w-4xl mx-auto">
      {/* Hidden native audio element */}
      <audio
        ref={audioRef}
        src={audioSrc}
        preload="metadata"
      />

      <div className="bg-white/90 dark:bg-[#1c1c1e]/90 backdrop-blur-xl border border-black/[0.08] dark:border-white/[0.1] rounded-2xl sm:rounded-3xl shadow-[0_8px_32px_rgba(0,0,0,0.08)] px-4 sm:px-6 py-3 sm:py-3.5 space-y-2">
        {/* Progress Bar & Scrubber */}
        <div className="flex items-center gap-3">
          <span className="text-[11px] font-mono font-medium text-[#86868b] min-w-[36px] text-right">
            {formatTime(activeTime)}
          </span>

          <div className="relative flex-1 flex items-center group py-1">
            {/* Visual background track */}
            <div className="w-full h-1.5 sm:h-2 bg-black/[0.06] dark:bg-white/[0.1] rounded-full overflow-hidden">
              <div
                className="h-full bg-[#1d1d1f] dark:bg-[#f5f5f7] rounded-full transition-[width] duration-75"
                style={{ width: `${progressPercent}%` }}
              />
            </div>

            {/* Native range slider for smooth touch/click scrub */}
            <input
              type="range"
              min={0}
              max={duration || 100}
              step={0.1}
              value={activeTime}
              onChange={handleSeekChange}
              onMouseDown={() => setIsSeeking(true)}
              onMouseUp={handleSeekEnd}
              onTouchStart={() => setIsSeeking(true)}
              onTouchEnd={handleSeekEnd}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
              aria-label="音频进度条"
            />
          </div>

          <span className="text-[11px] font-mono font-medium text-[#86868b] min-w-[36px]">
            {formatTime(duration)}
          </span>
        </div>

        {/* Playback Controls Row */}
        <div className="flex items-center justify-between gap-2 pt-0.5">
          {/* Left tools: Speed + Download */}
          <div className="flex items-center gap-1.5 sm:gap-2">
            <button
              onClick={cycleSpeed}
              className="px-2.5 py-1 rounded-full text-xs font-semibold bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.08] dark:hover:bg-white/[0.1] text-[#1d1d1f] dark:text-[#f5f5f7] active:scale-95 transition-all"
              title="切换播放倍速"
            >
              {playbackRate.toFixed(2).replace(/\.00$/, "")}×
            </button>

            <a
              href={downloadUrl}
              download
              className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-xs font-medium text-[#0071e3] dark:text-[#0a84ff] bg-[#0071e3]/10 dark:bg-[#0a84ff]/15 hover:bg-[#0071e3]/20 active:scale-95 transition-all"
              title="下载本套完整听力音频 MP3"
            >
              <Download className="w-3.5 h-3.5" />
              <span className="hidden xs:inline">下载音频</span>
            </a>
          </div>

          {/* Center Playback Controls */}
          <div className="flex items-center gap-2 sm:gap-4">
            <button
              onClick={() => jumpTime(-10)}
              className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all"
              title="快退 10 秒"
            >
              <RotateCcw className="w-4 h-4" />
            </button>

            <button
              onClick={togglePlay}
              className="w-11 h-11 sm:w-12 sm:h-12 flex items-center justify-center rounded-full bg-[#1d1d1f] hover:bg-black dark:bg-[#f5f5f7] dark:hover:bg-white text-white dark:text-[#1d1d1f] shadow-md active:scale-95 transition-all"
              title={isPlaying ? "暂停 (空格)" : "播放 (空格)"}
            >
              {isPlaying ? (
                <Pause className="w-5 h-5 fill-current" />
              ) : (
                <Play className="w-5 h-5 fill-current ml-0.5" />
              )}
            </button>

            <button
              onClick={() => jumpTime(10)}
              className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all"
              title="快进 10 秒"
            >
              <RotateCw className="w-4 h-4" />
            </button>
          </div>

          {/* Right Info: Mute & Label */}
          <div className="flex items-center gap-2">
            <button
              onClick={() => {
                if (audioRef.current) {
                  audioRef.current.muted = !isMuted;
                  setIsMuted(!isMuted);
                }
              }}
              className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all"
              title={isMuted ? "取消静音" : "静音"}
            >
              {isMuted ? <VolumeX className="w-4 h-4" /> : <Volume2 className="w-4 h-4" />}
            </button>

            <span className="text-[11px] text-[#86868b] hidden sm:inline truncate max-w-[140px]">
              {title}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}
