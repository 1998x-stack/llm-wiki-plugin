# 05 · CLAUDE.md & 上下文管理系统

> **CLAUDE.md 是概率性 AI 系统的"宪法"**——跨会话持久化的项目记忆与架构约束体系。

---

## 三级层级结构

```
~/.claude/CLAUDE.md          ← 全局层（优先级最低）
    · 个人代码风格偏好
    · 常用工具链配置
    · 个人编码习惯

./CLAUDE.md                  ← 项目层（团队共享，版本控制）
    · 技术栈：Python 3.11, FastAPI, Neo4j
    · 架构规则：所有 API 必须有 OpenAPI Schema
    · 禁止事项：不得直接操作 production DB
    · 架构决策记录（ADR）

./src/api/CLAUDE.md          ← 子目录层（优先级最高，覆盖上层）
    · 此目录所有端点必须包含速率限制
    · 响应格式必须符合 RFC 7807
```

## 正确 vs 错误的写法

### 错误：行为建议（概率性）
```markdown
- 尽量写测试
- 代码风格保持一致
- 提交前记得 Lint
```
这类指令会在第 47 次会话、上下文耗尽时被忽略。

### 正确：架构约束（结合 Hooks 实现确定性）
```markdown
# 项目技术宪法

## 硬性约束（通过 Hook 强制执行）
- 所有 Python 文件必须通过 `ruff check` + `mypy --strict`
- 禁止直接 `import *`
- 数据库变更必须通过 Alembic migration，禁止直接 DDL

## 架构决策记录（ADR）
- ADR-001: 选用 LangGraph 而非 Celery，原因：需要流式状态机支持
- ADR-002: 向量存储 Milvus + text-embedding-v3

## 上下文
- 核心链路：用户提问 → Neo4j N-hop 检索 → Rerank → SSE 流式输出

## Compact Instructions
When compacting, always preserve:
- All API endpoint signatures
- Database schema changes
- Any TODO comments marked with [CRITICAL]
```

## 自动上下文压缩（Compressor wU2）

```
上下文窗口 → 92% 阈值 → 触发 Compressor wU2

压缩策略（优先级从高到低清除）：
  1. 旧的工具调用输出（体积大，可重新获取）
  2. 早期对话历史（总结保留）
  3. 始终保留：用户显式请求 + 关键代码片段
  4. CLAUDE.md 规则：跨会话持久，不受压缩影响

手动控制：
  /compact focus on the API changes    ← 保留 API 相关内容
  /compact                             ← 默认压缩策略
  /context                             ← 查看当前 Token 占用
```

## Skills 按需加载机制

```
会话启动 → 加载所有 Skill 描述（轻量）
          → Claude 识别需要哪个 Skill
          → 按需加载完整 Skill 内容
          → Skill 用完可从上下文卸载

效果：即使配置了大量 Skills，上下文开销始终最小
```

## 三层记忆架构（生产最佳实践）

```
层 1：CLAUDE.md（稳定规则，每月变化）
    → 架构约束 · 技术栈声明 · 禁止事项

层 2：记忆文件（累积上下文，每周变化）
    → 已尝试方案 + 失败记录
    → 调试决策记录
    → 重要发现备忘

层 3：Skills（复用指令集，按需演化）
    → 调试模式：先做根因分析，再修复
    → 代码审查模式：重点检查安全漏洞

注意：记忆会过时。定期审查，
删除已完成项目的"当前优先级"引用（常见陷阱）。
```

---

# 06 · 配置 & 权限系统（Configuration & Permissions）

> 多层级配置层级 + 细粒度权限白名单，在"零人工审批"和"完全用户控制"之间取得最优平衡。

---

## 配置文件 4 级层级

