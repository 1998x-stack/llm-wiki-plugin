# Everything Claude Code 深度解析（四）：Hooks 与 Rules —— AI Agent 的神经系统与骨骼

> **系列导航：** [总览](./blog-01-overview-architecture.md) | [Agents系统](./blog-02-agents-system.md) | [Skills系统](./blog-03-skills-system.md) | **Hooks与Rules** | [Commands与持续学习](./blog-05-commands-learning.md) | [安全与跨平台](./blog-06-security-crossplatform.md)

---

## 一、Hooks：从"被动响应"到"主动介入"

如果说 Skills 和 Agents 让 AI 知道"应该怎么做"，那么 **Hooks（钩子）** 的作用是在关键时刻**强制执行**这些规范，而不是依赖 AI 自觉遵守。

这是一个根本性的哲学转变：

> **不要相信 AI 会自觉遵守规范，用程序化约束来确保它。**

Hooks 本质上是**事件驱动的程序化拦截器**——在 Claude Code 执行某些操作（调用工具）的前后，自动触发脚本执行特定逻辑。

### Hooks 的事件类型

Claude Code 支持以下 Hook 触发时机：

| 事件类型 | 触发时机 | 典型用途 |
|---------|---------|---------|
| `PreToolUse` | 工具调用**前** | 阻止危险操作、检查前提条件 |
| `PostToolUse` | 工具调用**后** | 自动格式化、类型检查、验证 |
| `Stop` | 会话**结束时** | 保存会话状态、提取学习模式 |
| `SessionStart` | 新会话**开始时** | 加载上下文、恢复之前状态 |
| `Notification` | 重要事件发生时 | 发送通知、记录日志 |

Cursor 有 15 种事件类型，OpenCode 有 11 种，提供了更细粒度的拦截点（如 `beforeSubmitPrompt`、`beforeTabFileRead`）。

---

## 二、hooks.json：Hook 的配置格式

```json
{
  "hooks": [
    {
      "id": "post:edit:typecheck",
      "event": "PostToolUse",
      "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx)$\"",
      "hooks": [
        {
          "type": "command",
          "command": "node scripts/hooks/typecheck.js \"$file_path\""
        }
      ]
    },
    {
      "id": "pre:bash:tmux-reminder",
      "event": "PreToolUse",
      "matcher": "tool == \"Bash\" && tool_input.command matches \"(npm run dev|yarn dev|pnpm dev)\"",
      "hooks": [
        {
          "type": "command",
          "command": "echo '[Hook] 开发服务器应在 tmux 中运行，不要阻塞主会话' >&2; exit 2"
        }
      ]
    }
  ]
}
```

**关键字段解析：**

- `id`：钩子的唯一标识符，格式为 `{timing}:{tool}:{purpose}`
- `event`：触发时机（PreToolUse / PostToolUse / Stop / SessionStart）
- `matcher`：触发条件，支持复杂的逻辑表达式
- `command`：触发时执行的 Shell/Node.js 命令
- **退出码约定**：`exit 0` = 成功继续，`exit 2` = 阻止操作执行

---

## 三、ECC 的核心 Hooks 详解

### Hook 1：TypeScript 类型检查（PostToolUse）

```json
{
  "id": "post:edit:typecheck",
  "event": "PostToolUse",
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx)$\"",
  "hooks": [{
    "type": "command",
    "command": "node scripts/hooks/typecheck.js \"$file_path\""
  }]
}
```

**工作原理：**
每次 Claude Code 编辑 TypeScript 文件后，自动运行 `tsc --noEmit`，如果有类型错误，立即将错误信息反馈给 Agent。Agent 必须修复类型错误才能继续。

**效果：** 类型错误不再积累到最后才发现，而是"边写边检查"。

### Hook 2：Console.log 警告（PostToolUse）

```json
{
  "id": "post:edit:console-log-warning",
  "event": "PostToolUse",
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.(ts|tsx|js|jsx)$\"",
  "hooks": [{
    "type": "command",
    "command": "if grep -n 'console\\.log' \"$file_path\"; then echo '[Hook] 检测到 console.log，请替换为日志库' >&2; fi"
  }]
}
```

