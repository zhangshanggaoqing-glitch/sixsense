"use client";

import React, { useState, useEffect, useMemo, useRef, memo } from "react";
import { X, Search, Check, ChevronRight, Calendar, Layers } from "lucide-react";
import { api, ExamItem, Subpart } from "@/lib/api";
import { formatExamTitleZh, formatSubpartTitleZh } from "@/lib/formatters";

interface ExamSelectorSheetProps {
  isOpen: boolean;
  onClose: () => void;
  currentExamId: string;
  currentSubpartId: string;
  onSelect: (examId: string, subpartId: string) => void;
  initialExams?: ExamItem[];
  initialSubparts?: Subpart[];
}

// Module-level in-memory cache to guarantee 0ms latency on open
let globalExamsCache: ExamItem[] | null = null;
const globalSubpartsCache = new Map<string, Subpart[]>();

export const ExamSelectorSheet = memo(function ExamSelectorSheet({
  isOpen,
  onClose,
  currentExamId,
  currentSubpartId,
  onSelect,
  initialExams,
  initialSubparts,
}: ExamSelectorSheetProps) {
  const [exams, setExams] = useState<ExamItem[]>(() => globalExamsCache || initialExams || []);
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedYear, setSelectedYear] = useState<number>(2026);
  const [expandedExamId, setExpandedExamId] = useState<string>(currentExamId);
  const [expandedSubparts, setExpandedSubparts] = useState<Subpart[]>([]);
  const [isLoadingSubparts, setIsLoadingSubparts] = useState(false);

  const searchInputRef = useRef<HTMLInputElement | null>(null);

  // Seed cache with initial props
  useEffect(() => {
    if (initialExams && initialExams.length > 0 && !globalExamsCache) {
      globalExamsCache = initialExams;
      setExams(initialExams);
    }
  }, [initialExams]);

  useEffect(() => {
    if (currentExamId && initialSubparts && initialSubparts.length > 0) {
      globalSubpartsCache.set(currentExamId, initialSubparts);
      if (expandedExamId === currentExamId) {
        setExpandedSubparts(initialSubparts);
      }
    }
  }, [currentExamId, initialSubparts, expandedExamId]);

  // Load all exams if not in cache
  useEffect(() => {
    if (!isOpen) return;

    if (!globalExamsCache || globalExamsCache.length === 0) {
      api.getExams()
        .then((data) => {
          globalExamsCache = data;
          setExams(data);
        })
        .catch((err) => console.error("Failed to load exams list", err));
    }
  }, [isOpen]);

  // Sync selectedYear & expandedExamId with currentExamId when opened
  useEffect(() => {
    if (isOpen) {
      setSearchQuery("");
      setExpandedExamId(currentExamId);
      const curr = exams.find((e) => e.id === currentExamId);
      if (curr) {
        setSelectedYear(curr.year);
      } else if (exams.length > 0) {
        setSelectedYear(exams[0].year);
      }
    }
  }, [isOpen, currentExamId, exams]);

  // Load subparts when expanded exam changes
  useEffect(() => {
    if (!isOpen || !expandedExamId) return;

    const cached = globalSubpartsCache.get(expandedExamId);
    if (cached) {
      setExpandedSubparts(cached);
      return;
    }

    setIsLoadingSubparts(true);
    api.getSubparts(expandedExamId)
      .then((data) => {
        globalSubpartsCache.set(expandedExamId, data);
        setExpandedSubparts(data);
      })
      .catch((err) => console.error("Failed to load subparts for exam", expandedExamId, err))
      .finally(() => setIsLoadingSubparts(false));
  }, [isOpen, expandedExamId]);

  // Keyboard navigation: Escape to close
  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  // Lock body scroll while open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    } else {
      document.body.style.overflow = "";
    }
    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  // Computed: available years
  const availableYears = useMemo(() => {
    return Array.from(new Set(exams.map((e) => e.year))).sort((a, b) => b - a);
  }, [exams]);

  // Computed: exams in current selected year
  const examsInYear = useMemo(() => {
    return exams.filter((e) => e.year === selectedYear);
  }, [exams, selectedYear]);

  // Categorize subparts into 3 standard sections: A (长对话), B (篇章), C (讲座/报道)
  const groupedSections = useMemo(() => {
    const secA = expandedSubparts.filter((sp) => {
      const sid = (sp.section_id || "").toLowerCase();
      const stype = (sp.type || "").toLowerCase();
      return sid.endsWith("sec-a") || sid.endsWith("section-a") || stype === "conversation" || sp.order_num <= 2;
    });

    const secB = expandedSubparts.filter((sp) => {
      const sid = (sp.section_id || "").toLowerCase();
      const stype = (sp.type || "").toLowerCase();
      return (
        !secA.includes(sp) &&
        (sid.endsWith("sec-b") || sid.endsWith("section-b") || stype === "passage" || sp.order_num <= 4)
      );
    });

    const secC = expandedSubparts.filter((sp) => !secA.includes(sp) && !secB.includes(sp));

    return [
      { id: "sec-a", name: "Section A · 长对话", subparts: secA },
      { id: "sec-b", name: "Section B · 听力篇章", subparts: secB },
      { id: "sec-c", name: "Section C · 讲座与报道", subparts: secC },
    ].filter((g) => g.subparts.length > 0);
  }, [expandedSubparts]);

  // Search filter across all exams
  const searchResults = useMemo(() => {
    const q = searchQuery.trim().toLowerCase();
    if (!q) return null;

    const matchedExams = exams.filter((e) => {
      const title = formatExamTitleZh(e.title || e.id).toLowerCase();
      const raw = (e.title || "").toLowerCase();
      const y = String(e.year);
      return title.includes(q) || raw.includes(q) || y.includes(q);
    });

    return matchedExams;
  }, [searchQuery, exams]);

  if (!isOpen) return null;

  const handleSelectSubpart = (examId: string, subpartId: string) => {
    onSelect(examId, subpartId);
    onClose();
  };

  const handleSelectExamInYear = (examId: string) => {
    setExpandedExamId(examId);
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-end sm:items-center justify-center bg-black/40 backdrop-blur-sm p-0 sm:p-4 animate-in fade-in duration-150"
      onClick={onClose}
    >
      <div
        className="w-full sm:max-w-xl h-[82vh] sm:h-auto sm:max-h-[82vh] bg-white dark:bg-[#1c1c1e] border-t sm:border border-black/[0.08] dark:border-white/[0.1] rounded-t-[28px] sm:rounded-2xl shadow-2xl flex flex-col overflow-hidden animate-in slide-in-from-bottom sm:zoom-in-95 duration-200 pb-[env(safe-area-inset-bottom)]"
        onClick={(e) => e.stopPropagation()}
      >
        {/* iOS Mobile Drag Handle */}
        <div className="w-10 h-1 bg-black/15 dark:bg-white/20 rounded-full mx-auto mt-2.5 sm:hidden shrink-0" />

        {/* Header */}
        <div className="flex items-center justify-between px-4 sm:px-6 py-3 border-b border-black/[0.05] dark:border-white/[0.08] shrink-0">
          <div>
            <h2 className="text-sm font-semibold text-[#1d1d1f] dark:text-[#f5f5f7]">选择题目</h2>
            <p className="text-[11px] text-[#86868b] dark:text-[#a1a1a6] mt-0.5">
              点击年份与套卷快速切换
            </p>
          </div>
          <button
            onClick={onClose}
            className="w-8 h-8 flex items-center justify-center rounded-full text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7] hover:bg-black/5 dark:hover:bg-white/10 active:scale-95 transition-all"
            aria-label="关闭"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Search Bar */}
        <div className="px-4 sm:px-6 pt-3 pb-2 shrink-0">
          <div className="relative flex items-center">
            <Search className="w-3.5 h-3.5 text-[#86868b] absolute left-3 pointer-events-none" />
            <input
              ref={searchInputRef}
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="搜索年份或套卷，如 2026、第1套"
              className="w-full pl-8 pr-8 py-1.5 text-xs bg-black/[0.04] dark:bg-white/[0.06] hover:bg-black/[0.06] dark:hover:bg-white/[0.08] focus:bg-white dark:focus:bg-[#2c2c2e] text-[#1d1d1f] dark:text-[#f5f5f7] placeholder:text-[#86868b] rounded-full border border-transparent focus:border-[#0071e3] outline-none transition-all"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-2.5 text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-2 space-y-4">
          {searchResults ? (
            /* Search Results Mode */
            <div className="space-y-2">
              <span className="text-[11px] text-[#86868b] font-medium">
                找到 {searchResults.length} 套相关考卷
              </span>
              {searchResults.length === 0 ? (
                <div className="py-12 text-center text-xs text-[#86868b]">
                  未找到匹配题目，可尝试搜索年份如 2026 或 2024
                </div>
              ) : (
                <div className="space-y-1">
                  {searchResults.map((ex) => {
                    const isCurrent = ex.id === currentExamId;
                    return (
                      <button
                        key={ex.id}
                        onClick={() => {
                          setSelectedYear(ex.year);
                          setExpandedExamId(ex.id);
                          setSearchQuery("");
                        }}
                        className={`w-full flex items-center justify-between px-3.5 py-2.5 rounded-xl text-left transition-all active:scale-[0.99] ${
                          isCurrent
                            ? "bg-[#0071e3]/10 text-[#0071e3] font-semibold"
                            : "hover:bg-black/[0.03] dark:hover:bg-white/[0.05] text-[#1d1d1f] dark:text-[#f5f5f7]"
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          <Calendar className="w-3.5 h-3.5 text-[#86868b]" />
                          <span className="text-xs">{formatExamTitleZh(ex.title || ex.id)}</span>
                        </div>
                        <div className="flex items-center gap-1.5 text-xs text-[#86868b]">
                          {isCurrent && <span className="text-[11px] text-[#0071e3]">当前进行</span>}
                          <ChevronRight className="w-3.5 h-3.5" />
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          ) : (
            /* Normal Grouped View */
            <>
              {/* Year Pills (Swipeable horizontal bar) */}
              <div>
                <div className="flex items-center gap-1.5 overflow-x-auto no-scrollbar pb-1">
                  {availableYears.map((yr) => {
                    const isSelected = yr === selectedYear;
                    return (
                      <button
                        key={yr}
                        onClick={() => {
                          setSelectedYear(yr);
                          const firstInYear = exams.find((e) => e.year === yr);
                          if (firstInYear) setExpandedExamId(firstInYear.id);
                        }}
                        className={`shrink-0 px-3 py-1 rounded-full text-xs font-medium transition-all active:scale-95 ${
                          isSelected
                            ? "bg-[#1d1d1f] dark:bg-[#f5f5f7] text-white dark:text-[#1d1d1f] shadow-xs"
                            : "bg-black/[0.04] dark:bg-white/[0.06] text-[#86868b] hover:text-[#1d1d1f] dark:hover:text-[#f5f5f7]"
                        }`}
                      >
                        {yr} 年
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Exam Set Selector for Selected Year */}
              <div className="space-y-1.5 pt-1">
                <span className="text-[11px] font-medium text-[#86868b]">真题套数</span>
                <div className="grid grid-cols-2 gap-2">
                  {examsInYear.map((ex) => {
                    const isExpanded = ex.id === expandedExamId;
                    const isCurrent = ex.id === currentExamId;
                    return (
                      <button
                        key={ex.id}
                        onClick={() => handleSelectExamInYear(ex.id)}
                        className={`px-3 py-2 rounded-xl text-left text-xs font-medium border transition-all active:scale-[0.98] flex items-center justify-between ${
                          isExpanded
                            ? "border-[#0071e3] bg-[#0071e3]/10 text-[#0071e3] dark:text-[#0a84ff]"
                            : "border-black/[0.06] dark:border-white/[0.08] hover:border-black/20 text-[#1d1d1f] dark:text-[#f5f5f7]"
                        }`}
                      >
                        <span className="truncate">{formatExamTitleZh(ex.title || ex.id)}</span>
                        {isCurrent && (
                          <span className="w-1.5 h-1.5 rounded-full bg-[#0071e3] shrink-0 ml-1.5" />
                        )}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Subparts / Sections in Expanded Exam */}
              <div className="pt-2">
                <div className="flex items-center justify-between pb-2 border-b border-black/[0.04] dark:border-white/[0.06]">
                  <span className="text-[11px] font-medium text-[#86868b] flex items-center gap-1">
                    <Layers className="w-3 h-3" />
                    题目小节列表
                  </span>
                  {isLoadingSubparts && (
                    <span className="text-[11px] text-[#86868b] animate-pulse">正在载入小节…</span>
                  )}
                </div>

                <div className="divide-y divide-black/[0.03] dark:divide-white/[0.04]">
                  {groupedSections.map((sec) => (
                    <div key={sec.id} className="py-2.5 space-y-1">
                      <div className="text-[11px] font-semibold text-[#86868b] dark:text-[#a1a1a6] px-2">
                        {sec.name}
                      </div>

                      <div className="space-y-0.5">
                        {sec.subparts.map((sp) => {
                          const isCurrent =
                            expandedExamId === currentExamId && sp.id === currentSubpartId;
                          const titleZh = formatSubpartTitleZh(sp.title, sp.question_range);

                          return (
                            <button
                              key={sp.id}
                              onClick={() => handleSelectSubpart(expandedExamId, sp.id)}
                              className={`w-full flex items-center justify-between px-2.5 py-2 rounded-lg text-left transition-all active:scale-[0.99] ${
                                isCurrent
                                  ? "bg-[#0071e3]/10 text-[#0071e3] font-semibold"
                                  : "hover:bg-black/[0.03] dark:hover:bg-white/[0.05] text-[#1d1d1f] dark:text-[#f5f5f7]"
                              }`}
                            >
                              <div className="flex items-center gap-2 min-w-0">
                                <span className="text-xs truncate">{titleZh}</span>
                                {sp.sentence_count ? (
                                  <span className="text-[10px] text-[#86868b] shrink-0 font-normal">
                                    {sp.sentence_count} 句
                                  </span>
                                ) : null}
                              </div>

                              {isCurrent ? (
                                <Check className="w-4 h-4 text-[#0071e3] shrink-0 ml-2" />
                              ) : (
                                <ChevronRight className="w-3.5 h-3.5 text-[#86868b]/60 shrink-0 ml-2" />
                              )}
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
});
