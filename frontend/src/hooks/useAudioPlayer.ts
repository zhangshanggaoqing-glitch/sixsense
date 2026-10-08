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
}

export function useAudioPlayer({
  audioUrl,
  sentences,
  initialIndex = 0,
  initialRate = 1.0,
  initialLoop = "off",
  onSentenceChange,
}: UseAudioPlayerProps) {
  const audioRef = useRef<HTMLAudioElement | null>(null);
  const [currentIndex, setCurrentIndex] = useState(initialIndex);
  const [isPlaying, setIsPlaying] = useState(false);
  const [playbackRate, setPlaybackRate] = useState(initialRate);
  const [loopMode, setLoopMode] = useState<LoopMode>(initialLoop);
  const [loopCount, setLoopCount] = useState(0);
  const [volume, setVolume] = useState(1.0);
  const [isLoaded, setIsLoaded] = useState(false);

  // Keep track of sentence change callback
  const onSentenceChangeRef = useRef(onSentenceChange);
  useEffect(() => {
    onSentenceChangeRef.current = onSentenceChange;
  }, [onSentenceChange]);

  // Initialize Audio
  useEffect(() => {
    const audio = new Audio(audioUrl);
    audio.preload = "auto";
    audioRef.current = audio;

    const handleLoadedMetadata = () => {
      setIsLoaded(true);
    };

    const handlePlay = () => setIsPlaying(true);
    const handlePause = () => setIsPlaying(false);

    audio.addEventListener("loadedmetadata", handleLoadedMetadata);
    audio.addEventListener("play", handlePlay);
    audio.addEventListener("pause", handlePause);

    return () => {
      audio.pause();
      audio.removeEventListener("loadedmetadata", handleLoadedMetadata);
      audio.removeEventListener("play", handlePlay);
      audio.removeEventListener("pause", handlePause);
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

  // Time boundary check loop
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio || !currentSentence) return;

    let animId: number;

    const checkBoundary = () => {
      if (isPlaying && audio.currentTime >= currentSentence.end_time) {
        // Sentence finished!
        const maxLoops =
          loopMode === "1x" ? 1 : loopMode === "3x" ? 3 : loopMode === "5x" ? 5 : loopMode === "infinity" ? Infinity : 0;

        if (maxLoops > 0 && loopCount + 1 < maxLoops) {
          // Replay current sentence in loop
          setLoopCount((prev) => prev + 1);
          audio.currentTime = Math.max(0, currentSentence.start_time - 0.05);
          audio.play().catch(() => {});
        } else {
          // Stop loop and pause
          audio.pause();
          setIsPlaying(false);
          setLoopCount(0);
        }
      }
      animId = requestAnimationFrame(checkBoundary);
    };

    animId = requestAnimationFrame(checkBoundary);
    return () => cancelAnimationFrame(animId);
  }, [isPlaying, currentSentence, loopMode, loopCount]);

  const playSentence = useCallback(
    (index: number) => {
      const audio = audioRef.current;
      if (!audio || index < 0 || index >= sentences.length) return;

      const target = sentences[index];
      setCurrentIndex(index);
      setLoopCount(0);
      onSentenceChangeRef.current?.(index);

      // Start slightly before boundary to avoid cutting initial consonants
      audio.currentTime = Math.max(0, target.start_time - 0.05);
      audio.play().then(() => setIsPlaying(true)).catch(() => {});
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
      if (audio.currentTime >= currentSentence.end_time || audio.currentTime < currentSentence.start_time) {
        audio.currentTime = Math.max(0, currentSentence.start_time - 0.05);
      }
      audio.play().then(() => setIsPlaying(true)).catch(() => {});
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

  const cycleLoopMode = useCallback(() => {
    const modes: LoopMode[] = ["off", "1x", "3x", "5x", "infinity"];
    setLoopMode((prev) => {
      const nextIdx = (modes.indexOf(prev) + 1) % modes.length;
      return modes[nextIdx];
    });
    setLoopCount(0);
  }, []);

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
