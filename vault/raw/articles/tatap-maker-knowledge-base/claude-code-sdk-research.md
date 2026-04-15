# Claude Code SDK：基于会话持久化的 AI Agent 开发框架

Claude Code SDK 是 Anthropic 官方提供的 TypeScript/JavaScript Agent 开发工具包，用于构建具有工具调用、文件操作和长期对话能力的 AI 助手。该 SDK 的核心优势在于其**会话持久化架构**和**多轮对话上下文保持**能力，通过 `continue` 和 `resume` 选项实现真正的长期记忆。与一次性的 API 调用不同，Claude Code SDK 管理完整的对话生命周期，包括工具权限控制、状态追踪和会话恢复，使其成为构建交互式编程助手、代码生成工具和协作开发环境的理想选择。

## 核心架构：会话持久化与上下文保持

### 1. 会话生命周期管理

Claude Code SDK 通过 `query()` 函数创建和管理对话会话，每个会话都有独立的上下文和状态：

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

// 创建新会话（首次对话）
const result = query({
  prompt: "List files in current directory",
  options: {
    cwd: "/path/to/project",
    permissionMode: "default",
  },
});

// 迭代处理响应
for await (const message of result) {
  console.log(message.type, message.data);
}
```

### 2. 多轮对话：continue 选项

**关键特性**：`continue: true` 选项允许在同一会话中发送新的 prompt，Claude 会记住之前的所有对话内容：

```typescript
// 第一轮对话
const firstQuery = query({
  prompt: "Create a file called hello.txt with 'Hello World'",
  options: { cwd: "/workspace" },
});

for await (const msg of firstQuery) {
  // 处理第一轮响应
}

// 第二轮对话 - 使用 continue: true
const secondQuery = query({
  prompt: "What file did you just create?", // Claude 会记住第一轮的内容！
  options: {
    cwd: "/workspace",
    continue: true, // ✨ 继续之前的会话
  },
});

for await (const msg of secondQuery) {
  // Claude 回答："I created hello.txt"
}
```

**工作原理**：

- 首次调用 `query()` 创建新的 SDK session（内部生成 session ID）
- 使用 `continue: true` 的后续调用会继续同一个 session
- Claude 的上下文包含之前所有的消息、工具调用和响应
- 工作目录（cwd）和权限设置保持一致

### 3. 会话恢复：resume 选项

`resume` 选项允许通过 session ID 恢复之前的会话，即使进程重启也能继续对话：

```typescript
// 恢复特定会话
const resumedQuery = query({
  prompt: "Continue the previous task",
  options: {
    resume: "session-abc123", // 指定要恢复的 session ID
    cwd: "/workspace",
  },
});

