# Pi Agent 深度解析（六）：扩展系统 —— 用 TypeScript 把 Pi 变成任何你想要的东西

> **系列终章**：扩展系统是 Pi「如果我不需要，就不构建它」哲学的完整闭环。所有被刻意省略的功能，都在这里找到了它们正确的归宿。

---

## 一、扩展系统是哲学的最终兑现

回顾 Pi 省略的功能清单：子代理、计划模式、权限确认、MCP 支持、to-do 列表……

每一个「没有」都有一个对应的回答：**用扩展实现它，按你自己的方式。**

这不是「功能残缺」的借口，而是一个严肃的架构主张：

> 通用框架内置的这些功能，往往是按照框架作者的假设设计的。而你的场景、你的工作流、你的安全需求，没有人比你更了解。扩展系统让你自己成为框架的完成者。

---

## 二、Extension API：完整接口

```typescript
import type {
  Extension,
  AgentSession,
  AgentTool,
  TuiComponent,
  HookContext,
} from '@mariozechner/pi-coding-agent';

const myExtension: Extension = {
  // ── 基本信息 ─────────────────────────────────────────
  name: 'my-extension',
  version: '1.0.0',
  description: '我的自定义扩展',

  // ── 工具注入（LLM 可调用） ────────────────────────────
  tools: [myCustomTool1, myCustomTool2],

  // ── 斜杠命令（用户在输入框中触发） ──────────────────────
  commands: [
    {
      name: 'review',
      description: '对当前文件进行代码审查',
      execute: async (session: AgentSession) => { /* ... */ }
    }
  ],

  // ── 键盘快捷键 ────────────────────────────────────────
  shortcuts: [
    {
      key: 'ctrl+r',
      description: '运行测试',
      execute: async (session: AgentSession) => { /* ... */ }
    }
  ],

  // ── 生命周期钩子 ──────────────────────────────────────
  hooks: {
    // 每次 LLM 调用前（动态上下文注入的关键点）
    beforeLlmCall: async (ctx: HookContext) => { /* ... */ },

    // 工具调用前（权限门控的关键点）
    beforeToolCall: async (ctx: HookContext) => { /* ... */ },

    // 工具调用后
    afterToolCall: async (ctx: HookContext) => { /* ... */ },

    // 上下文压缩时（自定义压缩策略）
    onCompact: async (ctx: HookContext) => { /* ... */ },

    // 会话开始/结束
    onSessionStart: async (ctx: HookContext) => { /* ... */ },
    onSessionEnd: async (ctx: HookContext) => { /* ... */ },
  },

  // ── TUI 扩展（pi-tui 存在时生效） ─────────────────────
  statusBarItems: [myStatusBarComponent],
  overlays: [myPermissionDialog],
};

export default myExtension;
```

---

## 三、实战案例：逐一实现「省略」的功能

### 案例 1：RAG 动态上下文注入

这是将 Pi 接入向量数据库、实现检索增强生成的关键扩展点：

```typescript
import { QdrantClient } from '@qdrant/js-client-rest';
import { getModel } from '@mariozechner/pi-ai';

const qdrant = new QdrantClient({ url: 'http://localhost:6333' });
const embeddingModel = getModel('openai', 'text-embedding-3-small');

const ragExtension: Extension = {
  name: 'rag-context',
  version: '1.0.0',

  hooks: {
    beforeLlmCall: async (ctx) => {
      // 获取用户最新输入
      const lastUserMsg = ctx.messages
        .filter(m => m.role === 'user')
        .at(-1)?.content;

      if (!lastUserMsg) return;

      // 生成查询向量
      const embedding = await generateEmbedding(lastUserMsg, embeddingModel);

      // 从向量数据库检索相关代码片段
      const results = await qdrant.search('codebase', {
        vector: embedding,
        limit: 5,
        score_threshold: 0.75,
      });

      if (results.length === 0) return;

      // 构建检索上下文
      const ragContext = results
        .map(r => `// ${r.payload.path}\n${r.payload.content}`)
        .join('\n\n---\n\n');

      // 注入到 messages 头部（作为参考上下文）
      ctx.messages.unshift({
        role: 'system',
        content: `以下是与当前任务相关的代码片段（来自代码库检索）：\n\n${ragContext}`,
        timestamp: Date.now(),
      });
    }
  }
};
```

### 案例 2：权限确认门控

为危险命令添加交互式确认，只需一个扩展：

```typescript
// 判断命令是否危险
function isDangerousCommand(cmd: string): { dangerous: boolean; reason: string } {
  const patterns = [
    { re: /rm\s+-rf?\s+[^/~]/, reason: '递归删除文件' },
    { re: />\s*\/dev\/sd/, reason: '写入磁盘设备' },
    { re: /curl.+\|\s*bash/, reason: '下载并执行脚本' },
    { re: /DROP\s+DATABASE/i, reason: '删除数据库' },
    { re: /git\s+push.*--force/, reason: '强制推送' },
  ];
  for (const { re, reason } of patterns) {
    if (re.test(cmd)) return { dangerous: true, reason };
  }
  return { dangerous: false, reason: '' };
}

