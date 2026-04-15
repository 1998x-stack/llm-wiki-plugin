# Pi Agent 深度解析（四）：`pi-coding-agent` —— 极简系统提示、四工具理念与 YOLO 模式

> **系列导读**：`pi-coding-agent` 是面向最终用户的完整 CLI 工具，也是 OpenClaw 等应用内嵌的 Agent 运行时。本篇剖析其每一个「刻意省略」的工程逻辑。

---

## 一、pi-coding-agent 在架构中的位置

```
┌─────────────────────────────────────────────────────────┐
│               pi-coding-agent                           │
│                                                         │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ 会话管理    │  │  工具系统    │  │  扩展系统     │  │
│  │ JSONL 持久化│  │  四核心工具  │  │  Skills/模板  │  │
│  │ 上下文压缩  │  │  工具验证    │  │  Package 分发 │  │
│  └─────────────┘  └──────────────┘  └───────────────┘  │
│                                                         │
│  ┌─────────────────────────────────────────────────┐   │
│  │            pi-agent-core（内嵌）                 │   │
│  │     Agent 循环 / 工具执行 / 事件流              │   │
│  └─────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

它是 Pi 将底层能力面向实际编程任务「落地」的层。

---

## 二、极简系统提示：< 1000 Token 的工程逻辑

### 对比

| Agent | 系统提示规模 | 内容 |
|-------|------------|------|
| Claude Code | ~8000 tokens | 大量行为规则、工具使用指南、格式约定、限制条款... |
| Codex CLI | ~4000 tokens | 类似 |
| **Pi** | **< 1000 tokens** | 核心行为描述 + 工具说明 |

### 为什么更短更好？

**1. Token 经济性**

每次 LLM 调用都会消耗系统提示的 token。一个 8000 token 的系统提示，在一次典型的多轮编程任务（20 次 LLM 调用）中：

```
额外消耗 = 8000 token × 20 次 = 160,000 tokens
换算成成本（claude-sonnet）≈ $0.48 额外支出/任务
```

而 1000 token 的系统提示同等场景只需 $0.06。**差距 8 倍**。

**2. 注意力竞争**

LLM 的注意力机制是有限资源。系统提示越长，模型分配给**实际任务**的注意力就越少。

**3. 可预期的行为**

系统提示越短，模型行为越可预期，调试也越容易。8000 token 的规则集很难追踪哪条规则在影响模型的某个具体输出。

### Mario 的核心观点

> 大量系统提示规则往往是在「帮 LLM 规避 LLM 的问题」，但这只是在**掩盖**问题而不是**解决**问题。更好的做法是在工具设计和上下文结构上下功夫。

---

## 三、四工具理念：bash 的图灵完备性

Pi 的内置工具**只有四个**，没有第五个：

```typescript
const CORE_TOOLS = [
  readTool,   // 读取文件内容
  writeTool,  // 写入/创建文件
  editTool,   // 精确编辑文件（diff 式修改）
  bashTool,   // 执行 bash 命令
];
```

### 为什么只有这四个？

**bash 工具是图灵完备的**：任何你能在终端做的事，bash 都能做：

```
需要搜索文件？        → bash: find / grep / rg
需要运行测试？        → bash: npm test / pytest / cargo test
需要 git 操作？       → bash: git diff / git commit / git log
需要安装依赖？        → bash: npm install / pip install
需要查看目录结构？    → bash: ls / tree / eza
需要网络请求？        → bash: curl / wget
需要数据库操作？      → bash: psql / sqlite3
需要 Docker？         → bash: docker build / docker run
```

那为什么还需要 read/write/edit？

- **read**：比 `bash: cat file` 更高效——直接返回文件内容，不经过 shell 解析，且可以指定行范围
- **write**：比 `bash: echo "..." > file` 更安全——处理特殊字符、换行符等边界情况
- **edit**：实现**精确 diff 式修改**，LLM 只需要指定「将 X 替换为 Y」，而不用重写整个文件

### 工具数量对 LLM 认知负担的影响

当 LLM 面对 20 个工具时，它在**每次决策**时都要从 20 个选项中选择一个，这本身就消耗 token 和注意力。4 个工具大幅降低了这个认知负担：

```
工具选择的计算复杂度 ∝ 工具数量
4 个工具 vs 20 个工具：决策复杂度降低 5 倍
```

### 四个工具的完整接口

```typescript
// read 工具
{
  name: 'read',
  parameters: {
    path: string,           // 文件路径
    startLine?: number,     // 可选：只读取部分内容
    endLine?: number,
  },
  returns: {
    output: string,         // 文件内容（LLM 通道）
    details: {
      path: string,
      lineCount: number,
      encoding: string,
    }
  }
}

