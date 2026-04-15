# Pi Agent 深度解析（二）：`pi-ai` —— 四种协议统一 300+ 模型的 LLM 抽象艺术

> **系列导读**：本篇深入解析 Pi 的基础层 `pi-ai`，它是整个框架的"发动机"，负责抹平所有 LLM Provider 之间的差异，提供统一的通信接口。

---

## 一、问题：LLM API 碎片化的真实痛苦

每一家 LLM Provider 都有自己的 API 设计，即使是「OpenAI 兼容」的端点也各有脾气：

| Provider | 特殊怪癖 |
|----------|---------|
| Cerebras、xAI、Mistral | 不接受 `store` 字段 |
| Mistral、Chutes | 用 `max_tokens` 而非 `max_completion_tokens` |
| Cerebras、xAI | 不支持 `developer` 角色的系统消息 |
| Grok 系列 | 不接受 `reasoning_effort` 字段 |
| 各家推理模型 | reasoning 内容字段名各不相同（`reasoning_content` / `reasoning` / `thinking`） |
| **Google** | 截至目前**仍不支持工具调用流式传输**（这很 Google） |

如果你想在项目中同时支持 Anthropic、OpenAI、Google、Groq、Ollama，你就必须为每家写适配代码——或者用一个把所有不一致都藏起来的统一层。

---

## 二、Mario 的洞察：其实只有四种 Wire Protocol

面对这片混乱，Mario 识别出一个关键规律：

> **市面上几乎所有 LLM Provider，归根结底只实现了四种 Wire Protocol 之一。**

```
┌────────────────────────────────────────────────────────┐
│                  300+ LLM 模型                         │
├─────────────────┬──────────────┬───────────┬───────────┤
│ OpenAI          │ OpenAI       │ Anthropic │ Google    │
│ Completions API │ Responses API│ Messages  │ Gen AI API│
├─────────────────┴──────────────┴───────────┴───────────┤
│       pi-ai：四个适配器，统一覆盖所有 Provider           │
└────────────────────────────────────────────────────────┘
```

| 协议 | 代表 Provider |
|------|--------------|
| OpenAI Completions API | OpenAI、Groq、Mistral、Cerebras、xAI、Ollama、vLLM、LM Studio、llama.cpp、任意 OpenAI 兼容端点 |
| OpenAI Responses API | OpenAI（新版） |
| Anthropic Messages API | Anthropic、AWS Bedrock（Anthropic 模型） |
| Google Generative AI API | Google Gemini 全系列 |

`pi-ai` 只需要**四个适配器**，即可统一覆盖 300+ 模型。

---

## 三、统一 API 设计

### 3.1 模型注册表（Model Registry）

pi-ai 在构建时自动从 `models.dev` 和 OpenRouter 拉取数据，生成 `models.generated.ts`，包含 2000+ 模型的：

- Token 成本（input/output/cacheRead/cacheWrite）
- 能力标签（图片输入、thinking 支持、上下文窗口大小）
- Provider 映射和 API 路由

```typescript
import { getModel } from '@mariozechner/pi-ai';

// 从内置目录直接查找，完全类型安全
const claude  = getModel('anthropic', 'claude-sonnet-4-5');
const gpt     = getModel('openai',    'gpt-4o');
const gemini  = getModel('google',    'gemini-2.5-flash');
const llama   = getModel('groq',      'llama-3.3-70b-versatile');
const deepseek = getModel('openrouter', 'deepseek/deepseek-r1');
```

### 3.2 自定义 / 本地模型

对于不在目录中的模型（本地部署、新发布、私有端点）：

```typescript
import type { Model } from '@mariozechner/pi-ai';

// 本地 Ollama 模型
const ollamaModel: Model<'openai-completions'> = {
  id: 'llama-3.1-8b',
  name: 'Llama 3.1 8B (Ollama)',
  api: 'openai-completions',          // 路由到 OpenAI Completions 适配器
  provider: 'ollama',
  baseUrl: 'http://localhost:11434/v1',
  reasoning: false,
  input: ['text'],
  cost: { input: 0, output: 0, cacheRead: 0, cacheWrite: 0 },
  contextWindow: 128000,
  maxTokens: 32000
};

// vLLM 生产部署
const vllmModel: Model<'openai-completions'> = {
  id: 'qwen2.5-72b-instruct',
  name: 'Qwen2.5 72B (vLLM)',
  api: 'openai-completions',
  provider: 'custom',
  baseUrl: 'https://your-vllm-endpoint.com/v1',
  // ...
};
```

`api` 字段决定使用哪个适配器，与 `provider` 字段无关——这就是 Pi 能透明支持任意 OpenAI 兼容端点的原因。

---

## 四、核心能力深解