// 从特定消息点恢复
const partialResume = query({
  prompt: "Let's try a different approach",
  options: {
    resume: "session-abc123",
    resumeSessionAt: "msg-456", // 只恢复到这条消息为止
  },
});
```

**使用场景**：

- 进程重启后恢复对话
- 多个客户端连接到同一会话
- 从历史对话分支（fork）新的方向

### 4. 会话分支：forkSession 选项

`forkSession: true` 允许从现有会话创建新分支，保留历史上下文但使用新的 session ID：

```typescript
const forkedQuery = query({
  prompt: "Try an alternative implementation",
  options: {
    resume: "session-abc123",
    forkSession: true, // 创建新分支，不修改原会话
  },
});
```

**对比**：

- `resume` without `forkSession`：继续原会话，新消息追加到原 session
- `resume` with `forkSession: true`：创建新会话，但包含原会话的历史上下文

## 工具调用与权限控制

### 1. 内置工具系统

SDK 提供一系列文件操作和代码分析工具：

- **Read**：读取文件内容
- **Write**：写入文件
- **Edit**：编辑现有文件
- **Bash**：执行 shell 命令
- **Glob**：文件模式匹配
- **Grep**：代码搜索
- **NotebookEdit**：Jupyter notebook 编辑

### 2. 权限模式控制

```typescript
const result = query({
  prompt: "Analyze the codebase",
  options: {
    permissionMode: "default", // 或 'always-allow', 'always-deny'
    canUseTool: async (toolName, input, options) => {
      // 自定义权限逻辑
      if (toolName === "Write") {
        // 请求用户批准
        const approved = await askUserPermission(toolName, input);
        return {
          behavior: approved ? "allow" : "deny",
          updatedInput: input,
        };
      }
      return { behavior: "allow", updatedInput: input };
    },
  },
});
```

**权限结果类型**：

```typescript
interface PermissionResult {
  behavior: "allow" | "deny";
  updatedInput?: Record<string, unknown>; // 可修改工具参数
  updatedPermissions?: any[]; // 更新权限规则
  message?: string; // 拒绝原因
  interrupt?: boolean; // 是否中断会话
}
```

### 3. 工具调用生命周期

```typescript
// 1. Claude 请求工具调用
// 2. SDK 触发 canUseTool 回调
// 3. 应用程序批准/拒绝
// 4. SDK 执行工具或返回拒绝消息
// 5. 结果传回 Claude 上下文
```

## 消息流与事件处理

### 1. 消息类型

SDK 通过 AsyncIterator 流式返回不同类型的消息：

```typescript
for await (const message of query({ prompt: "..." })) {
  switch (message.type) {
    case "session_start":
      // 会话开始，包含 model、cwd、tools 信息
      break;
    case "assistant_text":
      // Claude 的文本回复
      console.log(message.text);
      break;
    case "tool_call":
      // Claude 请求调用工具
      console.log(message.toolName, message.input);
      break;
    case "tool_result":
      // 工具执行结果
      break;
    case "session_end":
      // 会话结束，包含 reason、usage、cost
      break;
  }
}
```

### 2. Hook 系统与 Session ID 获取

**重要发现**：SDK 的 hook 系统存在架构限制，JavaScript 函数形式的 hooks **不会被触发**。

> **调查版本**：`@anthropic-ai/claude-agent-sdk` v0.1.14 → v0.1.21（已验证）
>
> 本调查最初基于 v0.1.14 进行，结论已在 v0.1.21 中重新验证，行为保持一致。

#### Hook 系统的设计与限制

SDK 类型定义中包含 `HookCallback` 函数类型：

```typescript
// SDK 类型定义（node_modules/@anthropic-ai/claude-agent-sdk/sdkTypes.d.ts）
export type HookCallback = (
  input: HookInput,
  toolUseID: string | undefined,
  options: { signal: AbortSignal },
) => Promise<HookJSONOutput>;

interface HookCallbackMatcher {
  matcher?: string;
  hooks: HookCallback[];
}

// Options 中的 hooks 字段
hooks?: Partial<Record<HookEvent, HookCallbackMatcher[]>>;
```

**但是**，根据深入调查（2025-10-17，参考 `server/tests/debug/HOOK_INVESTIGATION_REPORT.md`）：

1. **官方文档明确说明**：[Claude Code Hooks Guide](https://docs.claude.com/en/docs/claude-code/hooks-guide) 指出 hooks 是**用户定义的 shell 命令**，不是 JavaScript 函数
2. **架构限制**：SDK 和 CLI subprocess 之间的通信架构导致 JavaScript hooks 无法工作

   ```
   ┌─────────────────┐         ┌─────────────────┐
   │   Your Code     │         │  Claude Code    │
   │   (Node.js)     │ ◄────► │      CLI        │
   │                 │         │   (subprocess)  │
   │  SDK Functions  │  stdio  │                 │
   │  - hooks: {...} │         │  Only supports  │
   │                 │         │  shell commands │
   └─────────────────┘         └─────────────────┘
   ```

3. **测试验证**：多种配置均失败（SessionStart、PreToolUse、PostToolUse），hook 回调从未被触发
4. **根因**：CLI subprocess 不会发送 `hook_callback` 请求给 SDK，JavaScript 函数永远不会被调用

#### 获取 Session ID 的正确方法

由于 hooks 不可用，推荐通过**消息流**获取 session_id：

```typescript
// 所有 SDK 消息都包含 session_id
for await (const message of query({ prompt: "..." })) {
  // 第一条消息（type="system"）总是包含 session_id
  if (message.session_id) {
    console.log("Session ID:", message.session_id);
    // 保存 session_id 用于后续 resume
    conversation.sdkSessionId = message.session_id;
  }
}
```

**工作原理**：

- SDK 类型定义中，所有消息类型都继承自 `SDKMessageBase`：

  ```typescript
  export type SDKMessageBase = {
    uuid: UUID;
    session_id: string; // ← 每条消息都包含
  };
  ```

- 第一条消息（`type="system"`）总是包含 session_id
- 测试验证：100% 可靠，所有测试中第一条消息都包含有效的 session_id

**可用的 Hook 事件类型**（仅供类型参考，实际不工作）：

- `SessionStart` (source: 'startup' | 'resume' | 'clear' | 'compact')
- `SessionEnd` (reason: 'clear' | 'logout' | 'prompt_input_exit' | 'other')
- `PreToolUse`
- `PostToolUse`
- `Notification`
- `UserPromptSubmit`
- `Stop`
- `SubagentStop`
- `PreCompact`

### 3. 中断机制

```typescript
const result = query({ prompt: "..." }) as QueryIteratorWithInterrupt;

