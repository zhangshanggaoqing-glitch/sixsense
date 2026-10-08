import { useEffect } from "react";

export interface ShortcutHandlers {
  onTogglePlay: () => void;
  onReplay: () => void;
  onNext: () => void;
  onPrev: () => void;
  onToggleLoop: () => void;
  onToggleEnglish: () => void;
  onToggleTranslation: () => void;
  onToggleDictation: () => void;
  onSpeedDown: () => void;
  onSpeedUp: () => void;
  onVolumeUp: () => void;
  onVolumeDown: () => void;
  onToggleHelp: () => void;
  isDictating?: boolean;
}

export function useKeyboardShortcuts({
  onTogglePlay,
  onReplay,
  onNext,
  onPrev,
  onToggleLoop,
  onToggleEnglish,
  onToggleTranslation,
  onToggleDictation,
  onSpeedDown,
  onSpeedUp,
  onVolumeUp,
  onVolumeDown,
  onToggleHelp,
  isDictating = false,
}: ShortcutHandlers) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isInputFocused =
        target.tagName === "INPUT" || target.tagName === "TEXTAREA" || target.isContentEditable;

      // In dictation mode, allow Esc to exit dictation
      if (isDictating) {
        if (e.key === "Escape") {
          e.preventDefault();
          onToggleDictation();
          return;
        }
        // If typing in input, don't trigger playback single-character shortcuts
        if (isInputFocused) {
          // Allow Ctrl+Space or Alt+R for replay if needed, but let user type
          if ((e.ctrlKey || e.metaKey) && e.key === "r") {
            e.preventDefault();
            onReplay();
          }
          return;
        }
      }

      // If user is focused on a normal input, ignore shortcuts
      if (isInputFocused) return;

      switch (e.code) {
        case "Space":
          e.preventDefault();
          onTogglePlay();
          break;
        case "ArrowLeft":
          e.preventDefault();
          onPrev();
          break;
        case "ArrowRight":
          e.preventDefault();
          onNext();
          break;
        case "KeyR":
          e.preventDefault();
          onReplay();
          break;
        case "KeyL":
          e.preventDefault();
          onToggleLoop();
          break;
        case "KeyA":
          e.preventDefault();
          onToggleEnglish();
          break;
        case "KeyT":
          e.preventDefault();
          onToggleTranslation();
          break;
        case "KeyD":
          e.preventDefault();
          onToggleDictation();
          break;
        case "BracketLeft":
          e.preventDefault();
          onSpeedDown();
          break;
        case "BracketRight":
          e.preventDefault();
          onSpeedUp();
          break;
        case "ArrowUp":
          e.preventDefault();
          onVolumeUp();
          break;
        case "ArrowDown":
          e.preventDefault();
          onVolumeDown();
          break;
        case "Slash":
          if (e.shiftKey) {
            e.preventDefault();
            onToggleHelp();
          }
          break;
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [
    onTogglePlay,
    onReplay,
    onNext,
    onPrev,
    onToggleLoop,
    onToggleEnglish,
    onToggleTranslation,
    onToggleDictation,
    onSpeedDown,
    onSpeedUp,
    onVolumeUp,
    onVolumeDown,
    onToggleHelp,
    isDictating,
  ]);
}
