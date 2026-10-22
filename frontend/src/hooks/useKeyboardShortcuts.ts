import { useEffect } from "react";

export type StudioMode = "blind" | "bilingual" | "dictation";

export interface ShortcutHandlers {
  onTogglePlay: () => void;
  onNext: () => void;
  onPrev: () => void;
  onToggleLoop: () => void;
  onSelectMode?: (mode: StudioMode) => void;
  onSpeedDown?: () => void;
  onSpeedUp?: () => void;
  onToggleHelp?: () => void;
  isDictating?: boolean;
}

export function useKeyboardShortcuts({
  onTogglePlay,
  onNext,
  onPrev,
  onToggleLoop,
  onSelectMode,
  onSpeedDown,
  onSpeedUp,
  onToggleHelp,
  isDictating = false,
}: ShortcutHandlers) {
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      const target = e.target as HTMLElement;
      const isInputFocused =
        target.tagName === "INPUT" ||
        target.tagName === "TEXTAREA" ||
        target.isContentEditable;

      // In dictation mode, allow Esc to exit
      if (isDictating && e.key === "Escape") {
        e.preventDefault();
        onSelectMode?.("bilingual");
        return;
      }

      // If user is focused on a text input, don't trigger global shortcuts
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
          onToggleLoop();
          break;
        case "Digit1":
        case "Numpad1":
          e.preventDefault();
          onSelectMode?.("blind");
          break;
        case "Digit2":
        case "Numpad2":
          e.preventDefault();
          onSelectMode?.("bilingual");
          break;
        case "Digit3":
        case "Numpad3":
          e.preventDefault();
          onSelectMode?.("dictation");
          break;
        case "BracketLeft":
          e.preventDefault();
          onSpeedDown?.();
          break;
        case "BracketRight":
          e.preventDefault();
          onSpeedUp?.();
          break;
        case "Slash":
          if (e.shiftKey) {
            e.preventDefault();
            onToggleHelp?.();
          }
          break;
      }
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [
    onTogglePlay,
    onNext,
    onPrev,
    onToggleLoop,
    onSelectMode,
    onSpeedDown,
    onSpeedUp,
    onToggleHelp,
    isDictating,
  ]);
}
