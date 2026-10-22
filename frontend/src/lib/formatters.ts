/**
 * 苹果设计风格与六级听力专业本地化工具函数
 */

// 数字转汉字序数
const CHINESE_NUMS: Record<number, string> = {
  1: "一",
  2: "二",
  3: "三",
  4: "四",
  5: "五",
  6: "六",
  7: "七",
  8: "八",
  9: "九",
  10: "十",
};

/**
 * 格式化真题名称
 * 示例：2016-06-set1 -> 2016年6月 第一套
 * 示例：2016年06月 六级真题 (第1套) -> 2016年6月 第一套
 */
export function formatExamTitleZh(examTitleOrId: string): string {
  if (!examTitleOrId) return "六级真题";

  // 匹配标准 id: YYYY-MM-setN
  const idMatch = examTitleOrId.match(/^(\d{4})-(\d{2})-set(\d+)$/i);
  if (idMatch) {
    const year = idMatch[1];
    const month = parseInt(idMatch[2], 10);
    const setNum = parseInt(idMatch[3], 10);
    const setZh = CHINESE_NUMS[setNum] || setNum;
    return `${year}年${month}月 第${setZh}套`;
  }

  // 匹配形如 "2016年06月 六级真题 (第1套)" 或 "2024.06六级..."
  let clean = examTitleOrId
    .replace(/大学英语六级考试真题/g, "")
    .replace(/六级真题/g, "")
    .replace(/六级听力/g, "")
    .replace(/听力音频/g, "")
    .replace(/（全国单套卷）/g, " 第一套")
    .replace(/（全1套）/g, " 第一套")
    .replace(/（全一套）/g, " 第一套")
    .replace(/[(（]第?(\d+)套[)）]/, (_, n) => ` 第${CHINESE_NUMS[parseInt(n, 10)] || n}套`)
    .trim();

  // 清洗月份前面的0，如 2016年06月 -> 2016年6月
  clean = clean.replace(/(\d{4})年0?(\d{1,2})月/, "$1年$2月");
  clean = clean.replace(/(\d{4})\.0?(\d{1,2})/, "$1年$2月");

  return clean;
}

/**
 * 格式化题号区间
 * 示例：Q1-Q4 -> （第1–4题）
 */
export function formatQuestionRangeZh(range?: string): string {
  if (!range) return "";
  const clean = range.replace(/^[Qq]/, "").trim();
  const m = clean.match(/^(\d+)\s*[-–~至]\s*[Qq]?(\d+)$/);
  if (m) {
    return `（第${m[1]}–${m[2]}题）`;
  }
  return range.startsWith("（") ? range : `（${range}）`;
}

/**
 * 格式化分节/子题标题
 * 示例：Conversation 1 (Q1-Q4) -> 长对话一（第1–4题）
 * 示例：Passage 2 -> 短文二（第12–15题）
 * 示例：Recording 3 -> 讲座三（第23–25题）
 */
export function formatSubpartTitleZh(
  title?: string,
  questionRange?: string
): string {
  if (!title) return "当前题目";

  let baseName = title;

  // 长对话
  const convMatch = title.match(/conversation\s*(\d+)/i);
  if (convMatch) {
    const num = parseInt(convMatch[1], 10);
    baseName = `长对话${CHINESE_NUMS[num] || num}`;
  }

  // 短文理解
  const passMatch = title.match(/passage\s*(\d+)/i);
  if (passMatch) {
    const num = parseInt(passMatch[1], 10);
    baseName = `短文${CHINESE_NUMS[num] || num}`;
  }

  // 讲座 / 讲话 / 报道
  const recMatch = title.match(/recording\s*(\d+)/i);
  if (recMatch) {
    const num = parseInt(recMatch[1], 10);
    baseName = `讲座${CHINESE_NUMS[num] || num}`;
  }

  // 附带题号
  const rangeZh = formatQuestionRangeZh(questionRange);
  return `${baseName}${rangeZh}`;
}

/**
 * 格式化说话人
 * Speaker M -> 男
 * Speaker W -> 女
 */
export function formatSpeakerZh(speaker?: string): string {
  if (!speaker) return "";
  const s = speaker.trim().toUpperCase();
  if (
    s === "M" ||
    s === "MAN" ||
    s === "MALE" ||
    s.startsWith("M:") ||
    s.includes("SPEAKER M")
  ) {
    return "男";
  }
  if (
    s === "W" ||
    s === "WOMAN" ||
    s === "FEMALE" ||
    s === "F" ||
    s.startsWith("W:") ||
    s.includes("SPEAKER W") ||
    s.includes("SPEAKER F")
  ) {
    return "女";
  }
  return speaker.replace(/^Speaker\s*/i, "");
}

/**
 * 格式化句子进度
 * 示例：1 / 25 -> 第 1 句 / 共 25 句
 */
export function formatProgressZh(current: number, total: number): {
  currentText: string;
  totalText: string;
  fullText: string;
} {
  const currentNum = current + 1;
  return {
    currentText: `第 ${currentNum} 句`,
    totalText: `共 ${total} 句`,
    fullText: `第 ${currentNum} 句 / 共 ${total} 句`,
  };
}
