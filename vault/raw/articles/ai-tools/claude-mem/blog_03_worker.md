# Claude-Mem 深度解析（三）：Worker Service —— 异步处理引擎

> **核心问题**：为什么 Claude-Mem 需要一个独立的后台服务进程？22 个 HTTP 端点分别承担哪些职责？Claude Agent SDK 又是如何将原始工具日志变成有意义的"记忆"的？

---

## 为什么需要独立的 Worker？

这是理解 Claude-Mem 架构的第一个关键问题。

**直接在 Hook 脚本中调用 Claude API** 行不行？理论上可以，但会有三个致命问题：

1. **超时风险**：Claude Code 给 Hook 脚本的超时是 120 秒，AI 处理+网络延迟可能轻松超时
2. **阻塞体验**：每次工具调用都要等 AI 处理完毕，用户感受到明显卡顿
3. **状态管理困难**：同一会话的多个工具调用需要共享状态，但多个独立的 Hook 进程无法共享内存

**Worker Service 解决了这三个问题**：
- Hook 脚本只做数据传递（HTTP POST，2 秒超时），不做 AI 处理
- Worker 在独立进程中异步处理，不阻塞用户
- Worker 是长驻进程，天然共享内存状态

---

## Worker Service 全貌

```
Worker Service (port 37777)
├── Express.js HTTP Server
│   ├── Viewer & Health 端点（4个）
│   ├── Data Retrieval 端点（7个）
│   ├── Settings 端点（2个）
│   ├── Queue Management 端点（2个）
│   └── Session Management 端点（5个）
│
├── Claude Agent SDK 处理引擎
│   ├── SDKAgent（AI 处理核心）
│   ├── SessionManager（会话状态协调）
│   └── 事件驱动队列（零延迟通知）
│
├── SSE 实时推送系统
│   └── 向 Viewer UI 广播新增的 observations/summaries
│
└── SQLite Database
    ├── bun:sqlite 驱动（高性能）
    ├── SessionStore（CRUD 操作层）
    └── SessionSearch（FTS5 全文检索）
```

---

## 进程管理：从 PM2 到 Bun Native

### 早期架构（v3）

Claude-Mem 最初使用 **PM2**（Node.js 生态最流行的进程管理工具）来管理 Worker 进程。这带来了依赖问题——用户需要全局安装 PM2，且 PM2 本身也是一个相当重量级的工具。

### 当前架构（v4+）

现在使用 **Bun 原生进程管理**，通过 `ProcessManager` 类实现：

```typescript
class ProcessManager {
  private pidFile = path.join(HOME_DIR, '.claude-mem/worker.pid')

  async start() {
    // 用 Bun 启动 Worker 进程
    const proc = Bun.spawn(['bun', workerServicePath], {
      stdout: 'pipe',
      stderr: 'pipe',
      detached: true  // 独立于父进程运行
    })
    
    // 记录 PID（用于后续管理）
    fs.writeFileSync(this.pidFile, String(proc.pid))
    
    // 等待健康就绪
    await this.waitForHealth()
  }

  async stop() {
    const pid = parseInt(fs.readFileSync(this.pidFile, 'utf-8'))
    process.kill(pid, 'SIGTERM')
    
    // 给 5 秒优雅关闭窗口，超时后强制 SIGKILL
    await sleep(5000)
    try { process.kill(pid, 'SIGKILL') } catch {}
  }
}
```

Bun 的优势：
- **内置 SQLite**：`bun:sqlite` 比 `better-sqlite3` 快 3~5 倍
- **零额外依赖**：不需要全局安装任何额外工具
- **快速启动**：冷启动时间明显低于 Node.js + PM2 组合

---

## 22 个 HTTP 端点详解

### 分类一：Viewer & Health（基础设施端点）

#### `GET /` - Viewer UI
返回自包含的 React Web 界面（`viewer.html`，用 esbuild 打包）。
用户访问 `http://localhost:37777` 即可看到实时记忆流。

#### `GET /health` - 健康检查
```json
{ "status": "ok", "uptime": 12345, "port": 37777 }
```
Context Hook 启动时会轮询这个端点，确认 Worker 就绪。

#### `GET /stream` - Server-Sent Events
Worker 通过 SSE 向 Viewer UI 推送三类实时事件：
```
event: observation-created
data: {"id": 123, "title": "Fix auth token expiry", "type": "bugfix"}

event: session-summary-created  
data: {"id": 456, "request": "Optimize RAG pipeline..."}

event: user-prompt-created
data: {"id": 789, "prompt": "How do I improve recall?"}
```

---

### 分类二：Data Retrieval（数据读取端点）

这是 Viewer UI 和 MCP 搜索工具的数据来源。

#### `GET /api/observations` - 分页读取 Observations

```http
GET /api/observations?project=taptap-maker&limit=20&offset=0
```

