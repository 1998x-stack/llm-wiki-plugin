# Claude-Mem 深度解析（二）：Hook 生命周期系统

> **核心问题**：Claude Code 的插件系统如何让外部程序"感知"到 AI 的每一个动作？Claude-Mem 的 6 个 Hook 脚本又是如何精密配合，构建出完整的会话记忆管道的？

---

## Hook 系统：Claude Code 的神经末梢

Claude Code 提供了一套**生命周期钩子（Lifecycle Hooks）**机制，允许插件在特定时间节点介入 AI 的工作流程。这类似于 Git 的 pre-commit / post-commit hooks，或 React 的生命周期方法。

Claude-Mem 利用 5 种生命周期事件，部署了 6 个 Hook 脚本（其中 SessionStart 阶段挂载了 3 个顺序执行的脚本）：

```json
{
  "hooks": {
    "SessionStart":       ["smart-install.js", "worker-service.cjs", "context-hook.js"],
    "UserPromptSubmit":   ["new-hook.js"],
    "PostToolUse":        ["save-hook.js"],
    "Stop":               ["summary-hook.js"],
    "SessionEnd":         ["cleanup-hook.js"]
  }
}
```

所有 Hook 通过 **stdin/stdout** 与 Claude Code 通信：
- **输入**：Claude Code 将上下文数据序列化为 JSON，写入 Hook 进程的 stdin
- **输出**：Hook 将控制指令（或注入内容）序列化为 JSON，写入 stdout

---

## 第 0 阶段：Smart Install（预检钩子）

**文件**：`scripts/smart-install.js`
**触发时机**：SessionStart 的第一个命令（非生命周期钩子，属于前置检查）

### 核心职责

在 Worker 启动之前，确保所有依赖已经安装到位：
- Node.js 版本检查（需要 ≥ 18.0.0）
- Bun 运行时（如未安装，自动调用官方安装脚本）
- uv（Python 包管理器，ChromaDB 向量数据库依赖）

### 缓存机制：避免重复检查

Smart Install 最精妙的设计是**版本缓存**。它会记录上次检查时的 claude-mem 版本号：

```javascript
// 检查缓存文件
const cacheFile = path.join(pluginRoot, '.install-cache.json')
const cache = JSON.parse(fs.readFileSync(cacheFile))

// 仅当版本变化时才重新安装
if (cache.version === currentVersion) {
  process.exit(0)  // 跳过，直接退出
}
```

这意味着依赖检查只在**插件版本升级时**才真正运行，正常使用中几乎是零开销的。

---

## 第 1 阶段：SessionStart → Context Hook

**文件**：`src/hooks/context-hook.ts`  
**触发时机**：用户打开 Claude Code、执行 `/clear` 或 `/compact` 时

### 输入数据（来自 Claude Code stdin）

```json
{
  "session_id": "claude-session-abc123",
  "cwd": "/Users/xm/projects/taptap-maker",
  "source": "startup"
}
```

### 工作流程

```
1. 等待 Worker 健康就绪（最多 10 秒，含指数退避重试）
     ↓
2. GET http://127.0.0.1:37777/api/context/inject?project=taptap-maker
     ↓
3. Worker 从 SQLite 查询最近 N 条 observations + summaries
     ↓
4. 格式化为 Markdown 上下文块
     ↓
5. 返回 additionalContext 给 Claude Code
```

### 输出格式（写入 stdout）

```json
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "## Previous Session Context\n\n### Recent Observations\n..."
  }
}
```

`additionalContext` 字段是 Claude Code v2.1.0+ 新增的特性，允许插件**静默注入**上下文，不在用户界面显示任何消息，但这些内容会出现在 Claude 的初始上下文窗口中。

### 关键设计：健康检查 + 重试

Context Hook 必须等待 Worker Service 完全就绪才能查询数据库。这个等待过程使用了指数退避策略：

```typescript
async function waitForWorker(maxWait = 10000): Promise<boolean> {
  const startTime = Date.now()
  let delay = 100  // 初始等待 100ms
  
  while (Date.now() - startTime < maxWait) {
    try {
      const res = await fetch('http://127.0.0.1:37777/health')
      if (res.ok) return true
    } catch {}
    
    await sleep(delay)
    delay = Math.min(delay * 1.5, 2000)  // 最大等待间隔 2 秒
  }
  return false
}
```

---

## 第 2 阶段：UserPromptSubmit → New Hook

**文件**：`src/hooks/new-hook.ts`  
**触发时机**：用户每次提交提示词时

### 输入数据

```json
{
  "session_id": "claude-session-abc123",
  "cwd": "/Users/xm/projects/taptap-maker",
  "prompt": "帮我优化这个 RAG 检索管道的召回率"
}
```

### 工作流程（详细）

