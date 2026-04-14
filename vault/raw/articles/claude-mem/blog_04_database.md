# Claude-Mem 深度解析（四）：数据库层 —— SQLite + FTS5 + ChromaDB 三层存储

> **核心问题**：一个 AI 记忆系统为什么需要三种不同的存储技术？SQLite 的 FTS5 全文检索虚拟表和传统 LIKE 查询有什么本质区别？向量数据库 ChromaDB 又在哪个场景下是不可替代的？

---

## 架构哲学：为什么是三层存储？

Claude-Mem 的检索需求可以分解成三类不同的问题：

| 检索类型 | 示例查询 | 最优技术 |
|---------|---------|---------|
| **精确关键词检索** | "所有关于 JWT 的记录" | SQLite FTS5（BM25 排序）|
| **语义相似度检索** | "和认证安全相关的记录"（即使没有出现 JWT 这个词）| ChromaDB 向量检索 |
| **结构化数据查询** | "最近 7 天 bugfix 类型的记录" | SQLite 普通索引查询 |

没有哪一种技术能同时最优地解决这三类问题，因此三层存储各司其职：

```
存储层架构
├── SQLite (主库) ──────────── 结构化存储 + 关系数据
│   ├── 核心表（4张）
│   └── FTS5 虚拟表（3张）── 全文检索索引
│
└── ChromaDB (向量库) ────── 语义向量检索（可选）
    └── observations 集合 ── 每条记录的 embedding
```

---

## 核心数据模型：4 张主表

数据库文件位于 `~/.claude-mem/claude-mem.db`，使用 **WAL（Write-Ahead Logging）模式**。

### 表 1：`sdk_sessions` —— 会话注册表

```sql
CREATE TABLE sdk_sessions (
  id                    INTEGER PRIMARY KEY AUTOINCREMENT,
  sdk_session_id        TEXT UNIQUE NOT NULL,  -- 内部 UUID
  claude_session_id     TEXT,                  -- Claude Code 提供的 session_id
  project               TEXT NOT NULL,          -- 项目名（来自 cwd basename）
  prompt_counter        INTEGER DEFAULT 0,      -- 本次会话的提示词计数
  status                TEXT NOT NULL DEFAULT 'active',  -- active | completed
  created_at            TEXT NOT NULL,
  created_at_epoch      INTEGER NOT NULL,       -- Unix 毫秒时间戳（用于排序）
  completed_at          TEXT,
  completed_at_epoch    INTEGER,
  last_activity_at      TEXT,
  last_activity_epoch   INTEGER
);
```

**设计要点**：

- `sdk_session_id` 和 `claude_session_id` 是两个不同的 ID。前者是 Claude-Mem 内部生成的，后者是 Claude Code 提供的。这种解耦允许 Claude-Mem 在未来支持其他 AI 编程工具（如 Cursor）时不需要修改数据模型。
- `status` 字段采用"软完成"而非删除——会话结束时标记为 `completed`，记录永久保留。
- `created_at_epoch` 使用毫秒级 Unix 时间戳，便于高效范围查询和排序。

**索引策略**：

```sql
CREATE INDEX idx_sdk_sessions_claude_session ON sdk_sessions(claude_session_id);
CREATE INDEX idx_sdk_sessions_project        ON sdk_sessions(project);
CREATE INDEX idx_sdk_sessions_status         ON sdk_sessions(status);
CREATE INDEX idx_sdk_sessions_created_at     ON sdk_sessions(created_at_epoch DESC);
```

---

### 表 2：`observations` —— 记忆原子单元（最重要的表）