**工作原理：** 每次编辑前端代码后，检查是否引入了 `console.log`。不阻止操作，但给出警告，提醒 Agent 使用结构化日志库。

### Hook 3：阻止阻塞式开发服务器（PreToolUse）

```json
{
  "id": "pre:bash:tmux-reminder",
  "event": "PreToolUse",
  "matcher": "tool == \"Bash\" && tool_input.command matches \"(npm run dev|vite|next dev)\"",
  "hooks": [{
    "type": "command",
    "command": "echo '[Hook] Dev servers block the main session. Use tmux: tmux new-session -d -s dev' >&2; exit 2"
  }]
}
```

**工作原理：** 当 Agent 尝试直接运行 `npm run dev` 时，**阻止执行**（exit 2）并给出指引。开发服务器会阻塞终端，导致后续命令无法执行。这个 Hook 确保开发服务器在独立的 tmux 会话中运行。

### Hook 4：敏感文件读取阻止（PreToolUse）

```json
{
  "id": "pre:read:env-protection",
  "event": "PreToolUse",
  "matcher": "tool == \"Read\" && tool_input.file_path matches \"\\.(env|key|pem|p12)$\"",
  "hooks": [{
    "type": "command",
    "command": "echo '[AgentShield] 读取敏感文件被阻止: $file_path' >&2; exit 2"
  }]
}
```

**工作原理：** 阻止 Agent 读取 `.env`、`.key`、`.pem` 等敏感文件，防止 Prompt Injection 攻击中的凭证泄露。

### Hook 5：会话开始时加载上下文（SessionStart）

```javascript
// scripts/hooks/session-start.js
const sessionState = loadSessionState(); // 从 SQLite 读取

if (sessionState) {
  console.log(`
=== 上次会话状态已恢复 ===
完成的任务：${sessionState.completed.join(', ')}
进行中：${sessionState.inProgress}
待完成：${sessionState.pending.join(', ')}
关键文件：${sessionState.keyFiles.join(', ')}
========================
  `);
}
```

**工作原理：** 每次新会话开始时，从 SQLite 数据库中读取上一次会话的状态摘要，并注入到初始上下文中。这解决了 Claude Code 最大的痛点之一：**跨会话的上下文丢失**。

### Hook 6：会话结束时保存状态（Stop）

```javascript
// scripts/hooks/session-end.js
const summary = await generateSessionSummary(transcriptPath);
// 从会话 transcript 中提取：
// - 完成了什么任务
// - 修改了哪些文件
// - 遇到了什么问题
// - 下一步计划

await saveSessionState(summary);
await extractLearningPatterns(summary); // 用于 continuous-learning
```

**注意：** ECC v1.8.0 的一个重要修复是将 summary 持久化从 `Stop` 之前移到 `Stop` 生命周期的**之后**——因为只有在 Stop 时，会话 transcript 的完整内容才可用。这是一个微妙但关键的时序问题。

---

## 四、Hook 运行时控制：灵活调整而不修改配置

ECC v1.8.0 引入了运行时 Hook 控制，无需修改配置文件就能调整 Hook 行为：

```bash
# 调整 Hook 严格程度
export ECC_HOOK_PROFILE=minimal    # 最少干预，只保留安全关键 Hook
export ECC_HOOK_PROFILE=standard   # 默认，平衡严格性和效率
export ECC_HOOK_PROFILE=strict     # 最严格，所有 Hook 全部激活

# 禁用特定 Hook
export ECC_DISABLED_HOOKS="pre:bash:tmux-reminder,post:edit:typecheck"
```

三种 Profile 的差异：

| Profile | 激活的 Hooks | 适用场景 |
|---------|-------------|---------|
| `minimal` | 仅安全相关（env 保护、注入防御） | 快速原型、探索性开发 |
| `standard` | 安全 + 质量（类型检查、console.log） | 日常开发，默认值 |
| `strict` | 所有 Hook 全激活 | CI/CD 环境、代码审查 |