响应：
```json
{
  "observations": [{
    "id": 123,
    "title": "优化 LangGraph 状态机节点",
    "type": "refactor",
    "narrative": "将原有的线性 Chain 改为并行 Branch 节点...",
    "created_at": "2025-03-28T14:30:00Z"
  }],
  "total": 847,
  "hasMore": true
}
```

#### `POST /api/observations/batch` - 批量读取（MCP 核心端点）

```json
{
  "ids": [123, 456, 789],
  "orderBy": "date_desc",
  "project": "taptap-maker"
}
```

这个端点是 `get_observations` MCP 工具的后端，允许一次请求获取多个完整的 observation 详情，避免多次 HTTP 往返。

#### `GET /api/search` - FTS5 全文检索

```http
GET /api/search?query=JWT鉴权&type=bugfix&limit=10
```

核心 SQL（简化版）：
```sql
SELECT o.*, rank
FROM observations_fts fts
JOIN observations o ON o.id = fts.rowid
WHERE fts MATCH ?          -- FTS5 全文检索
  AND o.type = ?           -- 类型过滤
  AND o.project = ?        -- 项目过滤
ORDER BY rank              -- BM25 相关性排序
LIMIT ? OFFSET ?
```

---

### 分类三：Queue Management（队列管理端点）

#### `GET /api/pending-queue` - 队列状态诊断

```json
{
  "queue": {
    "totalPending": 5,
    "totalProcessing": 2,
    "totalFailed": 0,
    "stuckCount": 1
  }
}
```

`stuckCount` 表示处于 `processing` 状态超过 5 分钟的"卡住"任务数量——这通常意味着 SDK Agent 崩溃了。

#### `POST /api/pending-queue/process` - 手动触发恢复

**重要设计决策**：v5.x 起，Worker 启动时**不再自动**重处理积压队列。需要用户显式触发：

```bash
curl -X POST http://localhost:37777/api/pending-queue/process \
  -d '{"sessionLimit": 10}'
```

这是刻意为之的设计——避免 Worker 频繁重启时产生大量重复的 AI 处理请求（每次处理都消耗 Claude API Token）。

---

### 分类四：Session Management（会话管理端点）

这五个端点专门供 Hook 脚本调用：

| 端点 | Hook | 职责 |
|------|------|------|
| `POST /sessions/:id/init` | new-hook | 初始化会话，设置项目/提示词 |
| `POST /api/sessions/observations` | save-hook | 接收工具调用数据，加入处理队列 |
| `POST /api/sessions/summarize` | summary-hook | 触发会话摘要生成 |
| `GET /sessions/:id/status` | 诊断用 | 查询会话当前状态 |
| `POST /api/sessions/complete` | cleanup-hook | 标记会话完成 |

---

## Claude Agent SDK 处理引擎

这是 Worker Service 最核心的部分——将原始工具日志变成有意义记忆的 AI 引擎。

### SDKAgent 的工作原理

```typescript
class SDKAgent {
  async startSession(session: ActiveSession) {
    // 创建事件驱动的消息生成器
    const messageGenerator = this.createMessageGenerator(session)
    
    // 启动 Claude Agent SDK 查询循环
    const queryResult = query({
      prompt: messageGenerator,
      options: {
        model: 'claude-sonnet-4-5',
        // 关键：SDK Agent 只能"观察"，不能执行工具
        disallowedTools: ['Bash', 'Read', 'Write', 'Edit', 'Grep'],
        abortController: session.abortController
      }
    })
    
    // 处理 AI 响应流
    for await (const message of queryResult) {
      if (message.type === 'assistant') {
        await this.processSDKResponse(session, message.content)
      }
    }
  }
}
```

### 消息类型与提示词结构

SDK Agent 接收四种类型的消息：

**1. 初始化提示词（第一条消息）**

包含完整的系统指令，告知 AI 它的任务：
```xml
<system>
你是一个代码会话记忆提取助手。你的工作是将原始的工具调用数据
压缩成结构化的"观察记录"（Observations）。

每个 Observation 应当包含：
- title: 简明标题（不超过 80 字）
- type: feature|bugfix|refactor|research|config|test|docs
- narrative: 详细叙述（技术决策、上下文、影响）
- facts: 关键事实列表
- files: 涉及的文件路径
- concepts: 涉及的技术概念
</system>
```

**2. 工具调用数据（Observation 消息）**

```xml
<tool_use>
  <tool_name>Read</tool_name>
  <tool_input>{"file_path": "/src/retrieval/rag_pipeline.py"}</tool_input>
  <tool_response>
    import faiss
    import numpy as np
    
    class RAGPipeline:
      def __init__(self, embedding_dim=1536):
        self.index = faiss.IndexFlatL2(embedding_dim)
        ...
  </tool_response>
</tool_use>
```

**3. AI 响应解析**