// write 工具
{
  name: 'write',
  parameters: {
    path: string,      // 目标文件路径（自动创建父目录）
    content: string,   // 完整文件内容
  },
  returns: {
    output: string,    // "文件已写入: path"
    details: { path, bytesWritten, created: boolean }
  }
}

// edit 工具（精确 diff 式修改）
{
  name: 'edit',
  parameters: {
    path: string,        // 文件路径
    oldContent: string,  // 要替换的精确文本片段
    newContent: string,  // 替换后的文本
  },
  returns: {
    output: string,      // "编辑成功" 或详细错误
    details: { path, linesChanged, diff }
  }
}

// bash 工具
{
  name: 'bash',
  parameters: {
    command: string,       // Shell 命令
    workingDir?: string,   // 工作目录（默认当前目录）
    timeout?: number,      // 超时（毫秒，默认 30000）
  },
  returns: {
    output: string,        // stdout + stderr
    details: { exitCode, stdout, stderr, duration }
  }
}
```

---

## 四、YOLO 模式：「你只活一次」的默认设定

### 什么是 YOLO 模式？

在大多数 Agent 工具中，执行每个工具调用（尤其是 bash 命令）之前，会弹出权限确认：

```
╔═══════════════════════════════════════════════╗
║  Agent 想要执行以下命令：                     ║
║                                               ║
║    rm -rf ./build && npm run build            ║
║                                               ║
║  [允许]  [只允许一次]  [拒绝]                 ║
╚═══════════════════════════════════════════════╝
```

**Pi 默认完全跳过这个确认步骤，直接执行。** 这就是 YOLO 模式。

### 为什么这是正确的设计？

**理由 1：确认弹窗对专业开发者是干扰**

专业开发者在使用 AI Agent 时，通常已经对要执行的任务有清晰预期。每隔几秒弹出一个确认窗口会完全打断心流。

**理由 2：安全应该来自环境隔离，而不是弹窗**

```
弹窗安全模型（伪安全）：
用户看到命令 → [允许] → 命令执行
问题：用户不一定理解命令的副作用，"允许"变成了习惯性点击

环境隔离安全模型（真安全）：
在 Docker 容器中运行 Pi
→ 即使 Agent 执行了危险命令
→ 损害被限制在容器内
→ 容器销毁即清理
```

**理由 3：弹窗无法防止真正的错误**

如果 LLM 产生了一个错误的命令，一个经验不足的用户可能仍然会点「允许」（因为他们不理解命令的含义）。弹窗只是提供了**虚假的安全感**。

### Pi 对安全的建议

```bash
# 在 Docker 中运行 Pi（推荐的生产用法）
docker run -it --rm \
  -v $(pwd):/workspace \
  -e ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY \
  mariozechner/pi-coding-agent

# 这才是真正的隔离——即使 Agent 执行了 rm -rf /，也只影响容器
```

---

## 五、会话管理系统

### 5.1 JSONL 会话格式

每个会话存储为一个 JSONL 文件，位于 `~/.pi/sessions/[session-id].jsonl`：

```jsonl
{"type":"session_start","sessionId":"20251201-143022","model":"claude-sonnet-4-5","timestamp":1735000000000}
{"type":"user","content":"帮我实现快速排序并写单元测试","timestamp":1735000001000}
{"type":"assistant","content":[{"type":"thinking","text":"用户需要..."},{"type":"text","text":"好的，我来实现..."},{"type":"toolCall","name":"write","id":"tc_1","input":{"path":"sort.ts","content":"..."}}],"usage":{"inputTokens":450,"outputTokens":312,"totalTokens":762}}
{"type":"tool_result","toolCallId":"tc_1","output":"文件已写入","details":{"path":"sort.ts","bytesWritten":1024}}
{"type":"assistant","content":[{"type":"toolCall","name":"bash","id":"tc_2","input":{"command":"npx jest sort.test.ts"}}],"usage":{"inputTokens":820,"outputTokens":45}}
{"type":"tool_result","toolCallId":"tc_2","output":"PASS sort.test.ts\n✓ quickSort sorts empty array\n✓ quickSort sorts numbers","details":{"exitCode":0}}
{"type":"assistant","content":[{"type":"text","text":"实现完成！所有测试通过。"}],"usage":{"inputTokens":950,"outputTokens":28}}
{"type":"session_end","totalTokens":1825,"estimatedCost":0.0023,"duration":18400}
```

**JSONL 格式的优势**：
- 流式写入（不需要等会话结束才能写文件）
- 部分读取（只读最后 N 条）
- 断点恢复（崩溃后不丢失已完成部分）
- 后处理友好（jq、Python 脚本等）

### 5.2 会话管理命令

```bash
pi --list-sessions          # 列出最近的会话
pi --resume                 # 恢复最近一次会话
pi --resume session-id      # 恢复指定会话
pi --export session-id      # 导出为 Markdown 或 HTML
```

### 5.3 上下文压缩（Compaction）

当会话接近模型的上下文窗口限制时，Pi 自动触发压缩：

```
压缩前（接近上下文窗口）：
[用户1][助手1][工具][用户2][助手2][工具]...[用户N]
   ▲_________________________▲
   这部分即将超出上下文窗口

