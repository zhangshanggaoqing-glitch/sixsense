"use client";

import React, { useState, useEffect, useRef } from "react";
import { Search, X, Volume2, Plus, Check, Loader2, Sparkles } from "lucide-react";
import { api, WordLookupResult } from "@/lib/api";

interface QuickLookupModalProps {
  isOpen: boolean;
  onClose: () => void;
  currentExamId?: string;
}

export function QuickLookupModal({ isOpen, onClose, currentExamId = "" }: QuickLookupModalProps) {
  const [query, setQuery] = useState("");
  const [data, setData] = useState<WordLookupResult | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [isAdded, setIsAdded] = useState(false);
  const [playingVoice, setPlayingVoice] = useState<"uk" | "us" | null>(null);
  const inputRef = useRef<HTMLInputElement | null>(null);
  const voiceAudioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (isOpen) {
      setTimeout(() => inputRef.current?.focus(), 50);
    } else {
      setQuery("");
      setData(null);
      setIsAdded(false);
    }
  }, [isOpen]);

  const handleSearch = async (targetWord?: string) => {
    const wordToSearch = (targetWord || query).trim().toLowerCase();
    if (!wordToSearch) return;

    setIsLoading(true);
    setIsAdded(false);
    try {
      const res = await api.lookupWord(wordToSearch);
      setData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter") {
      e.preventDefault();
      handleSearch();
    } else if (e.key === "Escape") {
      onClose();
    }
  };

  const playVoice = (type: "uk" | "us") => {
    if (!data) return;
    if (voiceAudioRef.current) {
      voiceAudioRef.current.pause();
    }
    setPlayingVoice(type);

    const primaryUrl = type === "uk" ? data.audio_uk : data.audio_us;
    const directUrl = type === "uk" ? data.audio_uk_direct : data.audio_us_direct;
    const audio = new Audio(primaryUrl);
    voiceAudioRef.current = audio;

    const fallbackSpeech = () => {
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(data.word);
        utterance.lang = type === "uk" ? "en-GB" : "en-US";
        utterance.rate = 0.9;
        utterance.onend = () => setPlayingVoice(null);
        utterance.onerror = () => setPlayingVoice(null);
        window.speechSynthesis.speak(utterance);
      } else {
        setPlayingVoice(null);
      }
    };

    audio.onended = () => setPlayingVoice(null);
    audio.onerror = () => {
      if (directUrl) {
        const directAudio = new Audio(directUrl);
        voiceAudioRef.current = directAudio;
        directAudio.onended = () => setPlayingVoice(null);
        directAudio.onerror = () => fallbackSpeech();
        directAudio.play().catch(() => fallbackSpeech());
      } else {
        fallbackSpeech();
      }
    };
    audio.play().catch(() => fallbackSpeech());
  };

  const handleAdd = async () => {
    if (!data) return;
    try {
      const primaryDef = data.definitions.length > 0
        ? `${data.definitions[0].pos ? data.definitions[0].pos + ' ' : ''}${data.definitions[0].meaning}`
        : "六级核心语境词";
      const primaryPos = data.definitions[0]?.pos || "";

      await api.addVocabulary({
        word: data.word,
        lemma: data.lemma || data.word,
        phonetic: data.phonetic_us ? `/${data.phonetic_us}/` : (data.phonetic_uk ? `/${data.phonetic_uk}/` : `/${data.word}/`),
        phonetic_uk: data.phonetic_uk,
        phonetic_us: data.phonetic_us,
        audio_uk: data.audio_uk,
        audio_us: data.audio_us,
        part_of_speech: primaryPos,
        definition_zh: primaryDef,
        cet_level: "CET-6",
        exam_id: currentExamId,
      });
      setIsAdded(true);
    } catch (e) {
      console.error(e);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 backdrop-blur-sm animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div
        className="w-full max-w-lg bg-white dark:bg-[#151822] border border-gray-200 dark:border-gray-800 rounded-2xl shadow-2xl overflow-hidden animate-in zoom-in-95 duration-150"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Search Input Bar */}
        <div className="flex items-center gap-3 px-4 py-3.5 border-b border-gray-100 dark:border-gray-800/80">
          <Search className="w-5 h-5 text-gray-400 shrink-0" />
          <input
            ref={inputRef}
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="输入任何单词，查询权威英美音与翻译（按回车搜索）..."
            className="w-full bg-transparent text-sm sm:text-base text-gray-900 dark:text-gray-100 placeholder:text-gray-400 focus:outline-none"
          />
          {query && (
            <button
              onClick={() => { setQuery(""); setData(null); inputRef.current?.focus(); }}
              className="p-1 text-gray-400 hover:text-gray-600 dark:hover:text-gray-200"
            >
              <X className="w-4 h-4" />
            </button>
          )}
        </div>

        {/* Search Content */}
        <div className="p-5 max-h-[70vh] overflow-y-auto">
          {isLoading ? (
            <div className="py-12 flex flex-col items-center justify-center gap-2 text-gray-400">
              <Loader2 className="w-6 h-6 animate-spin text-blue-500" />
              <span className="text-xs font-mono">正在检索权威词库与英美原生读音...</span>
            </div>
          ) : data ? (
            <div className="space-y-4">
              <div className="flex items-start justify-between border-b border-gray-100 dark:border-gray-800/80 pb-3">
                <div>
                  <div className="flex items-baseline gap-2">
                    <h3 className="text-2xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
                      {data.word}
                    </h3>
                    {data.lemma && data.lemma !== data.word && (
                      <span className="text-xs text-gray-400 font-mono">(原形: {data.lemma})</span>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <button
                    onClick={handleAdd}
                    disabled={isAdded}
                    className={`flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-xl transition-all ${
                      isAdded
                        ? "bg-green-100 dark:bg-green-950/60 text-green-700 dark:text-green-300"
                        : "bg-gray-900 dark:bg-white text-white dark:text-gray-900 hover:opacity-90"
                    }`}
                  >
                    {isAdded ? (
                      <>
                        <Check className="w-3.5 h-3.5" /> 已在生词本
                      </>
                    ) : (
                      <>
                        <Plus className="w-3.5 h-3.5" /> 收入生词本
                      </>
                    )}
                  </button>
                </div>
              </div>

              {/* Pronunciation: UK & US */}
              <div className="grid grid-cols-2 gap-3">
                <button
                  onClick={() => playVoice("uk")}
                  className={`flex items-center justify-between p-3 rounded-xl border transition-all text-left ${
                    playingVoice === "uk"
                      ? "bg-indigo-50 border-indigo-300 dark:bg-indigo-950/50 dark:border-indigo-700 ring-2 ring-indigo-500/30"
                      : "bg-gray-50/80 dark:bg-[#191c28] border-gray-100 dark:border-gray-800 hover:border-indigo-200"
                  }`}
                  title="点击发音：英音 (UK)"
                >
                  <div>
                    <span className="text-xs font-semibold text-indigo-600 dark:text-indigo-400">
                      🇬🇧 英音
                    </span>
                    <p className="text-xs font-mono text-gray-600 dark:text-gray-300 mt-0.5">
                      {data.phonetic_uk ? `/${data.phonetic_uk}/` : `/${data.word}/`}
                    </p>
                  </div>
                  <div className={`p-2 rounded-lg ${playingVoice === "uk" ? "bg-indigo-600 text-white animate-pulse" : "text-gray-400 hover:text-indigo-600"}`}>
                    <Volume2 className="w-4 h-4" />
                  </div>
                </button>

                <button
                  onClick={() => playVoice("us")}
                  className={`flex items-center justify-between p-3 rounded-xl border transition-all text-left ${
                    playingVoice === "us"
                      ? "bg-blue-50 border-blue-300 dark:bg-blue-950/50 dark:border-blue-700 ring-2 ring-blue-500/30"
                      : "bg-gray-50/80 dark:bg-[#191c28] border-gray-100 dark:border-gray-800 hover:border-blue-200"
                  }`}
                  title="点击发音：美音 (US)"
                >
                  <div>
                    <span className="text-xs font-semibold text-blue-600 dark:text-blue-400">
                      🇺🇸 美音
                    </span>
                    <p className="text-xs font-mono text-gray-600 dark:text-gray-300 mt-0.5">
                      {data.phonetic_us ? `/${data.phonetic_us}/` : `/${data.word}/`}
                    </p>
                  </div>
                  <div className={`p-2 rounded-lg ${playingVoice === "us" ? "bg-blue-600 text-white animate-pulse" : "text-gray-400 hover:text-blue-600"}`}>
                    <Volume2 className="w-4 h-4" />
                  </div>
                </button>
              </div>

              {/* Definitions */}
              <div className="space-y-2 pt-1">
                <span className="text-xs font-semibold uppercase tracking-wider text-gray-400">权威中文释义</span>
                <div className="space-y-1.5">
                  {data.definitions.map((def, idx) => (
                    <div key={idx} className="flex items-start gap-2 text-sm leading-relaxed text-gray-800 dark:text-gray-200">
                      {def.pos && (
                        <span className="shrink-0 font-semibold px-1.5 py-0.5 rounded bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 font-mono text-xs">
                          {def.pos}
                        </span>
                      )}
                      <span>{def.meaning}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Context Examples */}
              {data.examples && data.examples.length > 0 && (
                <div className="p-3 rounded-xl bg-gray-50 dark:bg-[#191c28] border border-gray-100 dark:border-gray-800/80 text-xs space-y-1.5">
                  <div className="flex items-center gap-1 text-[11px] font-semibold text-gray-400 uppercase tracking-wider">
                    <Sparkles className="w-3.5 h-3.5 text-amber-500" /> 原汁例句搭配
                  </div>
                  <p className="font-medium text-gray-800 dark:text-gray-200">
                    {data.examples[0].en}
                  </p>
                  <p className="text-gray-500 dark:text-gray-400">
                    {data.examples[0].zh}
                  </p>
                </div>
              )}
            </div>
          ) : (
            <div className="py-10 text-center text-gray-400">
              <Search className="w-8 h-8 mx-auto mb-2 opacity-30" />
              <p className="text-sm font-medium">随时检索真题词汇</p>
              <p className="text-xs text-gray-500 mt-1">
                输入单词并按回车，查看权威英音与美音双重发音、中文字典释义及原声例句。
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
