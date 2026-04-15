# Claude-Mem 深度解析（五）：搜索架构 —— MCP 工具与 3 层渐进式检索

> **核心问题**：传统 RAG 系统往往一次性加载大量上下文，但这对 LLM 来说既昂贵又低效。Claude-Mem 如何用 4 个 MCP 工具和 3 层工作流实现 10 倍 Token 节省？

---

## 问题的起点：Token 是有代价的

在 LLM 应用中，上下文窗口是最稀缺的资源。一条 observation 的完整详情约 500~1,000 tokens；如果每次检索都无差别地加载 20 条记录，仅上下文就要消耗 10,000~20,000 tokens。

更糟糕的是：在这 20 条记录中，真正相关的往往只有 2~3 条。其余 17 条不仅浪费 Token 预算，还会给 LLM 带来"注意力稀释"问题，降低有效推理的质量。

Claude-Mem 的搜索架构从一个简单的原则出发：**先知道有什么，再决定要看什么**。

---

## 架构演化：从 9 工具到 4 工具

### v5.x 时代（已废弃）：9 个 MCP 工具

早期版本提供了 9 个功能高度重叠的 MCP 工具：

```
search_observations   → 全文检索 observations
find_by_type         → 按类型过滤
find_by_file         → 按文件过滤
find_by_concept      → 按概念过滤
get_recent_context   → 最近会话
get_observation      → 获取单条详情
get_session          → 获取会话详情
get_prompt           → 获取提示词
help                 → API 文档
```

问题：
- **操作重叠**：`search_observations` 和 `find_by_type` 能力高度重合
- **Token 开销大**：9 个工具的定义描述本身就需要 ~2,500 tokens
- **无工作流引导**：Claude 不知道应该以什么顺序使用这些工具
- **代码量膨胀**：mcp-server.ts 超过 2,718 行

### 当前架构：4 个 MCP 工具

```
__IMPORTANT      → 工作流说明（永远可见的指导文档）
search           → 第 1 层：获取紧凑索引
timeline         → 第 2 层：获取时间线上下文
get_observations → 第 3 层：获取选定记录的完整详情
```

代码从 2,718 行压缩到 312 行（减少 88%），同时工具定义的 Token 开销大幅降低。

---

## 4 个 MCP 工具详解

### 工具 0：`__IMPORTANT` —— 始终可见的工作流文档

这个工具名称以双下划线开头，是一个特殊设计——它排在工具列表的最前面，确保 Claude 总是首先看到工作流说明。

```typescript
{
  name: '__IMPORTANT',
  description: `
3-LAYER WORKFLOW (ALWAYS FOLLOW):
1. search(query) → Get index with IDs (~50-100 tokens/result)
2. timeline(anchor=ID) → Get context around interesting results
3. get_observations([IDs]) → Fetch full details ONLY for filtered IDs

NEVER fetch full details without filtering first. 10x token savings.
  `
}
```

这个工具本身不做任何 HTTP 请求，它只是一段永远显示在 Claude 工具列表顶部的说明文字，作为**强制性的工作流约束**。

这是一个巧妙的"提示词工程即架构"的设计案例：把工作流规范编码进工具定义，而不是依赖 Claude 自行记忆。

---

### 工具 1：`search` —— 第 1 层，紧凑索引

```typescript
{
  name: 'search',
  description: 'Step 1: Search memory. Returns index with IDs. ' +
    'Params: query, limit, project, type, obs_type, dateStart, dateEnd, offset, orderBy',
  inputSchema: {
    type: 'object',
    properties: {},
    additionalProperties: true  // 接受任意参数，不做模式校验
  }
}
```

**后端实现**：

```http
GET /api/search?query=JWT认证&type=bugfix&project=taptap&limit=10
```

**返回格式**（紧凑的 Markdown 表格）：

```markdown
| ID   | 时间     | 标题                    | 类型    |
|------|----------|-------------------------|---------|
| #247 | 3:25 PM  | 修复 JWT 过期验证逻辑    | bugfix  |
| #198 | 昨天     | 添加 token 刷新端点      | feature |
| #156 | 2天前    | 研究 OAuth 2.0 最佳实践  | research|
```

**Token 成本**：每条结果约 50~100 tokens（而非完整详情的 500~1,000 tokens）。

**背后的 FTS5 查询**：

```sql
SELECT o.id, o.title, o.type, o.created_at, rank
FROM observations_fts fts
JOIN observations o ON o.id = fts.rowid
WHERE fts MATCH 'JWT认证'   -- FTS5 全文匹配
  AND o.type = 'bugfix'     -- 类型过滤（普通索引）
  AND o.project = 'taptap'  -- 项目过滤（普通索引）
ORDER BY rank               -- BM25 相关性排序
LIMIT 10 OFFSET 0;
```

---

### 工具 2：`timeline` —— 第 2 层，时间线上下文

```typescript
{
  name: 'timeline',
  description: 'Step 2: Get context around results. ' +
    'Params: anchor (observation ID) OR query (finds anchor automatically), ' +
    'depth_before, depth_after, project'
}
```