```sql
CREATE TABLE observations (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id        TEXT NOT NULL,
  sdk_session_id    TEXT NOT NULL,
  claude_session_id TEXT,
  project           TEXT NOT NULL,
  prompt_number     INTEGER,       -- 来自第几条提示词
  tool_name         TEXT NOT NULL, -- 原始工具名（Read/Bash/Write 等）
  correlation_id    TEXT,          -- 用于追溯原始工具调用

  -- AI 压缩后的结构化字段
  title             TEXT,    -- 简明标题（< 80 字）
  subtitle          TEXT,    -- 副标题
  narrative         TEXT,    -- 详细叙述（核心字段）
  text              TEXT,    -- 辅助文本
  facts             TEXT,    -- JSON 数组：关键事实列表
  concepts          TEXT,    -- JSON 数组：涉及技术概念
  type              TEXT,    -- decision|bugfix|feature|refactor|discovery|change
  files_read        TEXT,    -- JSON 数组：读取的文件路径
  files_modified    TEXT,    -- JSON 数组：修改的文件路径

  created_at        TEXT NOT NULL,
  created_at_epoch  INTEGER NOT NULL,

  FOREIGN KEY (sdk_session_id) REFERENCES sdk_sessions(sdk_session_id)
);
```

**Observation Type 枚举的设计哲学**：

```
decision    → 架构决策、设计决定（如：选择 ChromaDB 而非 Faiss）
bugfix      → 缺陷修复（如：修复了 JWT 过期时间计算错误）
feature     → 新功能实现（如：添加了 SSE 实时推送）
refactor    → 代码重构（如：将 PM2 迁移到 Bun 进程管理）
discovery   → 代码库探索发现（如：发现 config.ts 中有硬编码 API key）
change      → 通用变更（无法归入以上类别时使用）
```

这个分类系统允许用户按类型过滤记忆：`type=bugfix` 只看 bug 修复记录，`type=decision` 只看架构决策记录。

**facts 和 concepts 字段**：这两个字段存储 JSON 数组，例如：

```json
{
  "facts": [
    "FTS5 比 LIKE 查询快 10-100 倍",
    "需要通过触发器保持 FTS 索引同步",
    "content='observations' 参数启用内容表模式"
  ],
  "concepts": ["全文检索", "FTS5", "SQLite 虚拟表", "BM25 排序"]
}
```

这些字段同时被 FTS5 索引，使得"按概念检索"成为可能。

---

### 表 3：`session_summaries` —— 会话级摘要

```sql
CREATE TABLE session_summaries (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  sdk_session_id    TEXT NOT NULL,
  claude_session_id TEXT,
  project           TEXT NOT NULL,
  prompt_number     INTEGER,

  -- 结构化摘要字段（由 summary-hook 触发，Claude Agent SDK 生成）
  request           TEXT,       -- 用户的原始需求
  investigated      TEXT,       -- 探索/调研了什么
  learned           TEXT,       -- 发现了什么关键信息
  completed         TEXT,       -- 实际完成了什么
  next_steps        TEXT,       -- 建议的后续行动
  notes             TEXT,       -- 其他备注

  created_at        TEXT NOT NULL,
  created_at_epoch  INTEGER NOT NULL,

  FOREIGN KEY (sdk_session_id) REFERENCES sdk_sessions(sdk_session_id)
);
```

**与 observations 的互补关系**：

- `observations`：细粒度，记录每次工具调用的语义信息
- `session_summaries`：高层次，记录整个工作段落的叙事结构

在下一次会话的上下文注入中，两者都会被包含：先呈现最近的 summaries（宏观视角），再呈现最近的 observations（细节视角）。

---

### 表 4：`user_prompts` —— 用户提示词存档

```sql
CREATE TABLE user_prompts (
  id                INTEGER PRIMARY KEY AUTOINCREMENT,
  sdk_session_id    TEXT NOT NULL,
  claude_session_id TEXT,
  project           TEXT NOT NULL,
  prompt_number     INTEGER,
  prompt_text       TEXT NOT NULL,  -- 脱敏后的用户提示词
  created_at        TEXT NOT NULL,
  created_at_epoch  INTEGER NOT NULL,

  FOREIGN KEY (sdk_session_id) REFERENCES sdk_sessions(sdk_session_id)
);
```

