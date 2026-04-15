# Pi Agent 深度解析（三）：`pi-agent-core` —— Agent 循环的最简实现与事件驱动设计

> **系列导读**：如果说 `pi-ai` 是发动机，`pi-agent-core` 就是传动系统。它将一次性的 LLM 调用组装成能持续运转的 Agent 循环，同时通过事件系统驱动任意上层 UI。

---

## 一、什么是 Agent 循环？

Agent 循环（Agent Loop）是所有 AI Agent 的核心心跳。用伪代码表示极为简单：

```
while (true):
    response = LLM(messages + tools_definition)

    if response.stopReason == "stop":
        # LLM 认为任务完成，直接输出文本
        break

    if response.stopReason == "toolUse":
        # LLM 请求调用工具
        tool_results = execute_tools(response.toolCalls)
        messages.append(tool_results)
        # 继续循环，让 LLM 基于工具结果继续推理
```

魔鬼在细节里：
- 工具执行**失败**时怎么处理？
- 工具参数**不合法**时怎么反馈给 LLM？
- 工具执行中如何向 UI **实时推送进度**？
- 用户在执行过程中**发出新指令**怎么处理？
- 如何**中断**一个正在运行的 Agent？

`pi-agent-core` 就是解答这些问题的最小实现。

---

## 二、核心数据结构

### 2.1 AgentTool —— 工具的完整定义

```typescript
import { Type } from '@mariozechner/pi-ai';
import type { AgentTool } from '@mariozechner/pi-agent-core';

// 工具参数的 TypeBox schema（编译期类型安全 + 运行时验证）
const bashParams = Type.Object({
  command: Type.String({ description: 'Shell 命令' }),
  workingDir: Type.Optional(Type.String({ description: '工作目录' })),
});

const bashTool: AgentTool<typeof bashParams> = {
  name: 'bash',
  label: '执行命令',            // UI 显示名称
  description: '执行 Shell 命令并返回输出。用于运行代码、管理文件、调用工具等。',

  parameters: bashParams,       // TypeBox schema

  execute: async (
    toolCallId: string,         // 唯一标识此次工具调用
    params,                     // 强类型：{ command: string; workingDir?: string }
    signal: AbortSignal,        // 响应中断请求
    onUpdate: (data) => void    // 推送流式进度（如命令实时输出）
  ) => {
    const proc = spawn('bash', ['-c', params.command], {
      cwd: params.workingDir,
    });

    let stdout = '';
    proc.stdout.on('data', (chunk) => {
      stdout += chunk;
      // 实时推送到 UI（不等待命令完成）
      onUpdate({ type: 'partial_output', content: chunk.toString() });
    });

    // 响应 AbortSignal
    signal.addEventListener('abort', () => proc.kill());

    await new Promise<void>((resolve) => proc.on('close', resolve));

    return {
      // LLM 看到的（影响后续推理）
      output: stdout || '（无输出）',
      // UI 看到的（结构化，不占 LLM token）
      details: { exitCode: proc.exitCode, stdout, stderr }
    };
  }
};
```

**四个参数设计的用意：**

| 参数 | 类型 | 用途 |
|------|------|------|
| `toolCallId` | string | 唯一标识，用于关联调用和结果 |
| `params` | 强类型对象 | 工具实际接受的参数（已验证） |
| `signal` | AbortSignal | 响应 Ctrl+C / 超时中断 |
| `onUpdate` | callback | 流式推送进度（bash 实时输出、文件写入进度等） |

### 2.2 AgentSession —— Agent 的运行时

```typescript
import { createAgentSession } from '@mariozechner/pi-agent-core';
import { getModel } from '@mariozechner/pi-ai';

const session = createAgentSession({
  model: getModel('anthropic', 'claude-sonnet-4-5'),
  systemPrompt: `你是一个专业的 TypeScript 编程助手。