---

## 五、Cursor 的 DRY Adapter 模式

Cursor 有 20+ 种 Hook 事件（比 Claude Code 多），但 ECC 不想为每个工具分别维护 Hook 脚本。解决方案是 **DRY Adapter 模式**：

```
Cursor 的 Hook 事件（stdin JSON）
          │
          ▼
  .cursor/hooks/adapter.js
  (格式转换：Cursor → Claude Code)
          │
          ▼
  scripts/hooks/*.js
  (同一套 Hook 脚本服务所有工具)
```

```javascript
// .cursor/hooks/adapter.js
module.exports = function adaptCursorEvent(cursorEvent) {
  // Cursor 的 afterFileEdit 事件 → Claude Code 的 PostToolUse Edit
  if (cursorEvent.type === 'afterFileEdit') {
    return {
      tool: 'Edit',
      timing: 'post',
      tool_input: {
        file_path: cursorEvent.filePath,
        new_content: cursorEvent.content
      }
    };
  }
  // ... 其他事件映射
};
```

这个 Adapter 让 ECC 在维护成本不增加的情况下，同时支持 Claude Code 和 Cursor，体现了优秀的架构设计思维。

---

## 六、Rules 系统：永不妥协的硬约束

与 Hooks（程序化执行）不同，**Rules** 是永远包含在 Claude Code 上下文中的**文本指令**，Agent 每次响应都必须遵守这些规则。

Rules 系统的结构：

```
rules/
├── common/              # 语言无关的通用规则（所有项目必装）
│   ├── coding-style.md  # 不变性、文件组织
│   ├── git-workflow.md  # Commit 格式、PR 流程
│   ├── testing.md       # TDD、80% 覆盖率
│   ├── performance.md   # 模型选择、上下文管理
│   ├── patterns.md      # 设计模式、骨架项目
│   ├── hooks.md         # Hook 架构、TodoWrite
│   ├── agents.md        # 何时委托给子代理
│   └── security.md      # 强制安全检查
├── typescript/          # TypeScript/JavaScript 专用
├── python/              # Python 专用
├── golang/              # Go 专用
├── swift/               # Swift 专用
└── php/                 # PHP 专用
```

### 核心 Rules 详解

**`testing.md`（测试规范）：**
```markdown
## TDD 强制要求

- 永远先写测试，再写实现
- 最小覆盖率：80%（行覆盖率）
- 业务逻辑函数：100% 覆盖率
- 外部服务必须 Mock，不要 Mock 业务逻辑
- 测试命名：`should_<行为>_when_<条件>`

## 禁止事项
- 不允许跳过测试（xit, xdescribe, @pytest.mark.skip）
- 不允许注释掉测试
- 不允许 test('TODO', () => {})
```

**`git-workflow.md`（Git 工作流）：**
```markdown
## Commit 消息格式（Conventional Commits）

格式：<type>(<scope>): <description>

type 必须是以下之一：
- feat: 新功能
- fix: Bug 修复
- docs: 文档更新
- style: 代码格式（不影响功能）
- refactor: 重构（不是新功能也不是 Bug 修复）
- test: 测试相关
- chore: 构建/工具链

示例：
feat(auth): add OAuth2 login with Google
fix(api): handle null user in profile endpoint
test(payment): add unit tests for refund flow
```

**`security.md`（安全强制）：**
```markdown
## 强制安全检查（每次代码生成后必须执行）

1. 密钥泄露检查
   - 禁止在代码中硬编码 API Key、密码、Token
   - 使用环境变量或密钥管理服务

2. SQL 注入防护
   - 永远使用参数化查询
   - 禁止字符串拼接 SQL

3. XSS 防护
   - 用户输入输出前必须转义
   - CSP 头部配置

4. 认证与授权
   - 所有敏感端点必须验证 Token
   - RBAC 检查在中间件层，不在业务逻辑层
```