SDK Agent 的输出是结构化 XML：
```xml
<observation>
  <title>读取 RAG 检索管道源码，分析 Faiss 索引配置</title>
  <type>research</type>
  <narrative>
    检查了 RAGPipeline 类的实现。当前使用 IndexFlatL2（暴力搜索），
    对于大型向量集合效率较低。embedding_dim=1536 表明使用 OpenAI 
    text-embedding-ada-002 模型。建议切换到 IndexHNSWFlat 以提升
    检索性能（近似最近邻搜索）。
  </narrative>
  <facts>
    <fact>使用 Faiss IndexFlatL2 进行精确搜索</fact>
    <fact>向量维度 1536，对应 OpenAI ada-002 模型</fact>
    <fact>暴力搜索在百万级别向量时性能不足</fact>
  </facts>
  <files>
    <file>/src/retrieval/rag_pipeline.py</file>
  </files>
  <concepts>
    <concept>向量索引</concept>
    <concept>近似最近邻搜索</concept>
    <concept>Faiss</concept>
  </concepts>
</observation>
```

### 模型配置

Worker 使用的模型通过环境变量配置：
```bash
export CLAUDE_MEM_MODEL=sonnet  # 默认，平衡速度与质量
export CLAUDE_MEM_MODEL=haiku   # 更快更便宜
export CLAUDE_MEM_MODEL=opus    # 最高质量
```

---

## 事件驱动队列：零延迟处理

Worker 内部使用**事件发射器（EventEmitter）**而非轮询机制：

```typescript
// Hook 提交数据时，队列立即发出通知
class ObservationQueue extends EventEmitter {
  async add(observation: RawObservation) {
    this.pending.push(observation)
    this.emit('new-observation')  // 立即通知处理器
  }
}

// 处理器监听事件，立即响应
queue.on('new-observation', async () => {
  const obs = queue.pending.shift()
  await sdkAgent.process(obs)
})
```

这比定时轮询（每隔 N 秒检查一次队列）有更低的延迟：工具调用发生后，记忆压缩几乎立即开始，而不是等到下一个轮询周期。

---

## 数据存储路径

Worker 将所有持久化数据存放在 `~/.claude-mem/` 目录：

```
~/.claude-mem/
├── claude-mem.db        # SQLite 主数据库
├── worker.pid           # Worker 进程 PID
├── settings.json        # 用户配置（UI 偏好、项目过滤等）
└── logs/
    ├── worker-2025-03-28.log  # 按日期轮转的日志
    └── worker-2025-03-29.log
```

SQLite 数据库使用 **WAL（Write-Ahead Logging）模式**，允许并发读取（Viewer UI 查询）不阻塞写入（Observation 插入）。

---

## 错误处理与优雅降级

Worker 实现了多层错误处理：

```typescript
// 数据库错误：记录日志，不崩溃
try {
  db.insertObservation(obs)
} catch (dbError) {
  logger.error('DB insert failed', dbError)
  // 不 rethrow，Worker 继续运行
}

// SDK 错误：指数退避重试（最多 3 次）
for (let attempt = 1; attempt <= 3; attempt++) {
  try {
    await sdkAgent.process(obs)
    break
  } catch (sdkError) {
    if (attempt === 3) {
      obs.status = 'failed'  // 标记失败，不丢弃数据
    } else {
      await sleep(1000 * Math.pow(2, attempt))  // 2s, 4s
    }
  }
}

// 网络错误：记录并跳过（不影响其他请求）
app.use((error, req, res, next) => {
  logger.error('HTTP error', error)
  res.status(500).json({ error: 'Internal server error' })
})
```

---

## Viewer UI：记忆可视化

Worker 同时提供了一个 React Web 界面，访问 `http://localhost:37777` 即可看到：

- **实时记忆流**：通过 SSE 自动更新，无需刷新页面
- **无限滚动**：自动分页加载历史 observations
- **项目过滤**：按项目名过滤，只看当前工程的记忆
- **暗色/亮色主题**：v5.1.2 新增
- **队列状态**：Settings 面板显示当前处理队列状态

这个界面的价值在于**透明度**——用户可以实时看到 Claude-Mem 正在记录什么，理解哪些信息被保留到了记忆中，从而更好地与系统协作。

---

## 性能特性

| 特性 | 实现方式 | 效果 |
|------|---------|------|
| 异步处理 | 事件驱动队列 | Hook 响应时间 < 10ms |
| 并发读写 | SQLite WAL 模式 | 读不阻塞写 |
| 批量获取 | POST /api/observations/batch | 一次请求获取多条详情 |
| FTS5 全文检索 | SQLite 内置虚拟表 | 典型查询 < 10ms |

---

## 小结

Worker Service 是 Claude-Mem 的处理核心，承担了三项关键职责：

1. **解耦**：将耗时的 AI 处理从 Hook 脚本中剥离，保证用户体验流畅
2. **AI 压缩**：通过 Claude Agent SDK 将原始工具日志提炼成语义丰富的结构化记忆
3. **服务化**：通过 22 个 HTTP 端点，为 Viewer UI、MCP 工具、Hook 脚本提供统一的数据访问接口

下一篇将深入数据库层，看 SQLite + FTS5 + ChromaDB 三层存储架构如何协同工作。
