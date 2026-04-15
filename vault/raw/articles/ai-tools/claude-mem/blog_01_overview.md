# Claude-Mem 深度解析（一）：跨会话记忆系统的设计哲学

> **系列导言**：Claude Code 是一个强大的 AI 编程助手，但它有一个致命弱点——每次新建会话，前一次会话积累的所有上下文都会消失，就像一位每天早上失忆的开发伙伴。Claude-Mem 正是为解决这个问题而生的持久化记忆插件。本系列将逐层拆解其架构精髓。

---

## 背景：LLM 的"失忆困境"

大型语言模型在设计上是**无状态的（stateless）**。每一次 API 调用、每一个新会话，模型都从零开始。对于日常问答场景，这无关紧要；但对于持续多天、甚至数周的软件开发项目，这就成了生产力杀手。

你昨天调试 JWT 鉴权时发现的那个关键逻辑边界，今天 Claude 毫无印象。上周重构时摸索出来的数据库连接池最优配置，新会话里你需要重新解释一遍。这种**重复解释的摩擦成本**，随项目时间线性增长。

Claude-Mem 的核心命题很简单：**让 AI 编程助手拥有真实的项目记忆**。

---

## 核心定位：什么是 Claude-Mem？

Claude-Mem 是一个 **Claude Code 插件**（Plugin），通过 Claude Code 的钩子系统（Hook System）实现：

1. **自动捕获**：实时监听会话中的所有工具调用（读取文件、执行命令、写代码等）
2. **AI 压缩**：用 Claude Agent SDK 将原始工具日志提炼成结构化「观察记录」（Observations）
3. **持久存储**：将压缩后的记忆存入本地 SQLite 数据库
4. **智能注入**：下次会话启动时，自动将相关历史上下文注入到 Claude 的初始提示词中

整个过程**无需用户手动干预**，完全在后台异步运行。

---

## 系统整体架构鸟瞰

Claude-Mem 的架构可以用一个"两进程 + 一数据库"的模型来理解：

```
┌─────────────────────────────────────────────┐
│            Claude Code (主进程)              │
│                                             │
│  用户输入 → Claude 推理 → 工具调用 → 输出   │
│       ↕ (via stdin/stdout Hook)             │
│  ┌─────────────────────────────────────┐   │
│  │      Hook 脚本群（6个JS文件）        │   │
│  │  context / new / save / summary /   │   │
│  │  cleanup / user-message hooks       │   │
│  └────────────────┬────────────────────┘   │
└───────────────────┼─────────────────────────┘
                    │ HTTP (fire-and-forget)
                    ↓
┌─────────────────────────────────────────────┐
│       Worker Service（后台常驻进程）         │
│                                             │
│  Express.js HTTP Server (port 37777)        │
│  ├── Claude Agent SDK（AI 压缩引擎）         │
│  ├── SessionManager（会话状态管理）          │
│  ├── SSE 实时推送                           │
│  └── Viewer UI (React Web界面)              │
│                    ↕                        │
│  ┌──────────────────────────────────────┐  │
│  │     SQLite Database + ChromaDB       │  │
│  │  sessions / observations / summaries │  │
│  │  FTS5 全文检索 + 向量相似度检索      │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

---

## 五大核心组件一览

| 组件 | 技术栈 | 核心职责 |
|------|--------|---------|
| **Plugin Hooks（钩子层）** | Node.js / TypeScript | 监听 Claude Code 生命周期事件，捕获原始数据 |
| **Worker Service（工作服务层）** | Express.js + Bun | 异步 AI 处理、HTTP API、SSE 实时推送 |
| **Database Layer（数据库层）** | SQLite + FTS5 + ChromaDB | 结构化存储 + 全文检索 + 语义向量检索 |
| **Search System（检索系统）** | MCP Tools + 3层工作流 | 高效的"渐进式披露"记忆检索 |
| **Viewer UI（可视化界面）** | React + TypeScript | 实时记忆流可视化，端口 37777 |

---

## 技术选型的精妙之处

### 为什么用 Bun 而非 Node.js 作进程管理器？

Bun 是一个现代 JavaScript 运行时，内置进程管理、高性能 SQLite 驱动（`bun:sqlite`）以及极低的冷启动时间。Claude-Mem 早期使用 PM2（Node.js 生态的进程管理工具），v4+ 后迁移到 Bun 原生管理，带来了两个关键优势：

- **无需额外依赖**：不再需要全局安装 PM2
- **SQLite 集成更优**：`bun:sqlite` 比 `better-sqlite3` 性能更高，支持 WAL 模式

### 为什么不用 Redis / PostgreSQL？

Claude-Mem 的设计目标是**零基础设施依赖的本地部署**——用户只需安装 Node.js，不需要搭建任何外部服务。SQLite + FTS5 的组合在单机场景下完全满足需求：

- FTS5（Full-Text Search 5）是 SQLite 内置的全文检索虚拟表，支持 BM25 排序
- 对于向量语义检索，使用可选的 ChromaDB（Python 进程，按需自动安装）

### 为什么 Hook 采用"即发即忘"（fire-and-forget）模式？

Claude Code 的 Hook 脚本有严格的**超时限制**（默认 120 秒），更关键的是，AI 压缩处理可能需要数秒甚至更长时间。如果 Hook 同步等待 Worker 处理完成，就会直接阻塞用户的编码流程。

因此，所有 Hook → Worker 的通信都采用：
```
POST http://127.0.0.1:37777/api/... (timeout: 2000ms)
```

Hook 发出请求后立即返回，Worker 在后台异步完成 AI 压缩。这是一个经典的**生产者-消费者解耦模式**。

---

## 数据流的全生命周期

一次完整的 Claude Code 会话，数据在 Claude-Mem 中经历的旅程：

```
1. 会话启动
   └─ context-hook 触发
      └─ 从数据库读取最近 N 条 observations
      └─ 注入到 Claude 的初始上下文 (additionalContext)

