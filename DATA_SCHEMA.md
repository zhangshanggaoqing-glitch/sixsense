# SixSense 数据模型与规范 (DATA_SCHEMA.md)

> **版本**：v1.0.0  
> **设计思想**：分层实体模型（Exam → Section → Dialogue/Passage → Sentence → Word），严格的数据来源追踪（Provenance Tracking）。

---

## 1. 核心业务实体模型 (Core Data Entities)

### 1.1 试卷实体 (`Exam`)
```json
{
  "id": "2020-07-set1",
  "year": 2020,
  "month": 7,
  "set_number": 1,
  "title": "2020年07月大学英语六级考试真题（全国单套卷）",
  "audio_file": "202007-CET6 听力.mp3",
  "audio_duration_seconds": 1611.15,
  "sections_count": 3,
  "total_sentences": 128,
  "is_golden": true
}
```

### 1.2 听力大项 (`Section`)
```json
{
  "id": "2020-07-set1-section-a",
  "exam_id": "2020-07-set1",
  "type": "Section A",
  "title": "Long Conversations",
  "order": 1,
  "subparts": [
    {
      "id": "conv-1",
      "type": "conversation",
      "title": "Conversation One: Olympic Champion & Technology in Sports",
      "start_time": 95.20,
      "end_time": 320.45,
      "questions": [1, 2, 3, 4]
    }
  ]
}
```

### 1.3 句子实体 (`Sentence`) — 核心精听原子单元
```json
{
  "id": "2020-07-s0014",
  "exam_id": "2020-07-set1",
  "section_id": "2020-07-set1-section-a",
  "subpart_id": "conv-1",
  "order": 14,
  "speaker": "W",
  "start_time": 142.350,
  "end_time": 148.120,
  "english": "The book is about how science and technology has helped push humans to the edge of their physical abilities.",
  "chinese": "这本书主要探讨科学与技术如何助推人类迫近体能极限。",
  "words": [
    {"word": "The", "start": 142.35, "end": 142.50},
    {"word": "book", "start": 142.52, "end": 142.85},
    {"word": "is", "start": 142.88, "end": 143.01},
    {"word": "about", "start": 143.05, "end": 143.32},
    {"word": "how", "start": 143.35, "end": 143.52},
    {"word": "science", "start": 143.55, "end": 143.98}
  ],
  "provenance": {
    "english_source": "official_pdf_native_text",
    "translation_source": "provided_explanation_full_translation",
    "alignment_source": "torchaudio_wav2vec2_ctc",
    "confidence": 0.985,
    "manually_verified": false
  }
}
```

### 1.4 生词本项 (`VocabularyItem`) — 语境化生词
```json
{
  "id": "vocab_profound_001",
  "word": "profound",
  "lemma": "profound",
  "phonetic": "/prəˈfaʊnd/",
  "part_of_speech": "adj.",
  "definition_zh": "深刻的；深远的；深奥的",
  "cet_level": "CET-6",
  "source_sentence_id": "2020-07-s0014",
  "source_sentence_en": "The findings have profound implications for public policy.",
  "source_sentence_zh": "这些发现对公共政策具有深远的影响。",
  "exam_id": "2020-07-set1",
  "audio_clip_start": 142.35,
  "audio_clip_end": 148.12,
  "created_at": 1727610000,
  "review_count": 0,
  "mastery": 0.0
}
```

### 1.5 听写记录 (`DictationAttempt`)
```json
{
  "id": "dict_att_10023",
  "sentence_id": "2020-07-s0014",
  "user_input": "The book is about how science and technology has help push human to the edge.",
  "standard_text": "The book is about how science and technology has helped push humans to the edge of their physical abilities.",
  "accuracy_score": 0.82,
  "errors_breakdown": {
    "missing_words": ["of", "their", "physical", "abilities"],
    "form_errors": [
      {"word": "helped", "user_input": "help", "type": "tense"},
      {"word": "humans", "user_input": "human", "type": "plural"}
    ],
    "extra_words": []
  },
  "created_at": 1727610120
}
```

### 1.6 有效学习心跳与会话 (`ListeningSession`)
```json
{
  "id": "session_20260929_01",
  "start_time": 1727610000,
  "end_time": 1727611800,
  "active_seconds": 1080,
  "exam_id": "2020-07-set1",
  "sentences_played": 42,
  "sentences_repeated": 18,
  "dictation_attempts": 6,
  "new_words_count": 3
}
```

### 1.7 用户全局偏好与续听进度 (`UserProgress & Settings`)
```json
{
  "last_resume": {
    "exam_id": "2020-07-set1",
    "section_id": "2020-07-set1-section-a",
    "sentence_index": 14,
    "playback_rate": 1.0,
    "display_mode": "C",
    "loop_mode": "off",
    "volume": 0.9
  },
  "settings": {
    "theme": "dark",
    "auto_replay_on_navigate": true,
    "dictation_tolerance_level": "standard",
    "keyboard_layout": "default"
  }
}
```