```
优先级最低
    │
    ▼
1. 企业策略层（Enterprise Policy）
   位置：企业管理员托管配置
   范围：所有用户、所有项目
   典型：禁止访问生产 DB · 强制代码审计日志

    ▼

2. 用户全局层（~/.claude/settings.json）
   范围：当前用户的所有项目
   典型：个人偏好 · 常用工具白名单

    ▼

3. 项目共享层（./.claude/settings.json）
   范围：当前项目的所有成员（提交到 Git）
   典型：团队级权限 · 项目级 Hooks · 共享 MCP

    ▼

4. 项目本地层（./.claude/settings.local.json）
   范围：仅当前用户在此项目（加入 .gitignore）
   典型：个人实验配置 · 临时覆盖
   优先级最高
```

## MCP 配置位置

```
用户级 MCP（所有项目可用）：
    ~/.claude.json         ← 注意：不在 ~/.claude/ 目录内！常见混淆点

项目级 MCP（仅当前项目）：
    ./.mcp.json            ← 提交到 Git，团队共享

规则：项目级 MCP 补充（不覆盖）用户级 MCP
```

## 权限决策流程

```
Claude 发起工具调用
        │
        ▼
PreToolUse Hook（确定性拦截层）
        ├─ 命中黑名单 → 立即拦截（exit 2）
        │
        ▼
查询 allowedTools 白名单
        ├─ 白名单命中 → 自动允许，无需用户确认
        │
        ▼
PermissionRequest Hook
        ├─ Hook 自动授权 → 跳过用户弹窗
        │
        ▼
用户手动确认
        ├─ 允许一次 → 本次执行
        ├─ 允许本会话 → 会话期间自动允许
        └─ 永久允许 → 写入 allowedTools 白名单
```

## allowedTools 配置示例

```json
{
  "allowedTools": [
    "Bash(git status)",
    "Bash(git diff*)",
    "Bash(npm test)",
    "Bash(npm run lint)",
    "Edit",
    "View",
    "mcp__github__list_issues",
    "mcp__github__*"
  ]
}
```

## 关键环境变量

```bash
ANTHROPIC_API_KEY="your-key"          # API 认证
CLAUDE_MODEL="claude-sonnet-4-6"      # 模型选择
MAX_MCP_OUTPUT_TOKENS=25000           # MCP 输出 Token 上限
ENABLE_TOOL_SEARCH=auto               # 工具搜索模式

# CI/CD 必须：防止 Claude 无限期等待用户输入
claude -p "your task" --output-format json
```

## 反模式清单

| 反模式 | 风险 | 正确做法 |
|--------|------|---------|
| Token 硬编码在 `.mcp.json` | 机密泄露 | 环境变量 `-e GITHUB_TOKEN` |
| CI/CD 不加 `-p` 标志 | 作业无限期挂起 | 始终使用 `--print` 模式 |
| 永久允许所有 MCP 工具 | 权限过度 | 按工具细粒度控制 |
| `settings.local.json` 提交到 Git | 个人配置污染团队 | 加入 `.gitignore` |

---

# 07 · MCP（Model Context Protocol）

> MCP 是 Claude Code 连接外部世界的标准化协议——统一接口，替代碎片化的专用集成方案。

---

## 架构

```
┌──────────────┐  JSON-RPC  ┌─────────────────────────┐
│  Claude Code  │ ◄────────► │      MCP Server          │
│   (客户端)    │stdio/SSE/  │ 封装外部服务访问逻辑       │
└──────────────┘    HTTP    │ GitHub / DB / Browser 等 │
                            └─────────────────────────┘
```

## 三种传输模式

| 模式 | 适用场景 | 特点 |
|------|---------|------|
| `stdio` | 本地进程 | 原生隔离，不经过网络 |
| `SSE` | 远程 HTTP 流式 | 实时推送 |
| `HTTP` | 远程 HTTP 非流式 | 简单请求-响应 |

## 配置结构

```json
// ~/.claude.json（用户级）
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": { "GITHUB_TOKEN": "$GITHUB_TOKEN" }
    }
  }
}

// ./.mcp.json（项目级，提交到 Git）
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@myorg/mcp-server-postgres"],
      "env": { "DB_URL": "$DATABASE_URL" }
    }
  }
}
```

## Tool Search 机制（上下文保护）