在回答问题之前先阅读相关文件，确保修改不会破坏现有功能。`,
  tools: [readTool, writeTool, editTool, bashTool],
  contextFiles: [
    '~/.pi/AGENTS.md',   // 全局 Agent 指令
    './AGENTS.md',        // 项目级指令（如存在）
  ],
  reasoning: 'medium',   // 开启思维链（可选）
});
```

---

## 三、事件驱动模型

这是 pi-agent-core 最重要的设计决策：**所有状态变化都通过事件通知，而不是返回值**。

```typescript
// 注册事件监听器
session.subscribe((event) => {
  switch (event.type) {

    // ── LLM 响应阶段 ──────────────────────────────────────
    case 'message_start':
      console.log('开始生成...');
      break;

    case 'text_delta':
      process.stdout.write(event.delta);  // 流式文本输出
      break;

    case 'thinking_delta':
      // Claude/Gemini 的思维链内容（可选展示）
      break;

    // ── 工具调用阶段 ──────────────────────────────────────
    case 'tool_call_start':
      console.log(`\n[工具] ${event.toolName}（${event.toolCallId}）`);
      break;

    case 'tool_call_delta':
      // 工具参数的局部 JSON（实时显示正在编辑的文件路径等）
      break;

    case 'tool_call_end':
      console.log(`参数确定：`, event.args);
      break;

    case 'tool_result':
      // 工具执行完成
      console.log(`结果：`, event.output);     // LLM 通道
      console.log(`详情：`, event.details);    // UI 通道（结构化数据）
      break;

    case 'tool_update':
      // onUpdate() 推送的流式进度（如 bash 实时输出）
      process.stdout.write(event.data.content);
      break;

    // ── 生命周期 ──────────────────────────────────────────
    case 'message_end':
      console.log('\n本轮生成完成');
      break;

    case 'session_end':
      console.log('Agent 循环结束');
      break;

    case 'error':
      console.error('错误：', event.error);
      break;
  }
});

// 触发 Agent 循环
await session.prompt('帮我为 src/utils/sort.ts 写单元测试');
```

**事件模型的核心价值**：相同的 Agent 核心可以驱动**完全不同的 UI**：

```
AgentSession（pi-agent-core）
    │
    ├── pi-tui（终端 UI）   ← 事件 → 差分渲染终端输出
    ├── pi-web-ui（Web UI）  ← 事件 → 更新 React 组件
    ├── OpenClaw（IM 平台）  ← 事件 → 发送 Telegram/Discord 消息
    └── 测试框架             ← 事件 → 断言验证、录制回放
```

---

## 四、完整循环生命周期

```
用户调用 session.prompt("任务描述")
         │
         ▼
┌────────────────────────────────────────────────────────┐
│                    构建请求上下文                       │
│  系统提示 + 上下文文件内容 + 历史消息 + 工具定义 schema │
└────────────────────────────────┬───────────────────────┘
                                 │
                                 ▼
                    调用 LLM（流式）
                    emit: message_start
                    emit: text_delta（逐字）
                    emit: thinking_delta（推理模型）
                    emit: tool_call_delta（工具参数流）
                                 │
              ┌──────────────────┴──────────────────┐
              │                                     │
    stopReason = "stop"              stopReason = "toolUse"
              │                                     │
              ▼                                     ▼
    emit: message_end           解析所有工具调用请求
    emit: session_end                    │
    循环结束 ✓                           ▼
                             ┌────────────────────────┐
                             │   工具参数验证（AJV）   │
                             └────────────┬───────────┘
                                          │
                             ┌────────────┴───────────┐
                             │ 验证失败                │ 验证成功
                             ▼                        ▼
                   生成详细错误信息          并行执行所有工具
                   反馈给 LLM              emit: tool_call_start
                   LLM 修正并重试          emit: tool_update（流式）
                                          emit: tool_result
                                                    │
                                                    ▼
                                       将工具结果追加到 messages
                                                    │
                                                    ▼
                                           再次调用 LLM
                                         （继续 while 循环）
```