// 优雅中断会话
await result.interrupt();
```

## 配置选项详解

### 基础配置

```typescript
interface Options {
  // 工作目录
  cwd?: string;

  // 环境变量
  env?: Record<string, string>;

  // 运行时选择
  executable?: "bun" | "deno" | "node";
  executableArgs?: string[];

  // 模型配置
  fallbackModel?: string;

  // 系统提示
  customSystemPrompt?: string;
  appendSystemPrompt?: string;
}
```

### 工具控制

```typescript
interface Options {
  // 工具白名单
  allowedTools?: string[];

  // 工具黑名单
  disallowedTools?: string[];

  // 额外目录访问
  additionalDirectories?: string[];
}
```

### 会话控制

```typescript
interface Options {
  // 继续最近会话
  continue?: boolean;

  // 恢复特定会话
  resume?: string;

  // 分支会话
  forkSession?: boolean;

  // 部分恢复到特定消息
  resumeSessionAt?: string;

  // 最大对话轮数
  maxTurns?: number;

  // 中止控制器
  abortController?: AbortController;
}
```

## 在 TapTap Maker 中的应用

### 1. 三层架构集成

```typescript
// Workspace → Conversation → Session

interface Conversation {
  conversationId: string; // 应用层 conversation ID
  workspaceId: string; // 项目/工作空间 ID
  sdkSessionId?: string; // SDK session ID（用于 resume）
  query: QueryIterator;
  status: "active" | "sleeping" | "terminated";
}
```

### 2. 多轮对话与 Session ID 捕获

```typescript
class ConversationManager {
  async createConversation(conversationId: string, workspaceId: string, prompt: string) {
    const project = this.projectManager.getProject(workspaceId);

    const result = query({
      prompt,
      options: {
        cwd: project.path,
        permissionMode: "default",
        canUseTool: async (toolName, input, options) => {
          return await this.handlePermissionRequest(conversationId, toolName, input);
        },
      },
    });

    this.conversations.set(conversationId, {
      conversationId,
      workspaceId,
      query: result,
      status: "active",
    });

    this.forwardMessages(result);
  }

  async sendPrompt(conversationId: string, prompt: string) {
    const conversation = this.conversations.get(conversationId);

    // 使用 continue: true 保持上下文
    const result = query({
      prompt,
      options: {
        cwd: conversation.project.path,
        continue: true, // ✨ Claude 记住之前的对话！
        canUseTool: async (toolName, input, options) => {
          return await this.handlePermissionRequest(conversationId, toolName, input);
        },
      },
    });

    conversation.query = result;
    this.forwardMessages(result);
  }

  // 消息转发 + Session ID 捕获
  private async forwardMessages(conversation: Conversation) {
    let messageCount = 0;

    for await (const message of conversation.query) {
      messageCount++;

      // 从第一条消息中捕获 session_id（用于跨进程恢复）
      if (messageCount === 1 && message.session_id) {
        // 保存到内存
        conversation.sdkSessionId = message.session_id;

        // 持久化到数据库
        try {
          this.db.updateConversationSessionId(conversation.conversationId, message.session_id);
        } catch (error) {
          console.error(`[Conversation] Failed to save session ID:`, error);
          // 继续执行 - 内存中的状态已保存
        }
      }

      // 转换并发送消息到客户端
      const browserMessage = this.messageTransformer.transform(
        message,
        conversation.conversationId,
      );
      this.sendMessage(conversation.conversationId, browserMessage.type, browserMessage);

      // 更新活动时间
      conversation.lastActivity = Date.now();
    }
  }