const permissionExtension: Extension = {
  name: 'permission-gates',
  version: '1.0.0',

  hooks: {
    beforeToolCall: async (ctx) => {
      if (ctx.tool.name !== 'bash') return { proceed: true };

      const { dangerous, reason } = isDangerousCommand(ctx.args.command);
      if (!dangerous) return { proceed: true };

      // 在 TUI 中弹出确认对话框
      const confirmed = await ctx.tui.confirm({
        title: '⚠️  检测到危险命令',
        body: [
          `命令：${ctx.args.command}`,
          `风险：${reason}`,
          '',
          '确认执行？'
        ].join('\n'),
        confirmLabel: '执行',
        cancelLabel: '取消',
        defaultValue: false,   // 默认取消
      });

      return confirmed ? { proceed: true } : { cancel: '用户取消了危险命令的执行' };
    }
  },

  // 弹窗 TUI 组件
  overlays: [PermissionConfirmOverlay],
};
```

### 案例 3：子代理系统（Multi-Agent）

```typescript
import { createAgentSession } from '@mariozechner/pi-agent-core';
import { getModel } from '@mariozechner/pi-ai';

// 规划代理：负责分解任务
const plannerSession = createAgentSession({
  model: getModel('anthropic', 'claude-opus-4-5'),
  systemPrompt: `你是一个任务规划专家。
将用户的复杂需求分解为具体的、可执行的子任务列表。
输出格式：JSON 数组，每项包含 { id, description, dependsOn: [] }`,
  tools: [],   // 规划代理不需要工具，只做推理
});

// 执行代理：负责实际编码
const coderSession = createAgentSession({
  model: getModel('anthropic', 'claude-sonnet-4-5'),
  systemPrompt: '你是一个专业的 TypeScript 程序员，专注于高质量代码实现。',
  tools: [readTool, writeTool, editTool, bashTool],
});

const multiAgentTool: AgentTool = {
  name: 'orchestrate',
  description: '将复杂任务分配给专门的子代理执行',
  parameters: Type.Object({
    task: Type.String({ description: '复杂任务描述' }),
    strategy: Type.Union([
      Type.Literal('plan-then-execute'),
      Type.Literal('parallel'),
    ]),
  }),

  execute: async (_, args, signal, onUpdate) => {
    if (args.strategy === 'plan-then-execute') {
      // 第一步：规划
      onUpdate({ type: 'status', message: '规划代理分解任务中...' });
      const planResult = await plannerSession.prompt(
        `分解以下任务：${args.task}`
      );

      const plan = JSON.parse(extractJson(planResult.text));
      onUpdate({ type: 'status', message: `生成了 ${plan.length} 个子任务` });

      // 第二步：串行执行（按依赖顺序）
      const results = [];
      for (const subtask of topologicalSort(plan)) {
        onUpdate({ type: 'status', message: `执行：${subtask.description}` });
        const result = await coderSession.prompt(subtask.description);
        results.push({ id: subtask.id, result: result.text });
      }

      return {
        output: `所有子任务完成：\n${results.map(r => `- ${r.id}: ${r.result}`).join('\n')}`,
        details: { plan, results }
      };
    }
  }
};

const multiAgentExtension: Extension = {
  name: 'multi-agent',
  version: '1.0.0',
  tools: [multiAgentTool],
};
```

### 案例 4：计划模式（Plan Mode）

```typescript
let planningMode = false;
const PLANNING_SYSTEM_PROMPT = `你现在处于计划模式。
不要执行任何工具调用，只生成详细的执行计划。
格式：Markdown checklist，每项以 - [ ] 开始。
计划完成后提示用户运行 /execute 开始执行。`;

