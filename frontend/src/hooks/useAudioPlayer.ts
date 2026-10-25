import { useState, useEffect, useRef, useCallback } from "react";
import { Sentence } from "@/lib/api";

export type LoopMode = "off" | "1x" | "3x" | "5x" | "infinity";

export interface UseAudioPlayerProps {
  audioUrl: string;
  sentences: Sentence[];
  initialIndex?: number;
  initialRate?: number;
  initialLoop?: LoopMode;
  onSentenceChange?: (index: number) => void;
  onSentenceComplete?: (index: number) => void;
}

export function useAudioPlayer({
  audioUrl,
  sentences,
  initialIndex = 0,
  initialRate = 1.0,
  initialLoop = "off",
  onSentenceChange,
  onSentenceComplete,
}: UseAudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [currentIndex, setCurrentIndex] = useState(initialIndex);
  const [isPlaying, setIsPlaying] = useState(false);
  const [isBuffering, setIsBuffering] = useState(false);
  const [isAutoplayBlocked, setIsAutoplayBlocked] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(initialRate);
  const [loopMode, setLoopMode] = useState<LoopMode>(initialLoop);
  const [loopCount, setLoopCount] = useState(0);
  const [volume, setVolume] = useState(1.0);
  const [isLoaded, setIsLoaded] = useState(false);

  const pendingSeekRef = useRef<number | null>(null);

  // Keep track of sentence change callback
  const onSentenceChangeRef = useRef(onSentenceChange);
  useEffect(() => {
    onSentenceChangeRef.current = onSentenceChange;
  }, [onSentenceChange]);

  const onSentenceCompleteRef = useRef(onSentenceComplete);
  useEffect(() => {
    onSentenceCompleteRef.current = onSentenceComplete;
  }, [onSentenceComplete]);

  // Initialize Audio
  useEffect(() => {
    const audio = new Audio(audioUrl);
    // Use metadata preload to avoid blocking or downloading 25MB upfront
    audio.preload = "metadata";
    audioRef.current = audio;

    const handleLoadedMetadata = () => {
      setIsLoaded(true);
      if (pendingSeekRef.current !== null) {
        audio.currentTime = Math.max(0, pendingSeekRef.current);
        pendingSeekRef.current = null;
      }
    };

    const handlePlay = () => {
      setIsPlaying(true);
      setIsAutoplayBlocked(false);
    };
    const handlePause = () => {
      setIsPlaying(false);
      setIsBuffering(false);
    };
    const handleWaiting = () => setIsBuffering(true);
    const handlePlaying = () => {
      setIsBuffering(false);
      setIsPlaying(true);
    };
    const handleCanPlay = () => setIsBuffering(false);

    audio.addEventListener("loadedmetadata", handleLoadedMetadata);
    audio.addEventListener("play", handlePlay);
    audio.addEventListener("pause", handlePause);
    audio.addEventListener("waiting", handleWaiting);
    audio.addEventListener("playing", handlePlaying);
    audio.addEventListener("canplay", handleCanPlay);

    return () => {
      audio.pause();
      audio.removeEventListener("loadedmetadata", handleLoadedMetadata);
      audio.removeEventListener("play", handlePlay);
      audio.removeEventListener("pause", handlePause);
      audio.removeEventListener("waiting", handleWaiting);
      audio.removeEventListener("playing", handlePlaying);
      audio.removeEventListener("canplay", handleCanPlay);
      audioRef.current = null;
    };
  }, [audioUrl]);

  // Update volume & playback rate
  useEffect(() => {
    if (audioRef.current) {
      audioRef.current.playbackRate = playbackRate;
      audioRef.current.volume = volume;
    }
  }, [playbackRate, volume]);

  const currentSentence = sentences[currentIndex] || null;

  const lastLoopTimeRef = useRef<number>(0);

  // Time boundary check loop
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !currentSentence) return;

    let animId: number;

    const checkBoundary = () => {
      if (isPlaying && audio.currentTime >= currentSentence.end_time) {
        const now = performance.now();
        // Prevent rapid re-triggering during seek buffer update (within 350ms)
        if (now - lastLoopTimeRef.current > 350) {
          lastLoopTimeRef.current = now;
          if (loopMode === "infinity" || loopMode === "1x" || loopMode === "3x" || loopMode === "5x") {
            // Replay current sentence in loop
            setLoopCount((prev) => prev + 1);
            audio.currentTime = Math.max(0, currentSentence.start_time - 0.05);
            audio.play().catch(() => {});
          } else {
            // Stop loop and pause
            audio.pause();
            setIsPlaying(false);
            setLoopCount(0);
            onSentenceCompleteRef.current?.(currentIndex);
          }
        }
      }
      animId = requestAnimationFrame(checkBoundary);
    };

    animId = requestAnimationFrame(checkBoundary);
    return () => cancelAnimationFrame(animId);
  }, [isPlaying, currentSentence, loopMode, loopCount, currentIndex]);

  const playSentence = useCallback(
    (index: number) => {
      const audio = audioRef.current;
      if (!audio || index < 0 || index >= sentences.length) return;

      const target = sentences[index];
      setCurrentIndex(index);
      setLoopCount(0);
      onSentenceChangeRef.current?.(index);

      const targetTime = Math.max(0, target.start_time - 0.05);
      if (audio.readyState >= 1) {
        audio.currentTime = targetTime;
      } else {
        pendingSeekRef.current = targetTime;
      }

      const p = audio.play();
      if (p !== undefined) {
        p.then(() => {
          setIsPlaying(true);
          setIsAutoplayBlocked(false);
        }).catch((err) => {
          if (err?.name === "NotAllowedError") {
            setIsAutoplayBlocked(true);
          }
          setIsPlaying(false);
        });
      }
    },
    [sentences]
  );

  const togglePlay = useCallback(() => {
    const audio = audioRef.current;
    if (!audio || !currentSentence) return;

    if (isPlaying) {
      audio.pause();
      setIsPlaying(false);
    } else {
      const targetTime = Math.max(0, currentSentence.start_time - 0.05);
      if (audio.readyState >= 1) {
        if (audio.currentTime >= currentSentence.end_time || audio.currentTime < currentSentence.start_time) {
          audio.currentTime = targetTime;
        }
      } else {
        pendingSeekRef.current = targetTime;
      }

      const p = audio.play();
      if (p !== undefined) {
        p.then(() => {
          setIsPlaying(true);
          setIsAutoplayBlocked(false);
        }).catch((err) => {
          if (err?.name === "NotAllowedError") {
            setIsAutoplayBlocked(true);
          }
          setIsPlaying(false);
        });
      }
    }
  }, [isPlaying, currentSentence]);

  const replay = useCallback(() => {
    playSentence(currentIndex);
  }, [playSentence, currentIndex]);

  const nextSentence = useCallback(() => {
    if (currentIndex < sentences.length - 1) {
      playSentence(currentIndex + 1);
    }
  }, [currentIndex, sentences.length, playSentence]);

  const prevSentence = useCallback(() => {
    if (currentIndex > 0) {
      playSentence(currentIndex - 1);
    }
  }, [currentIndex, playSentence]);

  const toggleLoopMode = useCallback(() => {
    setLoopMode((prev) => {
      const nextMode = prev === "off" ? "infinity" : "off";
      // If user turns ON loop and audio was paused at or past the end of the sentence, replay immediately!
      if (nextMode === "infinity" && audioRef.current && currentSentence) {
        if (audioRef.current.currentTime >= currentSentence.end_time || audioRef.current.paused) {
          audioRef.current.currentTime = Math.max(0, currentSentence.start_time - 0.05);
          audioRef.current.play().then(() => setIsPlaying(true)).catch(() => {});
        }
      }
      return nextMode;
    });
    setLoopCount(0);
  }, [currentSentence]);

  const cycleLoopMode = toggleLoopMode;

  const adjustSpeed = useCallback((delta: number) => {
    setPlaybackRate((prev) => {
      const newRate = Math.round((prev + delta) * 10) / 10;
      return Math.min(1.2, Math.max(0.7, newRate));
    });
  }, []);

  const adjustVolume = useCallback((delta: number) => {
    setVolume((prev) => {
      const newVol = Math.round((prev + delta) * 10) / 10;
      return Math.min(1.0, Math.max(0.0, newVol));
    });
  }, []);

  return {
    currentIndex,
    currentSentence,
    isPlaying,
    isBuffering,
    isAutoplayBlocked,
    playbackRate,
    loopMode,
    volume,
    isLoaded,
    playSentence,
    togglePlay,
    replay,
    nextSentence,
    prevSentence,
    cycleLoopMode,
    setPlaybackRate,
    adjustSpeed,
    adjustVolume,
  };
}