  // 跨进程恢复：使用 resume
  private async recreateConversationFromDB(conversationId: string, prompt: string) {
    const dbConv = this.db.getConversation(conversationId);
    const savedSessionId = dbConv.sdk_session_id;

    const result = query({
      prompt,
      options: {
        cwd: dbConv.workspace_path,
        // 如果有 session_id，使用 resume；否则使用 continue
        ...(savedSessionId ? { resume: savedSessionId } : { continue: true }),
        canUseTool: async (toolName, input, options) => {
          return await this.handlePermissionRequest(conversationId, toolName, input);
        },
      },
    });

    const conversation = {
      conversationId,
      workspaceId: dbConv.workspace_id,
      query: result,
      status: "active" as const,
    };

    this.conversations.set(conversationId, conversation);
    this.forwardMessages(conversation);
  }
}
```

### 3. 权限控制集成

```typescript
async handlePermissionRequest(
  conversationId: string,
  toolName: string,
  input: Record<string, unknown>
): Promise<PermissionResult> {
  // 路径验证
  if (fileTools.includes(toolName)) {
    const isValid = this.validateProjectPath(input.file_path);
    if (!isValid) {
      return {
        behavior: 'deny',
        message: 'Path outside project directory',
        interrupt: false,
      };
    }
  }

  // 发送权限请求到前端
  this.sendMessage(conversationId, 'permission_request', {
    toolName,
    input,
  });

  // 等待用户决策
  const decision = await this.permissionQueue.waitForDecision();

  return {
    behavior: decision.allow ? 'allow' : 'deny',
    updatedInput: input,
  };
}
```

## 性能与最佳实践

### 1. 会话生命周期管理

**建议**：

- 首次对话：创建新会话（不使用 `continue` 或 `resume`）
- 后续对话：使用 `continue: true`
- 长时间不活动：保存 `sdkSessionId`，下次使用 `resume` 恢复
- 30 分钟超时：自动清理内存中的 query iterator，但保留数据库记录

**实现**：

```typescript
// 超时检查器
setInterval(
  () => {
    for (const [id, conv] of this.conversations.entries()) {
      if (Date.now() - conv.lastActivity > 30 * 60 * 1000) {
        conv.status = "sleeping";
        conv.query = null; // 释放内存
        // sdkSessionId 仍保留在数据库中，可用于 resume
      }
    }
  },
  5 * 60 * 1000,
);
```

### 2. 消息持久化

**策略**：

```typescript
// 1. 消息先持久化到数据库
const msgId = db.createMessage(conversationId, type, data);

// 2. 再通过 SSE 发送到客户端
if (streamConnected) {
  stream.write({ id: msgId, type, data });
  db.markMessageDelivered(msgId);
} else {
  // 客户端离线，消息已在数据库中，重连时发送
}
```

### 3. 多客户端支持

**设计**：

- 一个 Conversation = 一个 SDK session
- 多个 SSE connections（不同浏览器标签页）
- 消息广播到所有连接的客户端

```typescript
class ConversationManager {
  private activeStreams = new Map<string, Set<StreamWriter>>();

  sendMessage(conversationId: string, type: string, data: any) {
    const msgId = this.db.createMessage(conversationId, type, data);

    const streams = this.activeStreams.get(conversationId);
    if (streams) {
      for (const stream of streams) {
        stream.write({ id: msgId, type, data });
      }
      this.db.markMessageDelivered(msgId);
    }
  }
}
```

## 局限性与未来改进

### 当前局限

1. **上下文窗口限制**：长对话会消耗 token，最终达到模型上下文限制
2. **会话存储**：SDK session 数据存储在 Claude Code 内部，应用层无法直接访问
3. **跨进程恢复**：`resume` 依赖本地 session 数据，无法跨机器恢复

### 改进方向

1. **会话压缩**：定期压缩长对话，保留关键信息
2. **显式 session ID 暴露**：SDK 返回 session ID 供应用层存储
3. **云端会话同步**：将 session 状态同步到云端，支持跨设备恢复

## 与其他 AI SDK 对比

### vs. LangChain

**LangChain**：

- 专注于 chain 和 agent 抽象
- 支持多种 LLM 提供商
- 需要手动管理对话历史

**Claude Code SDK**：

- 专为 Claude 优化
- 内置会话持久化（`continue`/`resume`）
- 自动管理对话上下文

### vs. OpenAI Assistants API

**OpenAI Assistants**：

- 云端管理 thread 和 message
- 内置文件存储和 code interpreter
- 需要轮询获取结果

**Claude Code SDK**：

- 本地运行，完全控制
- 流式响应（AsyncIterator）
- 直接文件系统访问

## 结论

Claude Code SDK 通过 `continue` 和 `resume` 选项实现了真正的长期对话能力，使其区别于传统的一次性 API 调用。对于构建交互式编程助手和代码生成工具，这种会话持久化架构提供了：

1. **上下文保持**：Claude 记住整个对话历史
2. **工具链连续性**：工具调用结果成为后续对话的上下文
3. **灵活的会话控制**：通过 `resume`、`forkSession` 实现复杂的会话管理

在 TapTap Maker 项目中，我们利用这些能力构建了三层架构（Workspace → Conversation → Session），实现了多项目隔离、多轮对话和多客户端同步，为用户提供流畅的 AI 编程助手体验。
