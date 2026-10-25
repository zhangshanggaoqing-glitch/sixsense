# SixSense (石头听力 / mystone.top) 🎧

<p align="center">
  <a href="https://mystone.top"><strong>在线体验 Online Demo: mystone.top</strong></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Next.js-14-black?style=flat-square&logo=next.js" alt="Next.js" />
  <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi" alt="FastAPI" />
  <img src="https://img.shields.io/badge/TailwindCSS-3.4-38B2AC?style=flat-square&logo=tailwind-css" alt="Tailwind" />
  <img src="https://img.shields.io/badge/SQLite-WAL_Mode-003B57?style=flat-square&logo=sqlite" alt="SQLite" />
  <img src="https://img.shields.io/badge/License-MIT-blue.svg?style=flat-square" alt="MIT License" />
</p>

> **极简、声学保真、工匠级打磨的大学英语六级沉浸式精听系统。**  
> 遵循 Steve Jobs / Apple 极简主义设计准则：少即是多，拒绝冗长堆砌与营销腔，一屏聚焦一件事，为中国大学生打造真正能「静心听懂」的听力利器。  
> **A minimalist, acoustically faithful, artisan-crafted CET-6 listening workspace.** Designed around Steve Jobs' "less is more" philosophy.

---

## 目录 / Table of Contents