const planModeExtension: Extension = {
  name: 'plan-mode',
  version: '1.0.0',

  commands: [
    {
      name: 'plan',
      description: '进入计划模式（只规划不执行）',
      execute: async (session) => {
        planningMode = true;
        session.setSystemPromptOverride(PLANNING_SYSTEM_PROMPT);
        session.tui.notify('✦ 进入计划模式。描述你的任务，Agent 将生成执行计划。');
        session.tui.notify('  完成后输入 /execute 开始执行，或 /cancel-plan 退出。');
      }
    },
    {
      name: 'execute',
      description: '执行当前计划',
      execute: async (session) => {
        planningMode = false;
        session.clearSystemPromptOverride();
        await session.prompt('请按照之前生成的计划逐步执行，完成后报告结果。');
      }
    },
    {
      name: 'cancel-plan',
      description: '退出计划模式',
      execute: async (session) => {
        planningMode = false;
        session.clearSystemPromptOverride();
        session.tui.notify('已退出计划模式。');
      }
    }
  ],

  hooks: {
    beforeToolCall: async (ctx) => {
      if (planningMode) {
        // 在计划模式下阻止所有工具执行
        return {
          cancel: '计划模式：请先运行 /execute 再执行工具操作。'
        };
      }
      return { proceed: true };
    }
  }
};
```

### 案例 5：MCP 集成适配器

```typescript
import { Client as McpClient } from '@modelcontextprotocol/sdk/client/index.js';
import { SSEClientTransport } from '@modelcontextprotocol/sdk/client/sse.js';

async function createMcpExtension(serverUrl: string): Promise<Extension> {
  // 连接到 MCP 服务器
  const client = new McpClient({ name: 'pi-mcp-bridge', version: '1.0.0' });
  const transport = new SSEClientTransport(new URL(serverUrl));
  await client.connect(transport);

  // 获取 MCP 服务器提供的工具列表
  const { tools: mcpTools } = await client.listTools();

  // 将 MCP 工具转换为 Pi AgentTool 格式
  const piTools: AgentTool[] = mcpTools.map((mcpTool) => ({
    name: `mcp__${mcpTool.name}`,
    label: mcpTool.name,
    description: mcpTool.description ?? '',
    parameters: mcpTool.inputSchema,   // 直接复用 MCP 的 JSON Schema

    execute: async (toolCallId, args, signal) => {
      const result = await client.callTool({
        name: mcpTool.name,
        arguments: args,
      });

      const content = result.content
        .map(c => c.type === 'text' ? c.text : JSON.stringify(c))
        .join('\n');

      return { output: content };
    }
  }));

  return {
    name: `mcp-${new URL(serverUrl).hostname}`,
    version: '1.0.0',
    description: `MCP 适配器：${serverUrl}`,
    tools: piTools,
  };
}

// 使用：连接到任意 MCP 服务器
const githubMcp = await createMcpExtension('https://github.mcp.example.com/sse');
const notionMcp = await createMcpExtension('https://notion.mcp.example.com/sse');
const customMcp = await createMcpExtension('http://localhost:3001/sse');
```

### 案例 6：成本与 Token 追踪仪表板

```typescript
interface CostRecord {
  timestamp: number;
  inputTokens: number;
  outputTokens: number;
  cost: number;
  model: string;
}

const records: CostRecord[] = [];

// TUI 状态栏组件：实时显示成本
const CostStatusItem: TuiComponent = {
  render(width: number): TerminalLine[] {
    const totalCost = records.reduce((sum, r) => sum + r.cost, 0);
    const totalTokens = records.reduce((sum, r) => sum + r.inputTokens + r.outputTokens, 0);
    return [{
      text: ` 💰 $${totalCost.toFixed(4)}  🔢 ${(totalTokens/1000).toFixed(1)}k tokens`,
      color: totalCost > 1.0 ? 'yellow' : 'green',
    }];
  }
};

const costTrackerExtension: Extension = {
  name: 'cost-tracker',
  version: '1.0.0',

  hooks: {
    afterLlmCall: async (ctx) => {
      const usage = ctx.lastMessage?.usage;
      if (!usage) return;

      records.push({
        timestamp: Date.now(),
        inputTokens: usage.inputTokens,
        outputTokens: usage.outputTokens,
        cost: usage.estimatedCost ?? 0,
        model: ctx.model.id,
      });
    },

    onSessionEnd: async (ctx) => {
      // 会话结束时输出成本摘要
      const totalCost = records.reduce((sum, r) => sum + r.cost, 0);
      const totalIn = records.reduce((sum, r) => sum + r.inputTokens, 0);
      const totalOut = records.reduce((sum, r) => sum + r.outputTokens, 0);

      ctx.tui.print(`
━━━━ 会话成本摘要 ━━━━
输入 Token：${totalIn.toLocaleString()}
输出 Token：${totalOut.toLocaleString()}
总估算成本：$${totalCost.toFixed(4)}
LLM 调用次数：${records.length}
━━━━━━━━━━━━━━━━━━━━━
      `);
    }
  },

  statusBarItems: [CostStatusItem],
};
```

---

## 四、Package 分发系统

扩展、Skills、模板、主题可以打包为 **Pi Package** 进行分发：

```bash
# 从 npm 安装
pi install npm:@company/pi-internal-tools
pi install npm:@foo/pi-review-skill

# 从 git 安装（开发中的扩展）
pi install git:github.com/user/pi-my-extension