v4.2.0 新增。存储用户的原始提示词（已剥离 `<private>` 标签），用于：
1. FTS5 全文检索（"搜索我之前问过的问题"）
2. 会话摘要生成的输入素材
3. Viewer UI 中的"提示词历史"视图

---

## SQLite FTS5：全文检索的核心引擎

### 为什么不用 LIKE 查询？

```sql
-- LIKE 查询（慢，无法排序相关性）
SELECT * FROM observations WHERE narrative LIKE '%JWT鉴权%';
-- 问题：全表扫描，无法利用索引，无相关性排序

-- FTS5 查询（快，BM25 相关性排序）
SELECT * FROM observations_fts WHERE observations_fts MATCH 'JWT鉴权';
-- 优势：倒排索引，子毫秒级查询，BM25 相关性排序
```

**性能差异**：在 10 万条记录下，LIKE 需要 500ms+，FTS5 通常 < 10ms。

### 三张 FTS5 虚拟表

**虚拟表**是 SQLite 的特殊机制——它看起来像普通表，但底层是倒排索引，不存储原始数据，而是存储词项到行 ID 的映射。

```sql
-- Observation 全文检索表
CREATE VIRTUAL TABLE observations_fts USING fts5(
  title,          -- 标题（权重最高）
  subtitle,       -- 副标题
  narrative,      -- 详细叙述（内容最丰富）
  text,           -- 辅助文本
  facts,          -- 关键事实（JSON 格式，FTS5 仍可检索）
  concepts,       -- 技术概念
  content='observations',     -- "内容表"模式：FTS 索引 observations 表
  content_rowid='id'          -- 行 ID 对应 observations.id
);

-- 会话摘要全文检索表
CREATE VIRTUAL TABLE session_summaries_fts USING fts5(
  request, investigated, learned, completed, next_steps, notes,
  content='session_summaries',
  content_rowid='id'
);

-- 用户提示词全文检索表
CREATE VIRTUAL TABLE user_prompts_fts USING fts5(
  prompt_text,
  content='user_prompts',
  content_rowid='id'
);
```

`content='observations'` 参数启用**内容表模式（Content Table Mode）**：FTS5 虚拟表不再自己存储文本，而是指向 `observations` 表中的原始数据，这避免了数据重复存储。

### 触发器自动同步：三时态触发

FTS5 索引通过 SQLite 触发器与主表保持同步：

```sql
-- AFTER INSERT：新记录插入主表后，同步到 FTS 索引
CREATE TRIGGER observations_ai AFTER INSERT ON observations
BEGIN
  INSERT INTO observations_fts(rowid, title, subtitle, narrative, text, facts, concepts)
  VALUES (new.id, new.title, new.subtitle, new.narrative, new.text, new.facts, new.concepts);
END;

-- AFTER UPDATE：主表记录更新后，先删除旧 FTS 条目，再插入新条目
CREATE TRIGGER observations_au AFTER UPDATE ON observations
BEGIN
  INSERT INTO observations_fts(observations_fts, rowid, title, ...)
  VALUES('delete', old.id, old.title, ...);  -- 特殊语法：删除旧索引
  INSERT INTO observations_fts(rowid, title, ...)
  VALUES(new.id, new.title, ...);             -- 插入新索引
END;

-- AFTER DELETE：主表记录删除后，同步删除 FTS 索引
CREATE TRIGGER observations_ad AFTER DELETE ON observations
BEGIN
  INSERT INTO observations_fts(observations_fts, rowid, title, ...)
  VALUES('delete', old.id, old.title, ...);
END;
```

每张主表（observations、session_summaries、user_prompts）都有对应的三个触发器（AI/AU/AD），共 9 个触发器。

### FTS5 查询语法与安全性

FTS5 支持丰富的查询语法：