### 4.1 统一流式传输接口

每个 Provider 的流式格式完全不同，pi-ai 将其标准化为一套事件：

```typescript
import { getModel, streamSimple } from '@mariozechner/pi-ai';

const model = getModel('anthropic', 'claude-sonnet-4-5');
const stream = streamSimple(model, {
  systemPrompt: '你是一个专业的编程助手。',
  messages: [
    { role: 'user', content: '解释一下 TCP 三次握手', timestamp: Date.now() }
  ]
});

for await (const event of stream) {
  switch (event.type) {
    case 'text_delta':      // 文本增量（所有 Provider 统一）
      process.stdout.write(event.delta);
      break;
    case 'thinking_delta':  // 思维链增量（Claude/Gemini/o3 等推理模型）
      // 可选：显示思维过程
      break;
    case 'toolcall_delta':  // 工具调用参数增量（局部 JSON）
      // 可选：实时显示工具参数
      break;
    case 'done':
      console.log(`\n完成。总 Token：${event.message.usage.totalTokens}`);
      console.log(`停止原因：${event.message.stopReason}`); // 'stop' | 'toolUse' | 'length' | 'error' | 'aborted'
      break;
    case 'error':
      console.error(event.error.errorMessage);
      break;
  }
}

// 也可以直接 await 最终结果（跳过流式处理）
const finalMessage = await stream.result(); // AssistantMessage
```

**切换 Provider 只需改一行：**

```typescript
// 切换前
const model = getModel('anthropic', 'claude-sonnet-4-5');
// 切换后——其余代码完全不变
const model = getModel('openai', 'gpt-4o');
const model = getModel('google', 'gemini-2.5-pro');
const model = getModel('groq', 'llama-3.3-70b-versatile');
```

### 4.2 跨 Provider 上下文迁移（Context Handoff）⭐

这是 pi-ai **最独特**的能力，在其他任何统一 LLM API 中几乎找不到对应物。

**一个会话可以跨 Provider 无缝延续：**

```typescript
import { getModel, complete, type Context } from '@mariozechner/pi-ai';

const claude  = getModel('anthropic', 'claude-sonnet-4-5');
const gpt     = getModel('openai', 'gpt-4o');
const gemini  = getModel('google', 'gemini-2.5-flash');

// 初始化上下文
const context: Context = { messages: [] };

// 第一轮：用 Claude（开启思维链）
context.messages.push({ role: 'user', content: '25 × 18 等于多少？' });
const claudeResp = await complete(claude, context, { thinkingEnabled: true });
context.messages.push(claudeResp);
// claudeResp.content 包含 thinking 块和 text 块

// 第二轮：切换到 GPT（Claude 的 thinking 被转为 <thinking> 标签文本）
context.messages.push({ role: 'user', content: '这个答案正确吗？' });
const gptResp = await complete(gpt, context);
context.messages.push(gptResp);

// 第三轮：再切换到 Gemini
context.messages.push({ role: 'user', content: '总结一下我们的对话' });
const geminiResp = await complete(gemini, context);

// 序列化整个跨 Provider 会话
const saved = JSON.stringify(context);

// 随时反序列化并继续（用任意模型）
const restored: Context = JSON.parse(saved);
restored.messages.push({ role: 'user', content: '继续之前的话题' });
const continuation = await complete(claude, restored);
```

**实现挑战**：各 Provider 都会在事件流中插入**签名 blob**，切换模型时必须重放这些 blob。pi-ai 在后台维护了一套转换管道，将 Anthropic thinking traces 转为 `<thinking></thinking>` 标签，将 OpenAI reasoning 转为文本块，尽力保证跨 Provider 互操作性。

### 4.3 分离工具结果（Structured Split Tool Results）⭐

这是另一个在其他统一 LLM API 中罕见的设计。工具执行结果被明确分为**两个独立通道**：

```
工具执行结果
    │
    ├─► LLM 通道（output）：纯文本/JSON，发给模型，模型根据此决策
    │
    └─► UI 通道（details）：结构化数据/图片，用于界面显示，不发给模型
```

```typescript
import { Type, type AgentTool } from '@mariozechner/pi-ai';

const directoryTool: AgentTool = {
  name: 'list_files',
  description: '列出目录下的文件',
  parameters: Type.Object({
    path: Type.String({ description: '目录路径' })
  }),
  execute: async (toolCallId, args) => {
    const files = await fs.readdir(args.path);
    return {
      // LLM 看到的：简洁文本
      output: `目录 ${args.path} 包含 ${files.length} 个文件：${files.join(', ')}`,
      // UI 显示的：结构化数据（不占 LLM 的 token）
      details: {
        path: args.path,
        files: files.map(f => ({ name: f, isDir: fs.statSync(f).isDirectory() })),
        count: files.length
      }
    };
  }
};

// 工具也可以返回图片（自动适配各 Provider 的图片格式）
const screenshotTool: AgentTool = {
  name: 'take_screenshot',
  description: '截取当前屏幕',
  parameters: Type.Object({}),
  execute: async () => {
    const imageBuffer = await captureScreen();
    return {
      content: [
        { type: 'text', text: '截图完成，请分析图中内容' },
        { type: 'image', data: imageBuffer.toString('base64'), mimeType: 'image/png' }
      ]
    };
  }
};
```