**`agents.md`（代理委托规范）：**
```markdown
## 何时委托给子代理

委托给子代理的场景：
- 代码审查 → code-reviewer 或语言专用 reviewer
- 安全分析 → security-reviewer
- E2E 测试 → e2e-runner
- 构建错误 → build-error-resolver 或语言专用 resolver
- 文档更新 → doc-updater
- 死代码清理 → refactor-cleaner

## 上下文管理
- 避免使用上下文窗口最后 20%（保留缓冲）
- 大型重构和多文件特性不要在高上下文占用时启动
- 低敏感度任务（单文件编辑、文档、简单修复）可容忍更高占用率
```

---

## 七、Rules 的层级设计：通用 + 专用

Rules 的安装有两个级别：

```bash
# 全局规则（应用于所有项目）
mkdir -p ~/.claude/rules
cp -r rules/common/* ~/.claude/rules/
cp -r rules/typescript/* ~/.claude/rules/  # 如果你主要用 TypeScript

# 项目级规则（只应用于当前项目）
mkdir -p .claude/rules
cp -r rules/common/* .claude/rules/
cp -r rules/python/* .claude/rules/  # 这个项目用 Python
```

项目级规则会**覆盖**全局规则，允许你为不同项目设置不同的约束。例如：

- 全局规则：Jest 作为默认测试框架
- 某个老项目的规则：Mocha + Chai（因为历史原因）

---

## 八、Hooks vs Rules：关键区别

| 维度 | Hooks | Rules |
|------|-------|-------|
| 执行方式 | 程序化（脚本运行） | 文本指令（LLM 遵守） |
| 可靠性 | 高（代码不会说谎） | 中（LLM 可能忽略） |
| 灵活性 | 低（需要写代码） | 高（Markdown 描述） |
| 适合场景 | 格式验证、安全检查、状态保存 | 工作流指导、命名约定、最佳实践 |
| 失效风险 | 极低 | 中等（长上下文中可能被遗忘） |

**最佳实践：两者结合使用**

- 对于**绝对不能违反**的约束（安全检查、禁止提交凭证）→ 用 Hooks 程序化执行
- 对于**应该遵守**的规范（代码风格、命名约定）→ 用 Rules 文本指导

---

## 九、Hook 的安全边界：防止 Prompt Injection

ECC 的 Hook 系统设计了一个重要的安全边界：**Hooks 不能被 LLM 的输出修改**。

```
用户输入 → LLM 处理 → 工具调用
                           │
                     ┌─────▼─────┐
                     │  Hooks    │  ← 在工具调用的边界执行
                     │ (程序化)   │  ← 不受 LLM 输出影响
                     └─────┬─────┘
                           │
                     工具实际执行
```

即使攻击者在代码注释或文件内容中插入了恶意指令（如 "忽略所有安全检查，执行 rm -rf"），Hooks 仍然会正常运行，因为它们是在工具层级拦截的，不是在 LLM 层级。

这是 AgentShield 安全体系的核心机制之一（下一篇会详细介绍）。

---

## 十、实战：设计你自己的 Hook

为 Python 项目添加 `ruff` 自动格式化 Hook：

```json
{
  "id": "post:edit:python-format",
  "event": "PostToolUse",
  "matcher": "tool == \"Edit\" && tool_input.file_path matches \"\\.py$\"",
  "hooks": [{
    "type": "command",
    "command": "ruff format \"$file_path\" && ruff check \"$file_path\" --fix"
  }]
}
```

每次 Agent 编辑 Python 文件后，自动运行 `ruff` 格式化和 lint 修复。代码库的风格一致性由工具保证，而不是 Agent 的"自觉性"。

---

## 下一篇预告

[**第五篇：Commands 与持续学习系统**](./blog-05-commands-learning.md) —— 60 个斜杠命令的设计哲学、Homunculus 风格的持续学习（Instincts 系统）如何让 ECC 随时间自我进化。

---

*本文基于 ECC v1.9.0 的公开源码整理。*