```sql
-- 简单词项搜索
SELECT * FROM observations_fts WHERE observations_fts MATCH 'authentication';

-- 短语搜索（精确匹配）
SELECT * FROM observations_fts WHERE observations_fts MATCH '"JWT token"';

-- 布尔运算
SELECT * FROM observations_fts WHERE observations_fts MATCH 'bug AND fix NOT feature';

-- 列限定搜索（只在 title 中搜索）
SELECT * FROM observations_fts WHERE observations_fts MATCH 'title:auth';

-- BM25 相关性排序
SELECT *, rank FROM observations_fts WHERE observations_fts MATCH 'auth' ORDER BY rank;
```

**SQL 注入防护**：

```typescript
function escapeFTS5Query(query: string): string {
  // FTS5 中双引号需要转义（双写）
  return query.replace(/"/g, '""')
}

// 使用示例
const safeQuery = escapeFTS5Query(userInput)
db.query(`SELECT * FROM observations_fts WHERE observations_fts MATCH ?`, [safeQuery])
```

测试套件包含 **332 个注入攻击测试用例**，覆盖各种特殊字符、SQL 关键词和引号组合。

---

## SessionStore 与 SessionSearch：数据访问层

### SessionStore —— CRUD 操作层

```typescript
// src/services/sqlite/SessionStore.ts

class SessionStore {
  // 幂等创建会话（INSERT OR IGNORE）
  createSDKSession(claudeSessionId: string, project: string, firstPrompt: string): number

  // 获取会话及其所有关联数据
  getSessionWithData(sessionId: number): SessionWithData

  // 插入 AI 压缩后的 Observation
  createObservation(obs: ObservationInput): number

  // 批量获取 Observations（用于 MCP get_observations 工具）
  getObservationsByIds(ids: number[], options?: BatchOptions): Observation[]

  // 获取用于上下文注入的最近记录
  getRecentContext(project: string, limit: number): ContextData
}
```

所有 bun:sqlite 操作使用**同步 API**（不是 async/await），这是有意为之——SQLite 的 I/O 在 WAL 模式下足够快，同步调用比异步反而更简单，避免了不必要的 Promise 开销。

### SessionSearch —— FTS5 检索层

```typescript
// src/services/sqlite/SessionSearch.ts

class SessionSearch {
  // 跨三表联合全文检索
  searchObservations(query: string, filters?: SearchFilters): SearchResult[]

  // 按概念标签检索
  findByConcept(concept: string, project?: string): Observation[]

  // 按文件路径检索
  findByFile(filePath: string, project?: string): Observation[]

  // 按类型过滤（不用 FTS，用普通索引）
  findByType(type: ObservationType, project?: string): Observation[]

  // 时间线上下文检索（用于 MCP timeline 工具）
  getTimeline(anchorId: number, depthBefore: number, depthAfter: number): TimelineResult

  // 综合高级搜索（支持所有过滤条件组合）
  advancedSearch(params: AdvancedSearchParams): SearchResult[]
}
```

---

## 数据库迁移系统

### 迁移历史（10 次迁移）

```
Migration 001: 初始 schema（sessions/memories/overviews 等遗留表）
Migration 002: 层次化字段（title/subtitle/facts/concepts/files_touched）
Migration 003: SDK sessions 和 observations 表（核心重构）
Migration 004: session_summaries 表
Migration 005: 多提示词会话支持（prompt_counter/prompt_number 字段）
Migration 006: FTS5 虚拟表 + 触发器（全文检索能力）
Migration 007: 各类改进
Migration 008: user_prompts 表
Migration 009: 性能索引优化
Migration 010: 最新 schema 修正
```

迁移系统保证了跨版本升级时数据的完整性。每次启动 Worker，都会检查当前数据库版本并应用未执行的迁移。

---

## ChromaDB：可选的语义向量层

### 何时使用 ChromaDB？

FTS5 虽然强大，但有一个根本局限：**它匹配的是词项（tokens），而不是语义（semantics）**。

