# SixSense 语料库入库进展记录 (walkthrough.md)

> 本文件记录每套六级真题听力语料的精细化摄取过程与结果，作为工程交付台账。
> 每一套试卷入库后，全库 `python3 pipeline/qa_audit.py` 必须保持 **0 Errors, 0 Warnings**。

---

## 一、黄金质检红线（不可逾越）

| 编号 | 红线要求 | 审计脚本校验点 |
| --- | --- | --- |
| R1 | 严格切分为 7 个子篇章（conv-1/conv-2/pass-1/pass-2/rec-1/rec-2/rec-3） | `len(subparts) == 7` |
| R2 | 每个子篇章有提炼准确的中文主旨与题号范围 | `topic_zh` 含汉字且非空 |
| R3 | 严禁孤立单词、破损残句（Zero Fragments） | 句长 ≥ 2 字符 |
| R4 | 英文句子首字母大写、标点闭合 | 句尾匹配 `[.?!\"”']$` |
| R5 | 100% 中英双语配对，零空翻译 | `chinese` 含汉字 |
| R6 | 时间戳严格单调递增且限制在 Subpart 时间窗内 | `start_time < end_time` |
| R7 | 单句时长不得超过 35 秒（34s 熔断：`e_time = s_time + 32.0`） | `end - start <= 35.0` |
| R8 | 严格 25 题，题干与 A/B/C/D 选项完整，答案与解析翔实 | 题数、选项非空、答案为 A/B/C/D、解析含中文 |

---

## 二、入库台账

| # | Exam ID | 试卷 | 音频时长 | 句子数 | 题数 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `2019-06-set1` | 2019年06月 六级真题 (第1套) | 1652.19s | 108 | 25 | ✅ GOLDEN |

### 2019-06-set1 详情

**音频**：`2019年06月六级听力第1套.mp3`（1652.19s）
**音频路径**：`/home/stone/桌面/听力/01-六级历年真题及答案解析+听力音频/2019年06月CET6题+解+音频/04、听力音频/`

**来源材料**
- 真题 Word：`02、真题word版/2019年06月六级真题（第1套）.docx`（25 题题干与选项完整）
- 答案解析 PDF：`03、答案解析/2019年06月真题解析第1套.pdf`（Kodak 扫描件，56 页，`pdftotext` 提取为空 → `pdftoppm -png -r 150` + `tesseract chi_sim+eng` OCR 提取第 3–28 页，成功取得全部听力原文、设题要点与答案精析）
- Whisper：`data/derived/exams/2019-06-set1/whisper_full.json`（base.en / CPU 8 线程 int8 / 260 segments / 2943 words / 305.6s）

**7 子篇章切分与声学边界**

| Subpart | 内容 | 声学窗口 | 句数 | 题号 |
| --- | --- | --- | --- | --- |
| conv-1 | 婚礼派对初识：难缠客户项目收官、烘焙与摄影爱好 | [39.27, 232.70] | 18 | Q1–Q4 |
| conv-2 | 大学与高中生活差异：自我责任、时间管理、择友与社团 | [232.70, 363.98] | 17 | Q5–Q8 |
| pass-1 | 滑雪传奇基利：跳出常规思维、技术创新与冬奥三金 | [479.02, 668.03] | 14 | Q9–Q11 |
| pass-2 | 负面情绪危害：豚鼠实验、毒素生成与身心关联 | [668.03, 791.21] | 14 | Q12–Q15 |
| rec-1 | 初学者与行家的注意焦点差异、心流误区与眼动追踪实验 | [899.76, 1136.03] | 14 | Q16–Q18 |
| rec-2 | 亚洲瘦身热潮：节食法与瘦身产品猎奇、东西方审美差异 | [1136.03, 1369.85] | 17 | Q19–Q21 |
| rec-3 | 人类成为裸猿：散热压力、皮肤色素与走出非洲后的基因变化 | [1369.85, 1562.35] | 14 | Q22–Q25 |

**答案与考点印证**（经 OCR 原文 + 精析双向核对）