### 4.4 流式局部 JSON 解析（Partial JSON Parsing）

当 LLM 流式输出工具调用参数时，pi-ai 会**逐步解析不完整的 JSON**：

```
流式输入（逐字到达）：         解析结果（实时可用）：
{"path": "/src/               → { path: '/src/' }（部分）
{"path": "/src/utils          → { path: '/src/utils' }（部分）
{"path": "/src/utils.ts",     → { path: '/src/utils.ts' }（完整）
{"path": "/src/utils.ts",     → { path: '/src/utils.ts',
 "content": "export           →   content: 'export' }（部分）
```

这使得 UI 可以在工具调用**完成之前**就开始展示正在编辑的文件路径、正在执行的命令等信息，大幅提升交互流畅感。

### 4.5 全链路 AbortSignal 支持

```typescript
const controller = new AbortController();

// 用户按 Ctrl+C 时触发
process.on('SIGINT', () => controller.abort());

const stream = streamSimple(model, context, {
  signal: controller.signal   // AbortSignal 贯穿整个调用链
});

for await (const event of stream) {
  if (event.type === 'error' && event.reason === 'aborted') {
    console.log('\n已中断');
  }
}

// 即使中断，也能获取已生成的部分内容
const result = await stream.result();
if (result.stopReason === 'aborted') {
  console.log('部分内容：', result.content);
}
```

AbortSignal 不只覆盖 LLM 调用，还会**传递给工具的 execute 函数**，让长时运行的工具也能响应中断。

### 4.6 Thinking / Reasoning 支持

```typescript
// 统一接口控制思维链深度
const stream = streamSimple(model, context, {
  reasoning: 'high'  // 'minimal' | 'low' | 'medium' | 'high' | 'xhigh'
});

// 对应各 Provider 的实现：
// Anthropic Claude：budget_tokens（预算 token 数）
// OpenAI o3/o4：reasoning_effort
// Google Gemini 2.5：thinkingConfig.thinkingBudget
// ——对用户透明，统一抽象
```

### 4.7 Token 与成本追踪

```typescript
const result = await stream.result();

console.log(result.usage);
// {
//   inputTokens: 1250,
//   outputTokens: 487,
//   cacheReadTokens: 800,   // Anthropic prompt caching
//   cacheWriteTokens: 200,
//   totalTokens: 1937,
//   estimatedCost: 0.00234  // USD，基于模型目录中的价格
// }
```

各 Provider 的 token 统计方式差异巨大（有的在流开头报告，有的在结尾）。pi-ai 采用**尽力而为（best-effort）**策略，对个人使用足够准确，但不适用于精确计费场景。

---

## 五、浏览器端支持

pi-ai 同样适用于**浏览器环境**：

```typescript
// 在浏览器中直接调用（无需后端代理）
// Anthropic 和 xAI 支持 CORS
import { getModel, streamSimple } from '@mariozechner/pi-ai';

const model = getModel('anthropic', 'claude-haiku-4-5');
const stream = streamSimple(model, context, {
  apiKey: import.meta.env.VITE_ANTHROPIC_KEY  // 浏览器端传递
});
```

这使得基于 pi-ai 的全前端 Agent Web UI 成为可能（配合 `pi-web-ui` 包）。

---

## 六、架构小结

```
用户代码
    │
    ▼
getModel()          ← 从 2000+ 模型目录解析，返回类型安全的 Model 对象
    │
    ▼
streamSimple() / completeSimple()   ← 统一调用入口
    │
    ▼
Router（根据 model.api 字段路由）
    │
    ├─► openai-completions-adapter.ts   ← 处理 Cerebras/xAI/Mistral 等各家差异
    ├─► openai-responses-adapter.ts
    ├─► anthropic-adapter.ts
    └─► google-adapter.ts
    │
    ▼
标准化事件流（text_delta / thinking_delta / toolcall_delta / done / error）
    │
    ▼
pi-agent-core / 用户代码
```

**pi-ai 的设计价值**：写一次调用代码，覆盖所有 Provider；切换模型，一行代码；迁移会话，完全无损。

---

*下一篇：`pi-agent-core` —— Agent 循环的最简实现与事件驱动设计*