- [中文说明 (Chinese)](#中文说明)
  - [设计哲学 (Design North Star)](#设计哲学)
  - [核心功能特性](#核心功能特性)
  - [系统技术架构](#系统技术架构)
  - [快速开始与部署](#快速开始与部署)
  - [快捷键清单](#快捷键清单)
- [English Documentation](#english-documentation)
  - [Philosophy & Overview](#philosophy--overview)
  - [Key Features](#key-features)
  - [Tech Stack](#tech-stack)
  - [Quick Start & Deployment](#quick-start--deployment)
  - [Keyboard Shortcuts](#keyboard-shortcuts)
- [开源协议 (License)](#开源协议-license)

---

## 中文说明

### 设计哲学

1. **少即是多 (Less is More)**：不加装饰性渐变、彩色图标墙与弹窗打扰；中性黑灰基调 + 少量苹果蓝强调色。
2. **声学真值 (Acoustic Truth)**：基于 Whisper 原始音频词级时间戳，100% 对齐真实发音，严格按语法单句切分，拒绝错版与长段截断。
3. **静默有用 (Silent Utility)**：粘性功能服务于学习习惯而非游戏感表演；打卡卡极简呈现，不弹冗余提醒。

---

### 核心功能特性

#### 1. ⚡ 首听极简体验 (1-Click First Listen)
- 首页主行动点一键直达「先听一句」，默认载入最新 2026 年真题第一句并秒级起播。
- 默认双语对照精听模式，不设注册门槛，新访客 5 分钟内顺利听完第一句。
- 当浏览器策略拦截自动播放时，页面视口中央自动呈现极简黑底胶囊「点击播放」，一次点击立刻出声。

#### 2. ⏸️ 双播放节奏与单句循环 (Playback Pace & Loop)
- **一句一停（默认）**：当前句播完后，播放指针自动定位到下一句起始时间并暂停，界面同步展示下一句文案，点击播放即听下一句。专为需要听一句、想一句、核对一句的深度精听设计。
- **连贯播放**：当前句播完自动推进并连续播放下一句，直至篇章末尾，还原考场真实语流。
- **单句循环**：快捷键 `R` 或点击循环按钮，句末严格重播当前句，优先级高于播放节奏，便于反复推敲难句。
- 记忆用户所选节奏（`localStorage` 持久化），下次进入自动保持偏好。

#### 3. 🔁 智能无缝续播 (Continue CTA)
- 听完任意一句、切题、暂停或离开页面时，毫秒级将进度写入本地缓存与服务端。
- 返回首页时，主按钮智能变更为「继续第 N 句」，副文案标注对应真题套数，点击直接跳回断点续听，告别每次重头找题。

#### 4. 🛡️ 访客身份隔离与无损合并 (Guest Isolation)
- 未登录访客分配稳定独立的本地 UUID 身份，彻底杜绝多端串号或共用进度。
- 登录账号时，自动无损合并游客期间的精听时长、学习进度与生词本。

#### 5. 🔥 可靠连续打卡与静默勋章 (Streak & Medals)
- **连续天数**：按 `Asia/Shanghai` 自然日切，当天有效精听满 60 秒即记为有效打卡日。首页秒级优先读本地缓存，坚决不闪「假 0」。
- **极简打卡分享卡**：纯客户端 HTML5 Canvas 渲染的 Apple 极简风格打卡图，一键导出 PNG 或复制，无第三方图片渲染依赖。
- **三枚静默勋章**：权威且克制，仅设「首听」、「连续3天」、「连续7天」，不搞繁杂打卡墙。

#### 6. 📝 词级卡拉OK高亮、查词与生词本
- 播放过程中随音频推进实现词级毫秒级平滑高亮。
- 单击/双击句子中的任意单词直接调出权威英汉词典释义及英/美发音，支持一键加入生词本。
- 生词本具备原生朗读与音频片段回溯播放。

#### 7. 📊 极简自建管理后台 (/admin)
- 包含全站总请求 PV、独立访客 IP 数量 UV、累计精听总分钟、今日精听分钟、活跃用户与热门真题分布看板。

---

### 系统技术架构

```text
sixsense/
├── backend/                  # FastAPI 高性能后端
│   ├── app/
│   │   ├── routers/
│   │   │   ├── exams.py      # 真题、篇章与单句检索
│   │   │   ├── progress.py   # 进度持久化、心跳与打卡算法
│   │   │   ├── vocab.py      # 生词本与词典
│   │   │   ├── auth.py       # JWT 鉴权与游客迁移
│   │   │   └── admin.py      # 运营大盘数据统计
│   │   ├── config.py         # 环境变量配置
│   │   ├── database.py       # SQLite 连接与连接池
│   │   └── main.py           # 路由挂载与 CORS 中间件
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                 # Next.js 14 (App Router) + Tailwind CSS 前端
│   ├── src/
│   │   ├── app/
│   │   │   ├── page.tsx      # 极简首页（今日时长、连续天数、继续第N句）
│   │   │   ├── studio/       # 沉浸精听工作台
│   │   │   ├── vocabulary/   # 生词本管理
│   │   │   └── admin/        # 运营后台看板
│   │   ├── components/
│   │   │   ├── studio/       # AudioBar 控制条、SentenceCard 句子卡片、打卡弹窗
│   │   │   └── vocabulary/
│   │   ├── hooks/            # useAudioPlayer (音频核), useKeyboardShortcuts, useAuth
│   │   └── lib/              # api.ts (请求封装与本地缓存治理)
│   ├── Dockerfile
│   └── package.json
├── data/
│   ├── sixsense.db           # 包含六级全部声学标注真题的 SQLite 数据库
│   └── audio/                # 完整真题 MP3 音频存放目录
└── docker-compose.yml        # 一键容器编排
```

---

### 快速开始与部署

#### 方式一：Docker Compose 一键部署（生产推荐）

适用于阿里云、腾讯云、Oracle Cloud 或任何 Linux VPS：

```bash
# 1. 克隆代码仓库
git clone https://github.com/zhangshanggaoqing-glitch/sixsense.git
cd sixsense

# 2. 启动服务容器
docker compose up -d --build
```
启动完成后访问：
- 前端 Web 访问地址：`http://your-server-ip:3000`
- 后端 API 地址：`http://your-server-ip:8000`
- 交互式 Swagger 文档：`http://your-server-ip:8000/docs`

配置 Nginx 反向代理与 SSL 证书后即可绑定域名（如 `https://mystone.top`）。

#### 方式二：本地开发运行

##### 1. 环境需求
- Python 3.11+
- Node.js 18+ (推荐 Node 20 LTS)

##### 2. 后端服务启动
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 启动 FastAPI
uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload
```

##### 3. 前端工程启动
```bash
cd frontend
npm install
npm run dev
```
打开浏览器访问 [http://localhost:3000](http://localhost:3000)。

---

### 快捷键清单

在精听工作室（`/studio`）中支持纯键盘盲操：

| 快捷键 | 功能 |
| :--- | :--- |
| `Space` | 播放 / 暂停当前单句 |
| `←` / `→` | 切换到上一句 / 下一句 |
| `R` | 开启 / 关闭单句循环模式 |
| `1` | 切换为 **盲听模式**（英中文本隐藏，专注声音辨析） |
| `2` | 切换为 **双语模式**（英中文本对照精听） |
| `3` | 切换为 **单句听写实战**（键盘输入并自动比对打分） |

---

## English Documentation

### Philosophy & Overview

**SixSense** (石头听力) is an artisan-grade listening workspace for the College English Test Band 6 (CET-6). Built from the ground up under Steve Jobs' minimalist principles, it eliminates unnecessary decorations, banners, marketing jargon, and gamification bloat, letting students focus solely on sentence-level deliberate practice.

- **Acoustic Truth**: Every sentence is meticulously aligned with Whisper-derived word-level acoustic timestamps, preventing arbitrary cuts or misheard transcripts.
- **Natural Translations**: 100% human-polished, idiomatic Chinese translations alongside authentic CET-6 test sets.
- **HTTP 206 Streaming**: Sub-second range-seeking and looping directly over full-length high-fidelity MP3s.

---

### Key Features

1. **Frictionless Onboarding**:
   - Primary hero CTA "Listen to One Sentence" immediately launches the studio into the latest exam paper.
   - Defaults to bilingual mode with zero initial sign-up walls.
   - Bulletproof fallback: If the browser rejects autoplay, an Apple-style dark capsule "Click to Play" appears instantly and vanishes upon user interaction.

2. **Dual Playback Paces**:
   - **Pause Each Sentence (`pause_each`, default)**: When the current sentence reaches its end, the player advances to the next sentence's text and timecode, then pauses. Ideal for deep contemplation.
   - **Continuous (`continuous`)**: Automatically flows into subsequent sentences for real exam simulation.
   - **Single-Sentence Loop (`R`)**: Repeats the active sentence indefinitely, prioritizing mastery over difficult utterances.
   - Preference saved automatically to `localStorage` (`stone_playback_pace`).

3. **Intelligent "Continue Sentence N" Resume**:
   - Saves progress instantly upon completion, sentence transition, pause, or page departure (`visibilitychange` / `beforeunload`).
   - Home screen hero CTA dynamically updates to "Continue Sentence N", letting learners resume where they left off.

4. **Isolated Guest Sessions & Cloud Merge**:
   - Uses device-isolated UUIDs for non-logged-in visitors, preventing cross-device interference.
   - Transparently merges accumulated minutes, vocabulary, and progress into registered accounts upon sign-in.

5. **Authoritative Streaks & Silent Medals**:
   - Computes streaks daily at Asia/Shanghai midnight whenever active listening reaches $\ge$ 60 seconds.
   - Zero-dependency client-side HTML5 Canvas generating clean, shareable achievement cards.
   - Only 3 silent medals: *First Listen*, *3-Day Streak*, and *7-Day Streak*.

6. **Word-Level Highlighting & Vocabulary Notebook**:
   - Precise karaoke-style word highlighting synchronized with the audio track.
   - Instant word definition popover with authentic UK/US pronunciation and 1-click vocabulary collection.

7. **Minimalist Admin Dashboard (`/admin`)**:
   - Tracks site Page Views (PV), Unique Visitors (UV), total active listening minutes, and popular test sections in real time.

---

### Tech Stack

- **Frontend**: Next.js 14 (App Router), React 18, TypeScript, Tailwind CSS, Lucide Icons.
- **Backend**: FastAPI, Uvicorn, SQLite3 (WAL mode), Pydantic v2, Python-Jose (JWT).
- **Deployment**: Docker Compose, Nginx Reverse Proxy with HTTP Range partial streaming.

---

### Quick Start & Deployment

#### Option 1: Docker Compose (Production)

```bash
git clone https://github.com/zhangshanggaoqing-glitch/sixsense.git
cd sixsense
docker compose up -d --build
```
Access points:
- Frontend: `http://localhost:3000`
- API docs: `http://localhost:8000/docs`

#### Option 2: Local Development

```bash
# 1. Backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn backend.app.main:app --port 8000 --reload

# 2. Frontend
cd frontend
npm install
npm run dev
```

---

### Keyboard Shortcuts

| Shortcut | Description |
| :--- | :--- |
| `Space` | Toggle Play / Pause |
| `←` / `→` | Jump to Previous / Next Sentence |
| `R` | Toggle Single-Sentence Loop |
| `1` | Blind Listening Mode (Audio only) |
| `2` | Bilingual Mode (English + Chinese text) |
| `3` | Dictation Mode (Real-time transcription diff) |

---

## 开源协议 (License)

本项目采用 [MIT License](LICENSE) 开源协议。  
Released under the [MIT License](LICENSE).