```typescript
// Step 1: 从 cwd 提取项目名
const project = path.basename(cwd)  // → "taptap-maker"

// Step 2: 幂等创建/获取 session（INSERT OR IGNORE）
const sessionDbId = db.createSDKSession(session_id, project, prompt)
// 关键：同一 session_id 在整个对话中始终映射到同一个 sessionDbId
// 无论用户提交多少条消息，都使用同一个 session 记录

// Step 3: 递增提示词计数器
const promptNumber = db.incrementPromptCounter(sessionDbId)
// 第一条消息 → 1, 第二条消息 → 2, ...

// Step 4: 剥离隐私标签
const cleanedPrompt = stripMemoryTagsFromPrompt(prompt)
// 移除 <private>...</private>
// 移除 <claude-mem-context>...</claude-mem-context>（防止注入内容被二次存储）

// Step 5: 完全私有则跳过
if (!cleanedPrompt || cleanedPrompt.trim() === '') return

// Step 6: 保存用户提示词到数据库（用于 FTS5 全文检索）
db.saveUserPrompt(session_id, promptNumber, cleanedPrompt)

// Step 7: 通知 Worker 初始化会话
await fetch(`http://127.0.0.1:37777/sessions/${sessionDbId}/init`, {
  method: 'POST',
  body: JSON.stringify({ project, userPrompt: cleanedPrompt, promptNumber }),
  signal: AbortSignal.timeout(2000)  // 2 秒超时，即发即忘
})
```

### 幂等性设计的重要性

`INSERT OR IGNORE` 是整个系统正确性的基石。同一次对话（多轮问答）会多次触发 UserPromptSubmit，但它们应该共享同一个 session 记录：

```sql
-- 首次触发：创建新记录
INSERT OR IGNORE INTO sdk_sessions (claude_session_id, project, first_user_prompt)
VALUES ('abc123', 'my-project', 'First prompt...')
RETURNING id;  -- 返回 → 1

-- 第二次触发：IGNORE 生效，返回已有记录的 id
INSERT OR IGNORE INTO sdk_sessions (claude_session_id, project, first_user_prompt)
VALUES ('abc123', 'my-project', 'Second prompt...')
RETURNING id;  -- 同样返回 → 1
```

---

## 第 3 阶段：PostToolUse → Save Hook（核心）

**文件**：`src/hooks/save-hook.ts`  
**触发时机**：Claude 每次使用工具后（可能触发 **100+ 次**）

这是整个记忆系统的**核心数据采集点**，也是触发最频繁的 Hook。

### 输入数据

```json
{
  "session_id": "claude-session-abc123",
  "cwd": "/Users/xm/projects/taptap-maker",
  "tool_name": "Read",
  "tool_input": { "file_path": "/src/retrieval/rag_pipeline.py" },
  "tool_response": "import langchain\n...(文件内容)..."
}
```

### 工具过滤黑名单

不是所有工具调用都值得记录。以下工具被明确跳过（低价值噪声）：

```typescript
const SKIP_TOOLS = new Set([
  'ListMcpResourcesTool',  // MCP 基础设施内部调用
  'SlashCommand',          // 命令调用（/clear, /help 等）
  'Skill',                 // Skill 调用（不记录调用元数据本身）
  'TodoWrite',             // 任务管理的元操作
  'AskUserQuestion',       // 用户交互询问
])
```

### 核心处理逻辑

```typescript
// 过滤低价值工具
if (SKIP_TOOLS.has(tool_name)) return { continue: true, suppressOutput: true }

// 确保 Worker 在线
await ensureWorkerRunning()

// 发送给 Worker（即发即忘，2 秒超时）
await fetch('http://127.0.0.1:37777/api/sessions/observations', {
  method: 'POST',
  body: JSON.stringify({
    claudeSessionId: session_id,
    tool_name,
    tool_input,
    tool_response,
    cwd
  }),
  signal: AbortSignal.timeout(2000)
})
```

### Worker 侧的异步处理

Worker 收到观察数据后，进入异步处理队列：

```
原始工具数据 → 隐私标签剥离 → 放入内存队列
     ↓
SDK Agent 取出数据
     ↓  
调用 Claude (claude-sonnet) 进行 AI 压缩
     ↓
解析 XML 响应，提取结构化字段：
  - title: 这次工具调用的简明标题
  - type: feature / bugfix / refactor / research / ...
  - narrative: 详细叙述
  - facts: 关键事实列表
  - files: 涉及的文件路径
  - concepts: 涉及的技术概念
     ↓
写入 SQLite observations 表 + ChromaDB 向量索引
```

---

## 第 4 阶段：Stop → Summary Hook

**文件**：`src/hooks/summary-hook.ts`  
**触发时机**：用户停止提问、Claude 完成本轮回答时

### 独特之处：读取 transcript.jsonl

Claude Code 会将完整的对话历史保存为 JSONL 格式的 transcript 文件。Summary Hook 利用了这个文件：

```typescript
// 读取 transcript 文件
const lines = fs.readFileSync(transcript_path, 'utf-8').split('\n')

// 提取最后一条用户消息
const lastUserMsg = lines
  .filter(l => l)
  .map(l => JSON.parse(l))
  .filter(m => m.type === 'user')
  .pop()

