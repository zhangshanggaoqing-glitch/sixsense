"use client";

import React, { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { ChevronLeft, Play, Pause, Trash2, BookOpen } from "lucide-react";
import { api, VocabItem } from "@/lib/api";

export default function VocabularyPage() {
  const [vocabList, setVocabList] = useState<VocabItem[]>([]);
  const [playingId, setPlayingId] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const audioRef = useRef<HTMLAudioElement | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const items = await api.getVocabulary();
        setVocabList(items);
      } catch (e) {
        console.error(e);
      } finally {
        setIsLoading(false);
      }
    }
    load();
  }, []);

  const handlePlayClip = (item: VocabItem) => {
    if (playingId === item.id) {
      audioRef.current?.pause();
      setPlayingId(null);
      return;
    }

    if (audioRef.current) {
      audioRef.current.pause();
    }

    const audioUrl = api.getAudioUrl("202007-CET6 听力.mp3");
    const audio = new Audio(audioUrl);
    audioRef.current = audio;

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
    <div className="min-h-screen bg-[#fbfbfd] dark:bg-[#0d0f14] text-gray-900 dark:text-gray-100 p-6 sm:p-12">
      <div className="max-w-2xl mx-auto">
        <header className="flex items-center justify-between pb-6 border-b border-gray-200 dark:border-gray-800">
          <Link
            href="/studio"
            className="flex items-center gap-1.5 text-xs font-medium text-gray-400 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
          >
            <ChevronLeft className="w-4 h-4" /> Back to Studio
          </Link>
          <span className="text-xs uppercase font-mono font-bold text-gray-400">Contextual Vocabulary</span>
        </header>

        <main className="mt-8">
          <div className="flex items-baseline justify-between mb-6">
            <h1 className="text-2xl font-light tracking-tight text-gray-900 dark:text-gray-50">Saved Words</h1>
            <span className="text-xs text-gray-400 font-mono">{vocabList.length} items</span>
          </div>

          {isLoading ? (
            <div className="py-12 text-center text-sm text-gray-400 font-mono">Loading words...</div>
          ) : vocabList.length === 0 ? (
            <div className="py-16 text-center text-gray-400">
              <BookOpen className="w-8 h-8 mx-auto mb-3 opacity-40" />
              <p className="text-sm">No saved vocabulary yet.</p>
              <p className="text-xs text-gray-500 mt-1">
                Click any word during listening to view definition and add to your contextual vocab.
              </p>
            </div>
          ) : (
            <div className="divide-y divide-gray-100 dark:divide-gray-800/80">
              {vocabList.map((item) => (
                <div key={item.id} className="py-5 flex flex-col gap-2">
                  <div className="flex items-baseline justify-between">
                    <div className="flex items-baseline gap-3">
                      <span className="text-lg font-semibold text-gray-900 dark:text-gray-100">{item.word}</span>
                      <span className="text-xs font-mono text-gray-400">{item.phonetic}</span>
                      <span className="text-xs text-gray-400 font-medium">{item.part_of_speech}</span>
                      <span className="text-sm text-gray-700 dark:text-gray-300 ml-2">{item.definition_zh}</span>
                    </div>

                    <div className="flex items-center gap-2">
                      <button
                        onClick={() => handlePlayClip(item)}
                        className="p-1.5 text-blue-600 dark:text-blue-400 hover:bg-blue-50 dark:hover:bg-blue-950/40 rounded-lg transition-colors"
                        title="Replay original audio sentence"
                      >
                        {playingId === item.id ? <Pause className="w-4 h-4 fill-current" /> : <Play className="w-4 h-4 fill-current" />}
                      </button>
                      <button
                        onClick={() => handleDelete(item.id)}
                        className="p-1.5 text-gray-400 hover:text-red-500 transition-colors"
                        title="Remove word"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>

                  {/* Context Sentence */}
                  {item.source_sentence_en && (
                    <div className="mt-1 p-3 bg-gray-50 dark:bg-[#151821] border border-gray-100 dark:border-gray-800/60 rounded-xl text-xs text-gray-600 dark:text-gray-400">
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