# 锁定到特定版本
pi install npm:@foo/pi-tools@2.1.0

# 临时测试（不写入配置）
pi -e git:github.com/user/pi-experimental

# 管理
pi list         # 列出已安装的包
pi update       # 更新所有包
pi remove foo   # 卸载
pi config foo   # 配置包
```

### Package 的目录结构

```
my-pi-package/
├── package.json              # npm 包配置
├── pi.config.ts              # Pi 包声明
│   └── export default {
│       extensions: [MyExtension],
│       skills: ['./skills/my-skill.md'],
│       templates: ['./templates/'],
│       themes: [MyTheme],
│     }
├── extensions/
│   └── my-extension.ts       # TypeScript 扩展
├── skills/
│   └── my-skill.md           # Skill 定义（Markdown）
├── templates/
│   └── review.md             # Prompt 模板
└── themes/
    └── my-theme.ts           # 主题定义
```

---

## 五、五大概念的完整定义

| 概念 | 定义 | 加载时机 | 典型用途 |
|------|------|----------|---------|
| **Extension** | TypeScript 模块，注册工具/命令/钩子/TUI 组件 | 启动时加载 | 子代理、权限门控、RAG、MCP 适配 |
| **Skill** | Markdown 定义的指令 + 可选工具集 | 按需加载（渐进式披露） | Python 测试规范、数据库操作最佳实践 |
| **Prompt Template** | 可重用的 Markdown 提示词 | 用户触发时展开（`/template-name`） | 代码审查、文档生成、PR 描述 |
| **Theme** | 颜色方案 + 符号集 | 配置时加载 | UI 个性化 |
| **Package** | 以上任意内容的打包和分发单元 | 安装时注册 | 团队共享工具集 |

---

## 六、最有趣的设计循环：让 Pi 给自己写扩展

```
用户：帮我写一个 Pi 扩展，实现以下功能：
      1. 每次工具调用前记录到本地日志文件
      2. 每天生成一份使用报告
      3. 在状态栏显示今日调用次数

Pi：好的，我来实现这个扩展...

    [read] ~/.pi/extensions/       ← 了解现有扩展结构
    [write] tool-logger.ts         ← 编写扩展主体
    [write] tool-logger/           ← 创建包目录
      package.json
      pi.config.ts
    [bash] tsc --noEmit            ← 类型检查
    [bash] node tool-logger.test.ts ← 运行测试

    完成！运行以下命令安装：
    pi install ./tool-logger
```

这是 Pi「你自己的工具，完全由你掌控」哲学的极致体现：一个 AI 编程代理，用来扩展它自身的能力。

---

## 七、系列总结：Pi 对 Agent 工程的启示

经过六篇的系统剖析，Pi 带来的不只是一个工具，而是一套值得深思的工程观：

### 启示 1：最小 Harness，最大自由

减少框架内置的假设，增加工程师的控制权。**这不是功能残缺，而是边界清晰**。Terminal-Bench 的验证告诉我们，这不只是审美偏好，而是有实际性能收益的工程选择。

### 启示 2：严格分层是真正的可组合性

```
pi-ai → pi-agent-core → pi-coding-agent
```

每一层都能独立使用。你可以只用 `pi-ai` 做一个多 Provider LLM 客户端，完全不触碰其余部分。这种单向依赖不是偶然的，而是从设计之初就通过构建系统强制执行的。

### 启示 3：上下文工程比工具堆砌更重要

> 4 个工具 + < 1000 token 系统提示 = 比 20 个工具 + 8000 token 系统提示更好的性能

这个反直觉的结论，改变了很多人对「什么让 Agent 更强大」的理解。

### 启示 4：会话是资产，不是副产品

可序列化、可跨 Provider 迁移、可后处理的 JSONL 会话，使每一次 Agent 交互都变成可复用的知识资产。

### 启示 5：扩展性应该是架构级别的

不是「插件系统」作为事后的附加功能，而是整个框架从底层就为「别人来完成它」而设计。

---

## 八、延伸阅读

| 资源 | 链接 |
|------|------|
| Mario Zechner 原始博客 | `mariozechner.at/posts/2025-11-30-pi-coding-agent/` |
| pi-mono GitHub 仓库 | `github.com/badlogic/pi-mono` |
| OpenClaw 官网 | `openclaw.ai` |
| Nader Dabit 实践教程 | `nader.substack.com` |
| Pi 的 Claude Code 历史分析 | `mariozechner.at/posts/2025-08-03-cchistory/` |
| models.dev（模型目录）| `models.dev` |

---

*本系列完结。六篇文章覆盖了 Pi Agent 从哲学到每个核心组件的完整知识体系。*
*感谢 Mario Zechner 构建了这个「完全无法被 Google 搜索到」却改变了 Agent 工程讨论的工具。*
