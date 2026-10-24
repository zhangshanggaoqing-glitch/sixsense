"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { ChevronLeft, Play, Pause, Trash2, BookOpen, Volume2, CheckCircle2 } from "lucide-react";
import { api, VocabItem, ExamItem } from "@/lib/api";
import { useAuth } from "@/hooks/useAuth";

export default function VocabularyPage() {
  const { user, isLoggedIn, logout } = useAuth();
  const [vocabList, setVocabList] = useState<VocabItem[]>([]);
  const [examAudioMap, setExamAudioMap] = useState<Record<string, string>>({});
  const [playingId, setPlayingId] = useState<string | null>(null);
  const [playingVoice, setPlayingVoice] = useState<{ id: string; type: "uk" | "us" } | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const clipAudioRef = useRef<HTMLAudioElement | null>(null);
  const voiceAudioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    async function load() {
      setIsLoading(true);
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
  }, [user]);

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
    <div className="min-h-screen bg-[#f5f5f7] dark:bg-[#000000] text-[#1d1d1f] dark:text-[#f5f5f7] p-4 sm:p-12 pt-[max(0.85rem,env(safe-area-inset-top))] pb-[max(2rem,env(safe-area-inset-bottom))] select-none">
      <div className="max-w-3xl mx-auto">
        <header className="flex items-center justify-between pb-4 sm:pb-6 border-b border-black/[0.06] dark:border-white/[0.08]">
          <Link
            href="/studio"
            className="flex items-center gap-1.5 text-xs font-medium text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] p-1 -ml-1 rounded-full transition-colors active:scale-95"
          >
            <ChevronLeft className="w-4 h-4" /> 返回精听工作台
          </Link>
          <span className="text-xs text-[#86868b]">语境生词本</span>
        </header>

        <main className="mt-6 sm:mt-8">
          {/* Account Sync Status Banner */}
          {!isLoggedIn ? (
            <div className="mb-6 p-4 rounded-2xl bg-[#0071e3]/10 dark:bg-[#0a84ff]/15 border border-[#0071e3]/20 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs animate-in fade-in duration-200">
              <span className="text-[#0071e3] dark:text-[#0a84ff]">
                当前为本地访客模式。登录后生词本将安全同步至云端账号，支持多设备无缝学习。
              </span>
              <Link
                href="/login?redirect=/vocabulary"
                className="px-4 py-2 rounded-full bg-[#0071e3] text-white font-medium hover:bg-[#0077ed] transition-colors shrink-0 shadow-sm text-center active:scale-95"
              >
                登录 / 注册
              </Link>
            </div>
          ) : (
            <div className="mb-6 px-1 flex items-center justify-between text-xs text-[#86868b] animate-in fade-in duration-200">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-3.5 h-3.5 text-[#34c759]" />
                已安全同步至账号：<strong className="text-[#1d1d1f] dark:text-[#f5f5f7]">{user?.username}</strong>
              </span>
              <button
                onClick={logout}
                className="text-[#86868b] hover:text-[#ff3b30] p-1 transition-colors"
              >
                退出登录
              </button>
            </div>
          )}

          <div className="flex items-baseline justify-between mb-5 sm:mb-6">
            <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
              生词笔记本
            </h1>
            <span className="text-xs text-[#86868b] font-mono">共收录 {vocabList.length} 词</span>
          </div>

          {isLoading ? (
            <div className="py-12 text-center text-sm text-[#86868b] font-mono">正在加载词汇库...</div>
          ) : vocabList.length === 0 ? (
            <div className="py-16 text-center text-[#86868b]">
              <BookOpen className="w-8 h-8 mx-auto mb-3 opacity-40" />
              <p className="text-sm">生词本目前为空。</p>
              <p className="text-xs text-[#86868b]/70 mt-1 max-w-sm mx-auto">
                在听力播放与听写练习中点击任何单词，即可查看权威英美发音、释义并一键加入生词本。
              </p>
            </div>
          ) : (
            <div className="divide-y divide-black/[0.05] dark:divide-white/[0.06]">
              {vocabList.map((item) => (
                <div key={item.id} className="py-4 sm:py-5 flex flex-col gap-2.5">
                  <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 sm:gap-4">
                    <div className="flex flex-col gap-1.5 flex-1">
                      <div className="flex items-center gap-2.5 flex-wrap">
                        <span className="text-lg sm:text-xl font-bold tracking-tight text-[#1d1d1f] dark:text-[#f5f5f7]">
                          {item.word}
                        </span>

                        {/* UK Voice Button */}
                        <button
                          type="button"
                          onClick={() => handlePlayVoice(item, "uk")}
                          className={`flex items-center gap-1 px-2.5 py-1 rounded-xl border text-xs font-medium transition-all active:scale-95 ${
                            playingVoice?.id === item.id && playingVoice.type === "uk"
                              ? "bg-[#0071e3]/10 border-[#0071e3]/30 text-[#0071e3] dark:text-[#0a84ff]"
                              : "bg-black/[0.02] dark:bg-white/[0.04] border-black/[0.06] dark:border-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7]"
                          }`}
                          title="播放英音发音"
                        >
                          <span className="text-[10px] font-semibold text-[#0071e3] dark:text-[#0a84ff]">英</span>
                          <span className="font-mono text-[11px] text-[#86868b]">
                            {item.phonetic_uk ? `/${item.phonetic_uk}/` : (item.phonetic || `/${item.word}/`)}
                          </span>
                          <Volume2 className={`w-3.5 h-3.5 ${playingVoice?.id === item.id && playingVoice.type === "uk" ? "text-[#0071e3] animate-pulse" : "text-[#86868b]"}`} />
                        </button>

                        {/* US Voice Button */}
                        <button
                          type="button"
                          onClick={() => handlePlayVoice(item, "us")}
                          className={`flex items-center gap-1 px-2.5 py-1 rounded-xl border text-xs font-medium transition-all active:scale-95 ${
                            playingVoice?.id === item.id && playingVoice.type === "us"
                              ? "bg-[#0071e3]/10 border-[#0071e3]/30 text-[#0071e3] dark:text-[#0a84ff]"
                              : "bg-black/[0.02] dark:bg-white/[0.04] border-black/[0.06] dark:border-white/[0.08] text-[#1d1d1f] dark:text-[#f5f5f7]"
                          }`}
                          title="播放美音发音"
                        >
                          <span className="text-[10px] font-semibold text-[#0071e3] dark:text-[#0a84ff]">美</span>
                          <span className="font-mono text-[11px] text-[#86868b]">
                            {item.phonetic_us ? `/${item.phonetic_us}/` : (item.phonetic || `/${item.word}/`)}
                          </span>
                          <Volume2 className={`w-3.5 h-3.5 ${playingVoice?.id === item.id && playingVoice.type === "us" ? "text-[#0071e3] animate-pulse" : "text-[#86868b]"}`} />
                        </button>
                      </div>

                      {/* Definition */}
                      <div className="text-sm text-[#1d1d1f] dark:text-[#f5f5f7] flex items-baseline gap-2 mt-0.5">
                        {item.part_of_speech && (
                          <span className="text-xs font-semibold px-1.5 py-0.5 rounded bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff] font-mono">
                            {item.part_of_speech}
                          </span>
                        )}
                        <span>{item.definition_zh}</span>
                      </div>
                    </div>

                    <div className="flex items-center gap-2 shrink-0 self-end sm:self-start">
                      <button
                        type="button"
                        onClick={() => handlePlayClip(item)}
                        className="px-3 py-1.5 text-xs font-medium text-[#0071e3] dark:text-[#0a84ff] bg-[#0071e3]/10 dark:bg-[#0a84ff]/15 rounded-full border border-[#0071e3]/20 flex items-center gap-1.5 transition-all active:scale-95"
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
                        type="button"
                        onClick={() => handleDelete(item.id)}
                        className="p-1.5 text-[#86868b] hover:text-[#ff3b30] transition-colors rounded-full active:scale-90"
                        title="移出生词本"
                      >
                        <Trash2 className="w-4 h-4" />
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