```
用户查询: "认证安全问题"
FTS5 能找到: "JWT 认证"、"身份认证流程"（包含'认证'二字）
FTS5 不能找到: "CSRF 防护"、"OAuth 令牌刷新"（语义相关但没有'认证'词项）

向量检索能找到: 所有语义相关的记录，无论措辞如何
```

### ChromaDB 集成架构

```typescript
// 每条 Observation 存入 SQLite 后，同步写入 ChromaDB
async function syncToChroma(observation: Observation) {
  const collection = await chromaClient.getOrCreateCollection({
    name: `observations_${observation.project}`
  })

  await collection.add({
    ids: [String(observation.id)],
    // 使用 narrative + facts + concepts 生成 embedding
    documents: [
      `${observation.title}\n${observation.narrative}\n${observation.facts?.join('\n')}`
    ],
    metadatas: [{
      type: observation.type,
      project: observation.project,
      created_at: observation.created_at_epoch
    }]
  })
}

// 混合检索：FTS5 关键词 + ChromaDB 向量
async function hybridSearch(query: string, project: string) {
  // 层 1：FTS5 关键词检索
  const ftsResults = sessionSearch.searchObservations(query, { project })

  // 层 2：ChromaDB 语义检索
  const vectorResults = await chromaCollection.query({
    queryTexts: [query],
    nResults: 10,
    where: { project }
  })

  // 融合排序（Reciprocal Rank Fusion）
  return mergeAndRerank(ftsResults, vectorResults)
}
```

ChromaDB 是**可选的**——如果用户不安装 uv（Python 包管理器），系统会退回到纯 FTS5 模式，大多数使用场景下效果依然良好。

---

## 性能优化汇总

| 优化手段 | 解决的问题 | 效果 |
|---------|-----------|------|
| WAL 模式 | 读写并发冲突 | 读不阻塞写，Viewer UI 实时刷新不影响数据写入 |
| FTS5 倒排索引 | 全表扫描慢 | 查询时间从 500ms 降至 < 10ms |
| 触发器自动同步 | 手动维护 FTS 索引的复杂性 | 完全透明，对应用层无感 |
| created_at_epoch 时间戳索引 | 时间范围查询 | `ORDER BY created_at_epoch DESC` 利用索引 |
| 批量 IDs 查询 | 多次 HTTP 往返 | 一次 POST 获取多条完整详情 |
| bun:sqlite 同步 API | async/await Promise 开销 | SQLite 场景无需异步，同步 API 更简洁 |

---

## 数据演化轨迹：从 v3 到现在

Claude-Mem 经历了三代数据模型：

**v3 时代（遗留）**：`sessions` → `memories` → `overviews`
- 粗粒度的"记忆块"概念，一个 memory 可能包含多次工具调用
- 没有 FTS5，只能用 LIKE 查询
- 没有 ChromaDB，纯关键词检索

**v4 时代（当前主线）**：`sdk_sessions` → `observations` → `session_summaries` → `user_prompts`
- 细粒度的 observation 单元，每条工具调用独立一条记录
- FTS5 全文检索 + 触发器自动同步
- ChromaDB 可选语义向量检索

遗留的 `sessions`/`memories`/`overviews` 表至今仍保留在 schema 中（但不再使用），这是向后兼容的考量——避免老用户升级时数据丢失。

---

## 小结

Claude-Mem 的数据库层体现了"用最简单的工具解决问题"的工程哲学：

- **不用 PostgreSQL**，因为 SQLite 的 WAL 模式在单机并发场景完全够用
- **不用 Elasticsearch**，因为 FTS5 的性能对本地开发场景已经足够
- **不强制 ChromaDB**，因为大多数用户不需要语义检索，可选安装降低门槛

三层存储的组合，在零外部基础设施依赖的前提下，提供了从毫秒级精确检索到语义模糊检索的完整检索能力谱系。

下一篇将深入 MCP 工具和 3 层渐进式检索工作流，这是用户与记忆交互的顶层界面。