**典型使用场景**：

Claude 在 Step 1 的搜索结果里看到了 `#247 修复 JWT 过期验证逻辑`，想了解这个 bug 修复前后发生了什么：

```
timeline(anchor=247, depth_before=3, depth_after=3)
```

**返回格式**（时间线视图）：

```markdown
## 时间线 (围绕 #247)

📅 之前
  #244 [research] 研究 JWT 规范文档 (3:10 PM)
  #245 [discovery] 发现 payload 中 exp 字段格式不一致 (3:18 PM)
  #246 [refactor] 提取 TokenValidator 工具类 (3:22 PM)

⭐ 锚点
  #247 [bugfix] 修复 JWT 过期验证逻辑 (3:25 PM)

📅 之后
  #248 [test] 添加 JWT 边界条件测试用例 (3:31 PM)
  #249 [feature] 添加刷新 token 自动续期 (3:45 PM)
  #250 [docs] 更新 API 鉴权文档 (4:02 PM)
```

这个视图的价值在于**叙事连贯性**——用户不仅能看到这个 bug 是怎么被修复的，还能看到修复前的探索过程（#244-246）和修复后的配套工作（#248-250）。

**后端 SQL**（简化）：

```sql
-- 找出时间锚点前的 N 条记录
SELECT * FROM observations
WHERE project = ?
  AND created_at_epoch < (SELECT created_at_epoch FROM observations WHERE id = ?)
ORDER BY created_at_epoch DESC
LIMIT ?;

-- 找出时间锚点后的 N 条记录
SELECT * FROM observations
WHERE project = ?
  AND created_at_epoch > (SELECT created_at_epoch FROM observations WHERE id = ?)
ORDER BY created_at_epoch ASC
LIMIT ?;
```

---

### 工具 3：`get_observations` —— 第 3 层，完整详情

```typescript
{
  name: 'get_observations',
  description: 'Step 3: Fetch full details for filtered IDs. ' +
    'Params: ids (array of observation IDs, required), orderBy, limit, project',
  inputSchema: {
    type: 'object',
    properties: {
      ids: {
        type: 'array',
        items: { type: 'number' },
        description: 'Array of observation IDs to fetch (required)'
      }
    },
    required: ['ids'],
    additionalProperties: true
  }
}
```

**只有 `ids` 是必填参数**，这是有意设计——强迫用户（Claude）必须先从前两层获取 ID，才能在第三层获取详情。

**后端实现**：`POST /api/observations/batch`

```json
{
  "ids": [247, 248],
  "orderBy": "date_desc"
}
```

**返回格式**（完整 Markdown 详情）：

```markdown
## Observation #247
**标题**: 修复 JWT 过期验证逻辑
**类型**: bugfix
**时间**: 2025-03-28 15:25:00
**项目**: taptap-maker

**详细叙述**:
发现 JWT 验证中 `exp` 字段的对比使用了毫秒时间戳，而 JWT 标准
规定 `exp` 是秒级 Unix 时间戳。修复方式：将服务端当前时间除以 1000
后再与 exp 对比。此 bug 导致所有 token 在签发后即刻失效。

**关键事实**:
- JWT exp 字段为秒级 Unix 时间戳（非毫秒）
- 错误代码：`Date.now() > payload.exp`
- 正确代码：`Math.floor(Date.now() / 1000) > payload.exp`

**涉及文件**:
- /src/auth/jwt-validator.ts
- /tests/auth/jwt-validator.test.ts

**涉及概念**:
- JWT 标准, Unix 时间戳, 鉴权
```

**Token 成本**：每条完整详情约 500~1,000 tokens。

---

## 3 层工作流的 Token 节省计算

### 传统 RAG 方式

```
场景：搜索"JWT 鉴权问题"，数据库中有 20 条相关记录

传统 RAG：全部加载
→ 20 条 × 750 tokens/条 = 15,000 tokens
→ 实际有用的：2~3 条（~10% 相关性）
→ 浪费：13,500 tokens
```

### 3 层工作流方式

```
Step 1: search(query="JWT鉴权", limit=20)
→ 20 条 × 75 tokens/条 = 1,500 tokens
→ Claude 审阅索引，识别出 3 条真正相关的（#247, #248, #198）

Step 2: timeline(anchor=247, depth_before=2, depth_after=2)
→ ~500 tokens（了解上下文）

Step 3: get_observations(ids=[247, 248, 198])
→ 3 条 × 750 tokens/条 = 2,250 tokens

总计：1,500 + 500 + 2,250 = 4,250 tokens
节省：15,000 - 4,250 = 10,750 tokens (72% 节省)
相关性：100%（Claude 主动选择了哪些值得深入）
```

---

## MCP Server：薄薄的协议翻译层

MCP Server 的核心价值是**协议翻译**——将 MCP 协议（JSON-RPC over stdio）转换为 HTTP API 调用。

