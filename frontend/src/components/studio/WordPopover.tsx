"use client";

import React, { useState } from "react";
import { Plus, Check } from "lucide-react";
import { api, Sentence } from "@/lib/api";

interface WordPopoverProps {
  word: string;
  currentSentence: Sentence;
  examId: string;
  onClose: () => void;
  position: { top: number; left: number };
}

// Simple local mini-dictionary for common CET-6 listening terms
const CET6_MINI_DICT: Record<string, { phonetic: string; pos: string; def: string }> = {
  profound: { phonetic: "/prəˈfaʊnd/", pos: "adj.", def: "深刻的；深远的；深奥的" },
  implications: { phonetic: "/ˌɪmplɪˈkeɪʃnz/", pos: "n.", def: "可能的影响；后果；含义" },
  champion: { phonetic: "/ˈtʃæmpiən/", pos: "n.", def: "冠军；优胜者；捍卫者" },
  abilities: { phonetic: "/əˈbɪlətiz/", pos: "n.", def: "能力；本领；才能" },
  biochemistry: { phonetic: "/ˌbaɪəʊˈkemɪstri/", pos: "n.", def: "生物化学" },
  mechanics: { phonetic: "/mɪˈkænɪks/", pos: "n.", def: "机械学；力学；运作方式" },
  perceived: { phonetic: "/pəˈsiːvd/", pos: "adj.", def: "感知到的；认为的" },
  textiles: { phonetic: "/ˈtekstaɪlz/", pos: "n.", def: "纺织品；纺织业" },
  container: { phonetic: "/kənˈteɪnə/", pos: "n.", def: "集装箱；容器" },
  versatile: { phonetic: "/ˈvɜːsətaɪl/", pos: "adj.", def: "多功能的；多才多艺的" },
  paroled: { phonetic: "/pəˈrəʊld/", pos: "v.", def: "假释；保释" },
  geneticist: { phonetic: "/dʒəˈnetɪsɪst/", pos: "n.", def: "遗传学家" },
  obese: { phonetic: "/əʊˈbiːs/", pos: "adj.", def: "肥胖的；过胖的" },
  stimulation: { phonetic: "/ˌstɪmjuˈleɪʃn/", pos: "n.", def: "刺激；激励；鼓舞" },
  specimens: { phonetic: "/ˈspesɪmənz/", pos: "n.", def: "标本；样本" },
  aging: { phonetic: "/ˈeɪdʒɪŋ/", pos: "n.", def: "变老；衰老；老龄化" },
};

export function WordPopover({ word, currentSentence, examId, onClose, position }: WordPopoverProps) {
  const [isAdded, setIsAdded] = useState(false);
  const cleanWord = word.replace(/[^\w']+/g, "").toLowerCase();
  const dictInfo = CET6_MINI_DICT[cleanWord] || {
    phonetic: `/${cleanWord}/`,
    pos: "word",
    def: "六级真题核心语境词",
  };

  const handleAdd = async () => {
    try {
      await api.addVocabulary({
        word: cleanWord,
        lemma: cleanWord,
        phonetic: dictInfo.phonetic,
        part_of_speech: dictInfo.pos,
        definition_zh: dictInfo.def,
        cet_level: "CET-6",
        source_sentence_id: currentSentence.id,
        source_sentence_en: currentSentence.english,
        source_sentence_zh: currentSentence.chinese,
        exam_id: examId,
        audio_clip_start: currentSentence.start_time,
        audio_clip_end: currentSentence.end_time,
      });
      setIsAdded(true);
      setTimeout(() => onClose(), 1200);
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div
      className="fixed z-50 p-4 bg-white dark:bg-[#161922] border border-gray-200 dark:border-gray-800 rounded-xl shadow-xl w-72 backdrop-blur-md animate-in fade-in zoom-in-95 duration-150"
      style={{
        top: `${Math.min(position.top + 10, window.innerHeight - 200)}px`,
        left: `${Math.max(20, Math.min(position.left - 100, window.innerWidth - 300))}px`,
      }}
      onClick={(e) => e.stopPropagation()}
    >
      <div className="flex items-start justify-between">
        <div>
          <h4 className="text-lg font-semibold text-gray-900 dark:text-gray-100">{cleanWord}</h4>
          <p className="text-xs text-gray-500 dark:text-gray-400 font-mono mt-0.5">{dictInfo.phonetic}</p>
        </div>
        <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 rounded-full border border-blue-200 dark:border-blue-900">
          CET-6
        </span>
      </div>

      <div className="mt-2.5 text-sm text-gray-700 dark:text-gray-300">
        <span className="text-xs font-semibold text-gray-400 dark:text-gray-500 mr-1.5">{dictInfo.pos}</span>
        {dictInfo.def}
      </div>

      <div className="mt-3.5 pt-3 border-t border-gray-100 dark:border-gray-800/80 flex items-center justify-between">
        <button
          onClick={handleAdd}
          disabled={isAdded}
          className={`flex items-center gap-1.5 text-xs font-medium px-3 py-1.5 rounded-lg transition-all ${
            isAdded
              ? "bg-green-100 dark:bg-green-950/60 text-green-700 dark:text-green-300"
              : "bg-gray-900 dark:bg-white text-white dark:text-gray-900 hover:opacity-90"
          }`}
        >
          {isAdded ? (
            <>
              <Check className="w-3.5 h-3.5" /> Added to Vocab
            </>
          ) : (
            <>
              <Plus className="w-3.5 h-3.5" /> + Add to Vocab
            </>
          )}
        </button>

        <button
          onClick={onClose}
          className="text-xs text-gray-400 hover:text-gray-600 dark:hover:text-gray-200 px-2 py-1"
        >
          Close
        </button>
      </div>
    </div>
  );
}
