"use client";

import React from "react";
import { X, Keyboard } from "lucide-react";

interface KeyboardHelpModalProps {
  isOpen: boolean;
  onClose: () => void;
}

const SHORTCUTS = [
  { key: "Space", desc: "Play / Pause sentence" },
  { key: "←", desc: "Previous sentence" },
  { key: "→", desc: "Next sentence" },
  { key: "R", desc: "Replay current sentence from start" },
  { key: "L", desc: "Cycle repeat loop (1× → 3× → 5× → ∞ → off)" },
  { key: "A", desc: "Toggle English transcript on / off" },
  { key: "T", desc: "Toggle Chinese translation on / off" },
  { key: "D", desc: "Toggle Dictation mode" },
  { key: "[  /  ]", desc: "Decrease / Increase playback speed (0.7× - 1.2×)" },
  { key: "↑  /  ↓", desc: "Adjust playback volume" },
  { key: "Esc", desc: "Exit dictation or close modal" },
  { key: "?", desc: "Open this keyboard shortcut reference" },
];

export function KeyboardHelpModal({ isOpen, onClose }: KeyboardHelpModalProps) {
  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 backdrop-blur-xs p-4 animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div
        className="w-full max-w-md bg-white dark:bg-[#161922] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-2xl p-6 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex items-center justify-between pb-4 border-b border-gray-100 dark:border-gray-800">
          <div className="flex items-center gap-2">
            <Keyboard className="w-4 h-4 text-blue-500" />
            <h3 className="text-base font-semibold text-gray-900 dark:text-gray-100">Keyboard Shortcuts</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 rounded-lg"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        <div className="mt-4 divide-y divide-gray-100 dark:divide-gray-800/60 max-h-[60vh] overflow-y-auto">
          {SHORTCUTS.map((s, idx) => (
            <div key={idx} className="py-2.5 flex items-center justify-between text-sm">
              <span className="text-gray-600 dark:text-gray-300">{s.desc}</span>
              <kbd className="px-2.5 py-1 bg-gray-100 dark:bg-gray-800/90 text-gray-800 dark:text-gray-200 text-xs font-mono font-medium rounded-md border border-gray-200 dark:border-gray-700/80 shadow-2xs">
                {s.key}
              </kbd>
            </div>
          ))}
        </div>

        <div className="mt-5 pt-3 border-t border-gray-100 dark:border-gray-800 text-center">
          <p className="text-xs text-gray-400">Designed for zero-mouse, keyboard-first intensive listening.</p>
        </div>
      </div>
    </div>
  );
}