---

## 五、工具参数验证机制

工具验证在工具**执行之前**发生，使用 **AJV** 根据 TypeBox schema 进行校验：

```typescript
// 假设 LLM 生成了错误的参数
const badArgs = { command: 123 }  // 应该是 string

// AJV 验证失败，生成详细错误消息
const error = `工具调用参数验证失败（bash）：
  - command: 期望 string，收到 number (123)

请使用正确的参数重新调用工具。`;

// 错误消息被作为 tool_result 发回给 LLM
// LLM 读到后会修正参数并重试
```

这比直接抛出异常崩溃要友好得多——LLM 有机会**自我修正**。

---

## 六、消息队列与并发交互

用户在 Agent 执行过程中发出的新消息会被**队列化**而不是丢弃：

```
时间轴：
t=0   用户发送 "帮我优化这段代码"
t=0   Agent 开始调用 read 工具读取文件...
t=2   用户发送 "等一下，先看看 test 目录"   ← 进入队列
t=4   read 工具执行完成
t=4   [LLM 调用前] 队列中的消息被注入
t=4   Agent 调整方向，先看 test 目录
```

队列中的消息分两种模式：

| 模式 | 注入时机 | 用途 |
|------|----------|------|
| **转向消息**（steering） | 下次 LLM 调用之前 | 在 Agent 运行过程中调整方向 |
| **跟进消息**（follow-up） | 整个 session_end 之后 | 等当前任务完成后再追加新任务 |

```typescript
// 转向消息（打断当前推理方向）
session.prompt('不对，先处理 main.ts 里的 bug', { mode: 'steering' });

// 跟进消息（等当前任务完成后执行）
session.prompt('完成后运行所有测试', { mode: 'follow-up' });
```

---

## 七、会话持久化与恢复

```typescript
// 序列化整个会话状态
const snapshot = session.serialize();
await fs.writeFile('./session.json', JSON.stringify(snapshot));

// 在新的 Node.js 进程中恢复
const saved = JSON.parse(await fs.readFile('./session.json', 'utf8'));
const restored = restoreAgentSession(saved, {
  model: getModel('anthropic', 'claude-sonnet-4-5'),
  tools: [readTool, writeTool, editTool, bashTool],
});

// 继续之前的对话，完整历史记录保留
await restored.prompt('继续之前未完成的重构工作');
```

---

## 八、pi-ai 与 pi-agent-core 的职责边界

| 职责 | pi-ai | pi-agent-core |
|------|:-----:|:------------:|
| LLM Provider 通信 | ✅ | ❌ |
| 流式事件标准化 | ✅ | ❌ |
| 多 Provider 抽象 | ✅ | ❌ |
| 工具 Schema 定义（TypeBox） | ✅ | ❌ |
| 工具参数验证（AJV） | ❌ | ✅ |
| 工具执行调度 | ❌ | ✅ |
| 多轮循环编排 | ❌ | ✅ |
| 消息队列管理 | ❌ | ✅ |
| 事件派发（subscribe/emit） | ❌ | ✅ |
| 会话状态管理 | ❌ | ✅ |
| 上层 UI 驱动 | ❌ | ✅ |

---

## 九、设计选择的反思

**为什么不内置 max_steps 限制？**

> "我从未发现 max_steps 这类限制有用。Agent 要么完成任务，要么卡住了——如果卡住了，max_steps 无法修复它，只会在错误的地方截断执行。" — Mario Zechner

**为什么不内置重试逻辑？**

因为重试策略高度依赖具体场景：对某些工具失败，你可能想立即重试；对另一些，你可能想先通知用户。通用的重试逻辑往往适得其反。

**为什么用事件而不是 async generator？**

事件模型允许**多个订阅者同时接收同一个事件**（如同时驱动终端 UI 和日志系统），而 async generator 是单消费者模型。

---

*下一篇：`pi-coding-agent` —— 极简系统提示、四工具理念与 YOLO 模式*