2. 用户输入提示词
   └─ new-hook 触发
      └─ 创建/更新 session 记录
      └─ 保存 user_prompt（去除 <private> 标签后）

3. Claude 使用工具（可能触发 100+ 次）
   └─ save-hook 触发（每次工具调用后）
      └─ 过滤低价值工具（TodoWrite、SlashCommand 等）
      └─ 发送 tool_name + tool_input + tool_response 到 Worker
      └─ Worker 用 Claude Agent SDK 压缩为结构化 Observation
      └─ 存入 SQLite + ChromaDB

4. 用户停止问答
   └─ summary-hook 触发
      └─ 读取 transcript.jsonl 最后几条消息
      └─ 生成会话摘要（request / completed / learnings）

5. 会话结束
   └─ cleanup-hook 触发
      └─ 标记 session 为 completed（不删除，保留记忆）
```

---

## 隐私保护设计：`<private>` 标签

Claude-Mem 引入了一个优雅的隐私控制机制。用户可以在提示词中用 `<private>` 标签包裹不想被记录的内容：

```
帮我分析这个 API Key：<private>sk-abc123...</private>

这段逻辑有 bug，帮我看看
```

系统会在数据进入 Worker 之前的**边缘层**（Hook 脚本中）剥离这些标签，防止敏感信息进入任何存储介质。

此外还有一个自动注入的系统标签 `<claude-mem-context>`，用于标记那些从数据库注入的历史上下文，防止它们被二次压缩存储（避免"记忆污染自己的记忆"这种递归问题）。

---

## 与其他记忆方案的对比

| 方案 | 工作方式 | 局限性 |
|------|---------|-------|
| **CLAUDE.md** | 手动编写项目规则文件 | 需人工维护，无法自动更新 |
| **Context Window 扩展** | 用更大的上下文窗口 | Token 成本指数级增长 |
| **传统 RAG** | 检索相关文档片段 | 需要预先构建知识库，不实时 |
| **Claude-Mem** | 自动压缩 + 按需注入 | 依赖 Claude API，有处理延迟 |

Claude-Mem 的独特价值在于：它不是静态知识库，而是**动态生长的项目记忆**——随着你每次与 Claude Code 的对话自动演化。

---

## 系列导读

本文是 Claude-Mem 深度解析系列的第一篇，后续文章将深入各个组件：

- **第二篇**：Hook 生命周期系统——5 阶段钩子的精确工作机制
- **第三篇**：Worker Service——异步处理引擎与 HTTP API 全解析
- **第四篇**：数据库层——SQLite + FTS5 + ChromaDB 三层存储架构
- **第五篇**：搜索架构——MCP 工具与 3 层渐进式检索工作流
- **第六篇**：上下文工程——渐进式披露的设计哲学与最佳实践

---

*Claude-Mem 是由 Alex Newman（@thedotmack）开发的开源项目，采用 AGPL-3.0 协议，当前版本 v10.6.2，GitHub Stars 超过 41.5k。*