```typescript
// plugin/scripts/mcp-server.cjs（只有 312 行！）

// 通用 Handler 工厂：接受任意参数，转发给 HTTP API
function makeHandler(endpoint: string) {
  return async (args: Record<string, any>) => {
    const url = new URL(`http://localhost:37777${endpoint}`)

    for (const [key, value] of Object.entries(args)) {
      url.searchParams.append(key, String(value))
    }

    const response = await fetch(url.toString())
    const data = await response.json()
    return { content: [{ type: 'text', text: JSON.stringify(data) }] }
  }
}

// 注册工具
const tools = [
  { name: 'search',           handler: makeHandler('/api/search') },
  { name: 'timeline',         handler: makeHandler('/api/timeline') },
  { name: 'get_observations', handler: makePostHandler('/api/observations/batch') },
]
```

`additionalProperties: true` 的 Schema 设计允许 Handler 将任意参数透传给 HTTP API，无需在 MCP Server 层做参数解析，进一步简化代码。

**架构清晰度**：
```
Claude → MCP Protocol (JSON-RPC) → MCP Server → HTTP API → Worker → SQLite
```
每一层只做一件事，没有业务逻辑泄漏。

---

## 搜索能力矩阵

| 能力 | 后端技术 | 工具 | 示例查询 |
|------|---------|------|---------|
| 全文关键词检索 | FTS5 BM25 | `search` | `query="认证"` |
| 类型过滤 | SQLite 普通索引 | `search` | `type="bugfix"` |
| 项目过滤 | SQLite 普通索引 | `search` | `project="taptap"` |
| 时间范围过滤 | SQLite 时间戳索引 | `search` | `dateStart="2025-03-01"` |
| 时间线上下文 | SQLite 时间排序 | `timeline` | `anchor=247` |
| 语义向量检索 | ChromaDB | `search`（混合） | 语义模糊查询 |
| 批量精确获取 | SQLite 主键查询 | `get_observations` | `ids=[1,2,3]` |

---

## FTS5 注入防护（安全细节）

在搜索系统中，FTS5 查询注入是一个真实存在的安全威胁：

```
# 恶意输入示例
query = '"; DROP TABLE observations; --'
query = 'bug" OR "1"="1'
```

FTS5 的防护方式与 SQL 参数化查询不同——FTS5 查询是作为字符串值传入的，但其内部仍有一套解析语法需要转义：

```typescript
function escapeFTS5Query(query: string): string {
  // FTS5 中，双引号用于短语搜索，需要双写转义
  return query.replace(/"/g, '""')
}

// 使用 prepared statement 传入转义后的查询
const stmt = db.prepare(
  `SELECT * FROM observations_fts WHERE observations_fts MATCH ?`
)
const results = stmt.all(escapeFTS5Query(userQuery))
```

测试覆盖 332 种注入模式，包括：
- SQL 关键词注入（DROP/SELECT/INSERT）
- FTS5 特殊字符（双引号、布尔操作符）
- Unicode 特殊字符
- 超长查询字符串
- 空查询边界条件

---

## Claude Desktop vs Claude Code：同一套 MCP

Claude-Mem 的 MCP 架构同时支持两个 Anthropic 客户端：

```json
// Claude Desktop 配置（~/.config/claude/claude_desktop_config.json）
{
  "mcpServers": {
    "mcp-search": {
      "command": "node",
      "args": ["/Users/YOU/.claude/plugins/.../plugin/scripts/mcp-server.cjs"]
    }
  }
}
```

```
// Claude Code（通过 plugin install 自动配置，无需手动修改）
```

两个客户端使用**同一个 MCP Server**，查询**同一个 SQLite 数据库**，这意味着你在 Claude Code 里积累的编程记忆，可以直接在 Claude Desktop 的对话中用 `search` 工具检索。

---

## 架构演化的关键洞察

从 9 工具到 4 工具的重构，背后有一个深刻的设计洞察：

**v5.x（旧）**：渐进式披露是 Claude 需要**记住**的行为规范
> "Claude 啊，你应该先搜索，再获取详情……"

**v6+（新）**：渐进式披露被**编码进工具设计本身**
> 工具的排列顺序、`__IMPORTANT` 的位置、`get_observations` 强制要求 `ids`——这些结构性约束让 Claude 想不按工作流来都难

这体现了系统设计的一个高级原则：**让正确的事情变得容易，让错误的事情变得困难**，而不是依赖用户（或 AI）的记忆和自律。

---

## 小结

Claude-Mem 的搜索架构在四个维度上都达到了最优：

- **Token 效率**：3 层工作流实现约 10 倍 Token 节省
- **代码简洁**：MCP Server 从 2,718 行压缩到 312 行
- **工作流约束**：`__IMPORTANT` 工具将工作流规范变成结构性约束
- **安全性**：332 个 FTS5 注入测试用例，全面覆盖边界条件

下一篇（最终篇）将讨论 Claude-Mem 的设计哲学——渐进式披露（Progressive Disclosure）和上下文工程（Context Engineering），这两个概念不仅是 Claude-Mem 的核心，也是所有 AI Agent 系统设计者应该深入理解的思维框架。