| Q | 答案 | 原文定位依据 | Q | 答案 | 原文定位依据 |
| --- | --- | --- | --- | --- | --- |
| 1 | C | `a project with a difficult client` | 14 | D | `impossible to be fearful, anxious, irritated and healthy at the same time` |
| 2 | A | `taking photos during the big event as a wedding gift` | 15 | A | `The mind-body connection is such that...` |
| 3 | B | `I was a bit nervous saying yes` | 16 | B | `With experts, it's just the other way around` |
| 4 | A | `you could very well open your own shop` | 17 | D | `pay close attention to the demands of high performance` |
| 5 | C | `take more individual responsibility for your actions` | 18 | C | `It supports what we might almost think of as conventional wisdom` |
| 6 | D | `you are expected to behave like an adult` | 19 | D | `overwhelmed with a wide range of different slimming products` |
| 7 | B | `keep the friends who respect your student commitments` | 20 | B | `it just reminded me of the roasted ham` |
| 8 | D | `unless they are directly related to your study` | 21 | A | `shaped by a person's culture, as well as how they were raised` |
| 9 | A | `minds wander outside traditional ways of thinking` | 22 | A | `naked ape` + `so many different shades` |
| 10 | B | `experiments resulted in a new style` | 23 | B | `keep ourselves cool when we were moving around vigorously in a hot environment` |
| 11 | C | `won three gold medals in the Winter Olympics` | 24 | C | `turned our skin darker to serve as a natural sun protector` |
| 12 | D | `have killed them in less than two minutes` | 25 | A | `real changes in the genetic makeup of natural coloring` |
| 13 | A | `affects your body chemistry within a split second` | | | |

**对齐算法演进（经验沉淀）**

模板中「首 token 定位 + 末 token 回扫」的贪心匹配在本次语料上出现严重漂移：

1. 首版（模板原样）：conv-1 第 13–18 句全部塌缩到时间窗右边界 232.70s，单调性虽通过但声学位置完全失真。
2. 二版（最长连续命中 run 打分）：在 `I'm` vs `I am` 等缩写差异处仍会误锚，第 4、12 句仍偏 20s 以上。
3. 三版（**最终采用**）：对整个 Subpart 做 `difflib.SequenceMatcher` **全局序列比对**，参考流为校订后逐句 token 流，Whisper 流为归一化后的字级词流；`equal` 区块直接映射，`replace` 区块按句内 token 占比分配。配合 `normalize_token()` 统一处理 `'s / 're / 've / 'll / 'd` 缩写与撇号，可稳定产出严格单调、不重叠、不溢窗的时间戳。

熔断防御保留：`if e_time - s_time > 34.0: e_time = round(s_time + 32.0, 2)`

**产出文件**
- `pipeline/generate_data_2019_06_set1.py`
- `pipeline/data_2019_06_set1.py`
- `pipeline/curate_2019_06_set1.py`
- `data/derived/exams/2019-06-set1/whisper_full.json`

**质检结果**

```
[Exam Audit] 2019-06-set1: 2019年06月 六级真题 (第1套)
  Audio: 2019年06月六级听力第1套.mp3 (1652.19s), Golden: 1
  [PASS] Audio file verified on disk
  [PASS] 7 subparts present
  Total sentences: 108
  [PASS] 100% sentences have authentic Chinese translations (0 empty)
  [PASS] 0 broken English sentence fragments
  [PASS] Monotonic acoustic word-level timestamps valid
  Total questions: 25
  [PASS] Exactly 25 official questions present

Audit Summary: 0 Errors, 0 Warnings
[SUCCESS] All audited exams passed 100% QA standards!
```

---

## 三、累计入库统计

| 指标 | 数值 |
| --- | --- |
| 已入库试卷 | 30 套 |
| 黄金句子总数 | 4,385 句 |
| 官方题目总数 | 750 题 |
| 全库 QA 状态 | **0 Errors, 0 Warnings** ✅ |

### 各年份套数分布

| 年份 | 已入库 |
| --- | --- |
| 2019 | 3 套（06-set1、12-set1、12-set2） |
| 2020 | 4 套（07、09、12-set1、12-set2） |
| 2021 | 4 套 |
| 2022 | 4 套 |
| 2023 | 5 套 |
| 2024 | 4 套 |
| 2025 | 4 套 |
| 2026 | 2 套 |

### 待推进队列（沿时间轴向前回溯）

- [ ] `2019-06-set2` ← **当前进行中**
- [ ] `2019-06-set3`（该套音频需查阅同目录说明文件确认）
- [ ] 2018 年及以前：`/home/stone/桌面/听力/1990年-2018年真题资料【合集】/`