// 提取最后一条 AI 回复（过滤 <system-reminder> 系统注入内容）
const lastAssistantMsg = lines
  .filter(l => l)
  .map(l => JSON.parse(l))
  .filter(m => m.type === 'assistant')
  .map(m => ({
    ...m,
    content: m.content.filter(c => !c.includes('<system-reminder>'))
  }))
  .pop()
```

### 摘要的结构化字段

Summary Hook 生成的摘要包含以下字段（由 Claude Agent SDK 处理后提取）：

```typescript
interface SessionSummary {
  request: string;       // 用户的原始需求
  investigated: string;  // 探索/调研了什么
  learned: string;       // 发现了什么关键信息
  completed: string;     // 实际完成了什么
  next_steps: string;    // 建议的后续行动
}
```

这个摘要是下一次会话注入上下文时的重要参考，它提供的是**高层次的叙述**，而 observations 提供的是**细粒度的工具调用记录**。

---

## 第 5 阶段：SessionEnd → Cleanup Hook

**文件**：`src/hooks/cleanup-hook.ts`  
**触发时机**：会话关闭时（`exit`、`/clear`、注销等）

### 设计演进：标记完成而非删除

早期版本（v4.0 之前）的 Cleanup Hook 会直接**删除**会话记录。这带来了一个问题：Worker 可能还没有完成对本次会话 observations 的异步压缩处理，会话就已经被标记为不存在。

v4.1.0+ 改为**标记完成（mark as completed）**：

```typescript
// 发送完成信号（即发即忘）
await fetch('http://127.0.0.1:37777/api/sessions/complete', {
  method: 'POST',
  body: JSON.stringify({
    claudeSessionId: session_id,
    reason: reason  // 'exit' | 'clear' | 'logout' | 'other'
  }),
  signal: AbortSignal.timeout(2000)
})
```

Worker 收到后：
1. 查找对应的 session 记录
2. 将 `status` 字段从 `'active'` 更新为 `'completed'`
3. 通过 SSE 广播"会话完成"事件给 Viewer UI

### `/clear` 的特殊处理

当用户执行 `/clear` 命令时，`reason` 为 `'clear'`。此时 Cleanup Hook 会**跳过** completion 标记，因为用户重置对话后通常紧接着开始新会话，Worker 需要继续处理之前积压的 observations。

---

## 会话状态机

6 个 Hook 共同维护了一个**隐式状态机**：

```
         SessionStart
              ↓
         [initializing]
              ↓ (context-hook 完成)
         [ready / context-injected]
              ↓ (UserPromptSubmit)
         [active / session-created]
              ↓ (PostToolUse × N)
         [active / collecting-observations]
              ↓ (Stop)
         [summarizing]
              ↓ (summary 生成完毕)
         [idle / waiting-for-next-prompt]
              ↓ (SessionEnd)
         [completed]
```

`session_id` 在整个状态机中是**唯一的不变量**，由 Claude Code 生成并注入到每个 Hook 的 stdin 中，Claude-Mem 严格遵守这个 ID 作为所有数据关联的主键。

---

## 隐私标签的边缘处理

隐私保护遵循**边缘处理原则**：在数据离开 Hook 进程之前就完成脱敏，而不是在 Worker 侧处理。

```typescript
// new-hook.ts: 处理用户提示词
const clean = stripMemoryTagsFromPrompt(rawPrompt)

// save-hook.ts: 处理工具调用数据
const cleanInput = stripMemoryTagsFromJson(JSON.stringify(tool_input))
const cleanResponse = stripMemoryTagsFromJson(JSON.stringify(tool_response))
```

这确保了即使 Worker 出现 bug 或日志泄露，敏感数据也不会出现在任何存储介质上。

`tag-stripping.ts` 中还有 ReDoS 防护：最多处理 100 个标签，防止恶意输入导致正则引擎指数回溯。

---

## 常见陷阱与解决方案

| 问题 | 根因 | 解决方案 |
|------|------|---------|
| Worker 未响应 | Hook 超时太短 | context-hook 有 10 秒等待窗口 |
| 同一 session 创建了多条记录 | 没有使用 `INSERT OR IGNORE` | 始终用 `session_id` 作为幂等键 |
| IDE 被阻塞 | Hook 同步等待 AI 处理 | 所有 Worker 调用使用 2 秒超时 |
| 记忆标签出现在数据库 | 在 Worker 侧剥离标签而非 Hook 侧 | 边缘处理，Hook 侧先行剥离 |

---

## 小结

Claude-Mem 的 Hook 系统是整个架构的"神经末梢"。它的设计遵循以下核心原则：

1. **session_id 是唯一真相来源**，由 IDE 生成，Claude-Mem 只读不写
2. **幂等操作**，任何 Hook 被重复调用都不产生副作用
3. **边缘脱敏**，隐私处理在最靠近数据源的地方完成
4. **即发即忘**，Hook 不阻塞用户的主工作流
5. **优雅降级**，Worker 不可用时 Hook 会记录错误但不抛出异常

下一篇，我们将深入 Worker Service 的内部，看看那 22 个 HTTP 端点和 Claude Agent SDK 如何协同工作。