压缩后：
[摘要: 之前完成了 A、B、C 工作，当前状态为...][用户N]
```

压缩策略是**可定制的**（通过扩展系统），默认策略：

1. 使用当前模型（或更便宜的模型）生成对话摘要
2. 保留最近 N 条消息的完整内容
3. 将摘要注入为 system 消息
4. 删除压缩范围内的旧消息

---

## 六、项目上下文文件

Pi 在启动时自动从多个位置加载**项目感知上下文**：

```
加载顺序（后加载的优先级更高）：

1. ~/.pi/agent/AGENTS.md          全局 Agent 指令（个人习惯、编码风格）
2. ~/projects/AGENTS.md           工作区级别指令
3. ~/projects/my-repo/AGENTS.md   项目级别指令
4. ./src/AGENTS.md                子目录级别指令（如存在）
5. ./SYSTEM.md                    覆盖/追加默认系统提示
```

**典型的 `AGENTS.md` 内容：**

```markdown
# 项目：TapTap 游戏代码生成系统

## 技术栈
- TypeScript 5.x + Bun 运行时
- LangGraph 用于 Agent 编排
- DashScope/Qwen API 作为主要 LLM
- Neo4j 用于代码知识图谱

## 编码规范
- 所有函数必须有 JSDoc 注释（中文）
- 错误处理使用 Result<T, E> 模式
- 日志使用 loguru 风格

## 项目结构
- src/agents/: Agent 定义
- src/tools/: 工具实现
- src/prompts/: 提示词模板
- tests/: 测试文件（与 src 镜像结构）

## 重要约束
- 不要修改 src/core/ 下的文件，除非明确被要求
- 所有 API 调用必须有重试逻辑
```

---

## 七、Skills（技能包）系统

Skills 是「渐进式披露」（Progressive Disclosure）的实现：

```
初始状态（精简上下文）：
系统提示: 750 tokens
工具: 4 个

触发 /use python-testing-skill 后：
系统提示: 750 + 280 = 1030 tokens（追加 Python 测试最佳实践）
工具: 4 + 2 = 6 个（追加 pytest-runner、coverage-reporter）
```

Skills 只在**需要时才注入上下文和工具**，避免在所有任务中都携带所有知识。

---

## 八、四种运行模式

| 模式 | 命令 | 用途 |
|------|------|------|
| **交互式** | `pi` | 日常开发，完整 TUI 界面 |
| **Print/JSON** | `pi -p "任务"` | 脚本集成、CI/CD 管道 |
| **RPC** | `pi --rpc` | 程序化控制（JSON-RPC over stdio） |
| **SDK** | `createAgentSession()` | 嵌入其他 TypeScript 应用 |

```bash
# 交互式（完整 TUI）
pi

# 单次任务（输出到 stdout）
pi -p "给 src/utils.ts 添加 JSDoc 注释"

# JSON 输出（机器可读）
pi -p "分析项目结构" --json

# 指定模型
pi --model openai/gpt-4o
pi --model google/gemini-2.5-pro
pi --model ollama/llama3.1  # 本地模型

# 以特定文件作为上下文启动
pi --context src/sort.ts
```

---

## 九、「故意省略」的功能清单

每一个省略都是刻意的工程决策：

| 省略的功能 | 省略理由 | 替代方案 |
|-----------|---------|---------|
| **子代理** | 增加不可预期性，调试困难 | 扩展系统实现 |
| **计划模式** | 计划往往在执行中失效，徒增 token | 扩展系统实现 |
| **MCP 支持** | MCP 生态不稳定，工具质量参差不齐 | 扩展适配 MCP SDK |
| **后台 bash** | 无法观测状态，调试困难 | 不提供 |
| **权限弹窗** | 伪安全，打断工作流 | 扩展实现 / Docker 隔离 |
| **Web 搜索** | 质量难以控制 | 扩展 / bash: curl |
| **LSP 集成** | bash 工具已够用 | 扩展实现 |
| **to-do 列表** | LLM 自己记忆即可 | 扩展实现 |
| **max_steps** | 没有实际价值 | 不提供 |

---

*下一篇：`pi-tui` —— 终端 UI 的差分渲染与无闪烁输出*
