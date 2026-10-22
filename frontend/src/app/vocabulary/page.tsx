"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { ChevronLeft, Play, Pause, Trash2, BookOpen, Volume2 } from "lucide-react";
import { api, VocabItem, ExamItem } from "@/lib/api";

export default function VocabularyPage() {
  const [vocabList, setVocabList] = useState<VocabItem[]>([]);
  const [examAudioMap, setExamAudioMap] = useState<Record<string, string>>({});
  const [playingId, setPlayingId] = useState<string | null>(null);
  const [playingVoice, setPlayingVoice] = useState<{ id: string; type: "uk" | "us" } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const clipAudioRef = useRef<HTMLAudioElement | null>(null);
  const voiceAudioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const [items, exams] = await Promise.all([
          api.getVocabulary(),
          api.getExams().catch(() => [] as ExamItem[]),
        ]);
        setVocabList(items);

        const map: Record<string, string> = {};
        for (const e of exams) {
          map[e.id] = e.audio_file;
        }
        setExamAudioMap(map);
      } catch (e) {
        console.error(e);
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, []);

  const handlePlayVoice = (item: VocabItem, type: "uk" | "us") => {
    if (voiceAudioRef.current) {
      voiceAudioRef.current.pause();
      voiceAudioRef.current = null;
    }

    setPlayingVoice({ id: item.id, type });

    const primaryUrl = api.getVoiceUrl(item.word, type === "uk" ? 1 : 2);
    const audio = new Audio(primaryUrl);
    voiceAudioRef.current = audio;

    const fallbackSpeech = () => {
      if (typeof window !== "undefined" && "speechSynthesis" in window) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(item.word);
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
      const directUrl = `https://dict.youdao.com/dictvoice?audio=${encodeURIComponent(item.word)}&type=${type === "uk" ? 1 : 2}`;
      const directAudio = new Audio(directUrl);
      voiceAudioRef.current = directAudio;
      directAudio.onended = () => setPlayingVoice(null);
      directAudio.onerror = () => fallbackSpeech();
      directAudio.play().catch(() => fallbackSpeech());
    };

    audio.play().catch(() => fallbackSpeech());
  };

  const handlePlayClip = (item: VocabItem) => {
    if (playingId === item.id) {
      clipAudioRef.current?.pause();
      setPlayingId(null);
      return;
    }

    if (clipAudioRef.current) {
      clipAudioRef.current.pause();
    }

    const audioFile = examAudioMap[item.exam_id] || "2016年06月六级听力第1套.mp3";
    const audioUrl = api.getAudioUrl(audioFile);
    const audio = new Audio(audioUrl);
    clipAudioRef.current = audio;

    audio.currentTime = item.audio_clip_start;
    audio.play().then(() => {
      setPlayingId(item.id);
    }).catch(() => {});

    audio.ontimeupdate = () => {
      if (audio.currentTime >= item.audio_clip_end) {
        audio.pause();
        setPlayingId(null);
      }
    };

    audio.onended = () => setPlayingId(null);
  };

  const handleDelete = async (id: string) => {
    try {
      await api.deleteVocabulary(id);
      setVocabList((prev) => prev.filter((v) => v.id !== id));
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] p-6 sm:p-12 select-none">
      <div className="max-w-3xl mx-auto">
        <header className="flex items-center justify-between pb-6 border-b border-black/[0.06] dark:border-white/[0.08]">
          <Link
            href="/studio"
            className="flex items-center gap-1.5 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] transition-colors"
          >
            <ChevronLeft className="w-4 h-4" /> 返回精听工作台
          </Link>
          <span className="text-xs text-[#86868b]">大学英语六级语境生词本</span>
        </header>

        <main className="mt-8">
          <div className="flex items-baseline justify-between mb-6">
            <h1 className="text-2xl font-light tracking-tight text-gray-900 dark:text-gray-50">
              生词笔记本
            </h1>
            <span className="text-xs text-gray-400 font-mono">共收录 {vocabList.length} 词</span>
          </div>

          {isLoading ? (
            <div className="py-12 text-center text-sm text-gray-400 font-mono">正在加载词汇库...</div>
          ) : vocabList.length === 0 ? (
            <div className="py-16 text-center text-gray-400">
              <BookOpen className="w-8 h-8 mx-auto mb-3 opacity-40" />
              <p className="text-sm">生词本目前为空。</p>
              <p className="text-xs text-gray-500 mt-1">
                在听力播放与听写练习中点击任何单词，即可查看权威英美发音、释义并一键加入生词本。
              </p>
            </div>
          ) : (
            <div className="divide-y divide-gray-100 dark:divide-gray-800/80">
              {vocabList.map((item) => (
                <div key={item.id} className="py-5 flex flex-col gap-2.5">
                  <div className="flex items-start justify-between gap-4">
                    <div className="flex flex-col gap-1.5">
                      <div className="flex items-center gap-3 flex-wrap">
                        <span className="text-xl font-bold tracking-tight text-gray-900 dark:text-gray-100">
                          {item.word}
                        </span>

                        {/* UK Voice Button */}
                        <button
                          onClick={() => handlePlayVoice(item, "uk")}
                          className={`flex items-center gap-1 px-2 py-0.5 rounded-lg border text-xs font-medium transition-all ${
                            playingVoice?.id === item.id && playingVoice.type === "uk"
                              ? "bg-indigo-50 border-indigo-300 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300"
                              : "bg-gray-50 dark:bg-[#191c28] border-gray-200/80 dark:border-gray-800 text-gray-600 dark:text-gray-300 hover:border-indigo-300"
                          }`}
                          title="播放英音发音"
                        >
                          <span className="text-[10px] font-semibold text-indigo-600 dark:text-indigo-400">英</span>
                          <span className="font-mono text-[11px] text-gray-500 dark:text-gray-400">
                            {item.phonetic_uk ? `/${item.phonetic_uk}/` : (item.phonetic || `/${item.word}/`)}
                          </span>
                          <Volume2 className={`w-3.5 h-3.5 ${playingVoice?.id === item.id && playingVoice.type === "uk" ? "text-indigo-600 animate-pulse" : "text-gray-400"}`} />
                        </button>

                        {/* US Voice Button */}
                        <button
                          onClick={() => handlePlayVoice(item, "us")}
                          className={`flex items-center gap-1 px-2 py-0.5 rounded-lg border text-xs font-medium transition-all ${
                            playingVoice?.id === item.id && playingVoice.type === "us"
                              ? "bg-blue-50 border-blue-300 text-blue-700 dark:bg-blue-950/60 dark:text-blue-300"
                              : "bg-gray-50 dark:bg-[#191c28] border-gray-200/80 dark:border-gray-800 text-gray-600 dark:text-gray-300 hover:border-blue-300"
                          }`}
                          title="播放美音发音"
                        >
                          <span className="text-[10px] font-semibold text-blue-600 dark:text-blue-400">美</span>
                          <span className="font-mono text-[11px] text-gray-500 dark:text-gray-400">
                            {item.phonetic_us ? `/${item.phonetic_us}/` : (item.phonetic || `/${item.word}/`)}
                          </span>
                          <Volume2 className={`w-3.5 h-3.5 ${playingVoice?.id === item.id && playingVoice.type === "us" ? "text-blue-600 animate-pulse" : "text-gray-400"}`} />
                        </button>
                      </div>

                      {/* Definition */}
                      <div className="text-sm text-gray-700 dark:text-gray-300 flex items-baseline gap-2">
                        {item.part_of_speech && (
                          <span className="text-xs font-semibold px-1.5 py-0.5 rounded bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 font-mono">
                            {item.part_of_speech}
                          </span>
                        )}
                        <span>{item.definition_zh}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 shrink-0">
                      <button
                        onClick={() => handlePlayClip(item)}
                        className="px-2.5 py-1.5 text-xs font-medium text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-950/40 rounded-xl border border-blue-200 dark:border-blue-900/60 flex items-center gap-1.5 transition-colors"
                        title="复读真题原声上下文"
                      >
                        {playingId === item.id ? (
                          <>
                            <Pause className="w-3.5 h-3.5 fill-current" /> 暂停原句
                          </>
                        ) : (
                          <>
                            <Play className="w-3.5 h-3.5 fill-current" /> 原句回放
                          </>
                        )}
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="p-1.5 text-gray-400 hover:text-red-500 transition-colors rounded-lg"
                        title="移出生词本"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  {/* Context Sentence */}
                  {item.source_sentence_en && (
                    <div className="p-3 bg-gray-50 dark:bg-[#151821] border border-gray-100 dark:border-gray-800/60 rounded-xl text-xs text-gray-600 dark:text-gray-400 leading-relaxed">
                      <p className="font-medium text-gray-800 dark:text-gray-200">{item.source_sentence_en}</p>
                      <p className="mt-1 text-gray-400 dark:text-gray-500">{item.source_sentence_zh}</p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </main>
      </div>
    </div>
  );
}
