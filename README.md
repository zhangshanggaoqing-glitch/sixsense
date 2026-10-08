# SixSense (六级精听工作台) 🎧

> **极简、声学保真、工匠级打磨的大学英语六级听力沉浸式精听系统。**  
> 秉承乔布斯标准：**100% 声学真值、单句语法切分、零题目污染、母语级工匠翻译、全套官方真题题库与逐词毫秒级卡拉OK高亮。**

---

## 🌟 核心特性

- 🎯 **100% 声学真值 (Acoustic Truth)**：所有句子对齐 Whisper 原始音频词级时间戳，杜绝网上流传的虚假转述与截断错版。
- ✂️ **单句精细切分 (Fine-Grained Segmentation)**：告别长段落，严格按单句语法切分（平均时长 4~8s，最大时长严格 < 18s），支持针对单句无限循环复读。
- 🎙️ **零题目污染与零硬钳 (Zero Question Bleed & Clamps)**：篇章边界在播音员报题前严格截止，拒绝 32s 伪截断。
- 🎨 **母语级工匠翻译 (Artisan Translations)**：100% 逐句精准人工润色，自然流畅，零机翻生硬感。
- 📝 **全真题题库深度集成**：包含完整题目题干、4 个官方选项、权威正确答案与名师解析。
- 🎵 **流式音频传输 (HTTP 206 Partial Content)**：毫秒级响应任意拖动与区间循环，戴上耳机 2 秒内沉浸精听。

---

## 📁 目录结构

```text
├── backend/            # FastAPI 后端服务
│   ├── app/
│   │   ├── routers/    # 路由 (exams, audio, vocab, progress)
│   │   ├── config.py   # 配置管理
│   │   ├── database.py # SQLite 数据库连接与初始化
│   │   └── main.py     # 入口文件
│   └── Dockerfile      # 后端容器化构建
├── frontend/           # Next.js 14 + Tailwind CSS 前端
│   ├── src/
│   │   ├── app/        # 页面路由 (首页列表、/studio 精听工作台)
│   │   ├── components/ # 精听播放器、题目卡片、单句列表组件
│   │   └── lib/        # API 请求与音频控制逻辑
│   └── Dockerfile      # 前端容器化构建
├── data/
│   ├── sixsense.db     # SQLite 核心数据库（包含全部真题与声学标注数据）
│   └── audio/          # 存放本地音频文件的目录（可选）
├── docker-compose.yml  # Docker 一键编排文件
├── start.sh            # 生产级本地启动脚本
├── stop.sh             # 生产级停止脚本
└── requirements.txt    # 后端 Python 依赖
```

---

## 🚀 快速启动

### 方式一：本地直接运行 (开发/生产环境)

#### 1. 环境准备
- Python 3.10+
- Node.js 18+ (推荐 Node 20)

#### 2. 安装依赖
```bash
# 1. 安装后端依赖
pip install -r requirements.txt

# 2. 安装前端依赖并构建
cd frontend
npm install
npm run build
cd ..
```

#### 3. 一键启动
```bash
bash start.sh
```
- 前端工作台：[http://localhost:3000](http://localhost:3000)
- 后端 API：[http://localhost:8000](http://localhost:8000)
- API 文档：[http://localhost:8000/docs](http://localhost:8000/docs)

停止服务：
```bash
bash stop.sh
```

---

### 方式二：Docker Compose 一键云端部署（推荐，摆脱本地笔记本）

适合部署在阿里云、腾讯云、AWS、轻量应用服务器或任何 Linux VPS 上：

```bash
# 1. 克隆代码
git clone https://github.com/zhangshanggaoqing-glitch/sixsense.git
cd sixsense

# 2. 启动容器服务
docker compose up -d
```
启动后即可直接通过服务器公网 IP 访问：
- 前端端口：`3000`
- 后端端口：`8000`

---

## ☁️ 云端音频配置指南

音频文件体积较大（历年真题完整 MP3 约 1.1GB），推荐以下三种云端存储方式：

1. **直接存放在服务器目录**：
   将音频文件上传到服务器的 `./data/audio/` 目录下，后端会自动递归检索。
2. **挂载外部持久化卷**：
   在 `docker-compose.yml` 中配置：
   ```yaml
   volumes:
     - /your/host/audio/dir:/app/data/audio
   ```
3. **环境变量指定路径**：
   设置 `CET6_RAW_SOURCE_DIR=/your/audio/path`，后端将自动在此路径下检索音频。

---

## ⌨️ 精听工作台核心快捷键

- `Space`：播放 / 暂停当前单句
- `R`：重听当前单句
- `Up` / `Down`：切换上一个 / 下一个句子
- `1` / `2` / `3` / `4`：快速切换显示模式（盲听模式、英文模式、中文模式、双语模式）
- `D`：一键开启听写对比模式

---

## 📜 开源许可
MIT License.