```
会话启动：仅加载工具名称（极低 Token 消耗）
    │
    ▼ Claude 遇到需要外部工具的任务
    │
    ▼ 搜索匹配的 MCP 工具名
    │
    ▼ 按需加载完整工具 Schema（进入上下文）

效果：10+ 个 MCP 服务器，上下文开销仍然最小
```

## 输出 Token 保护

```
警告阈值：10,000 tokens（显示警告）
默认上限：25,000 tokens（截断）

调整：export MAX_MCP_OUTPUT_TOKENS=50000
最佳实践：让 MCP 服务器分页/过滤响应，而非增加上限
```

## 社区生态（2026 年 3 月）

| MCP 服务器 | 工具数 | 核心能力 |
|-----------|-------|---------|
| `server-github` | 15 | Issues · PR · 仓库搜索 |
| `mcp-server-brave-search` | 1 | 网页搜索（400ms 均值）|
| `@playwright/mcp` | 多 | 浏览器自动化（150MB/实例）|
| 数据库系列 | 多 | SQL 查询、Schema 探索 |
| `server-slack` | 多 | 消息、频道、搜索 |

生态规模：200+ 社区服务器；GitHub 服务器被 **92%** 启用 MCP 的用户最先安装。

---

# 08 · 子 Agent & 多 Agent 系统（Delegation Layer）

> **设计原则**：受控并行，而非无限递归。
> 子 Agent 提供上下文隔离和并行能力，深度限制防止 Agent 扩散失控。

---

## 为什么需要子 Agent？

```
主 Agent 上下文窗口有限（200k tokens）。
当任务需要：
  · 并行探索多个实现方案
  · 隔离执行重型探索（不污染主上下文）
  · 专业分工（不同模型处理不同类型工作）

→ 将工作委派给子 Agent，仅将结论返回主上下文。
```

## 深度限制架构

```
主 Agent（上下文保持精简）
    │
    ├─► Sub-Agent A（独立上下文，仅返回结论）✓
    ├─► Sub-Agent B（独立上下文，仅返回结论）✓
    └─► Sub-Agent C（独立上下文，仅返回摘要）✓

❌ 严格禁止：
    Sub-Agent → Sub-Sub-Agent（深度 > 1，阻断）
```

## Git Worktree 隔离

```bash
# 子 Agent 在临时 Git Worktree 中执行
git worktree add /tmp/claude-subagent-xyz HEAD

优势：
  · 防止污染主工作目录
  · 子 Agent 的实验性变更不影响主分支
  · 多个子 Agent 可同时安全操作不同文件
  · 子 Agent 完成后自动清理 Worktree
```

## 模型选择策略

| 任务类型 | 推荐模型 | 原因 |
|---------|---------|------|
| 探索型（搜索、收集信息）| `claude-haiku-4-5` | 廉价快速 |
| 实现型（大多数编码）| `claude-sonnet-4-6` | 平衡 |
| 架构决策 / 深度推理 | `claude-opus-4-6` | 最强（14.5h 任务完成率 50%）|

## 并行 Agent Teams 模式

```
任务：代码审查
    │
    ├─► Reviewer A（Sonnet）：安全漏洞专项
    ├─► Reviewer B（Sonnet）：性能问题专项
    ├─► Reviewer C（Opus）：架构合理性评估
    │
    ▼
Validator（Opus，最终汇总）
    │
    ▼
统一审查报告返回主 Agent
```

## Builder-Validator 模式

```
针对每个功能模块：
    ├─ Builder Agent：实现功能
    └─ Validator Agent：验证实现

通过共享任务列表（JSON）协调，非直接通信：
    task_list.json:
        session_end_builder: completed
        session_end_validator: in_progress
```

## 何时不用子 Agent

| 场景 | 建议 | 原因 |
|------|------|------|
| 标准顺序编码 | 主循环执行 | 无并行需求，子 Agent 有开销 |
| 单线程调试 | 主循环执行 | 需要连续上下文 |
| 简单文件读写 | 直接工具调用 | 无需上下文隔离 |
| 需要完整历史 | 主循环执行 | 子 Agent 只返回摘要 |
