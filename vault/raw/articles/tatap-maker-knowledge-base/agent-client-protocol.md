# Agent Client Protocol：Zed 的 AI 编码代理开放标准

**ACP 是由 Zed Industries 创建的开源通信协议，旨在标准化代码编辑器与 AI 编码代理之间的交互方式。** 类似于用于语言工具的 Language Server Protocol (LSP)，ACP 通过使任何编辑器能够通过单一接口与任何代理协作，解决了 AI 编码助手的碎片化问题。重要的是，ACP 是由 Zed 开发的——而非 Anthropic——尽管它与 Anthropic 的 Claude Code 和 Model Context Protocol (MCP) 无缝集成。

该协议消除了供应商锁定，允许开发者独立选择他们偏好的编辑器和 AI 代理。通过将代理作为本地子进程运行，并通过 stdin/stdout 上的 JSON-RPC 进行通信，ACP 确保代码保持私密，同时提供生产级功能，如实时流式传输、多文件差异可视化和细粒度权限控制。截至 2025 年 1 月，JetBrains 承诺在其整个 IDE 阵容中共同开发 ACP，为其成为新兴标准提供了重要动力。

## 澄清协议格局

一个关键的混淆点：**并不存在"Anthropic Computer Protocol"。** 三个具有相似名称的不同协议在 AI 生态系统中服务于互补目的：

**Anthropic 的 MCP (Model Context Protocol)** 将 AI 模型连接到数据源和工具——这是 Claude 访问你的 Google Drive、数据库或 API 的方式。MCP 于 2024 年 11 月发布，已被 OpenAI、Google DeepMind 和主要开发工具迅速采用。它定义了三种原语：工具（模型控制）、资源（应用程序控制）和提示（用户控制）。

**Zed 的 ACP (Agent Client Protocol)** 将代码编辑器连接到 AI 代理——这是你如何在 Zed、Neovim 或 JetBrains IDE 中通过一个标准接口使用 Claude Code、Gemini CLI 或 Goose。ACP 于 2025 年 8 月推出，故意重用 MCP 数据类型以实现互操作性，但服务于根本不同的架构层。

**IBM 的 ACP (Agent Communication Protocol)** 在分布式多代理系统中实现代理之间的协作。为 IBM 的 BeeAI 项目开发并目前处于 alpha 阶段，这个基于 REST 的协议处理自主代理之间的任务委派和协商。

这些协议**互补而非竞争**。一个最佳的 AI 编码设置可能使用所有三个：MCP 让代理访问工具和数据，Zed 的 ACP 让你在任何编辑器中使用任何代理，而 IBM 的 ACP 协调多代理工作流。当你看到"Zed ACP Anthropic"时，这指的是 Zed 使用他们的协议来集成 Anthropic 的 Claude Code——这是一个 Zed 倡议使用 Zed 协议，而非 Anthropic 的创造。

## ACP 的架构工作原理

ACP 实现了一种**基于子进程的架构**，其中代理作为编辑器的子进程运行，通过 stdin/stdout 上的 JSON-RPC 2.0 消息进行通信。这种设计提供了强大的安全边界，同时支持丰富的实时交互。

**协议流程**遵循清晰的生命周期。初始化通过 `initialize` 请求建立连接，编辑器宣告其能力（文件系统访问、终端支持、MCP 服务器端点），代理响应其支持的功能（会话加载、流式传输、工具执行）。版本协商在此阶段进行——如果版本不兼容，连接将干净地终止。如果代理需要，可选的身份验证随后进行，完全由代理本身处理；Zed 永远看不到身份验证令牌。

会话管理是 ACP 设计的核心。编辑器使用 `session/new` 创建新会话，或者如果代理宣告此能力，则通过 `session/load` 加载现有会话。每个会话在多个提示 - 响应周期中维护对话上下文。当用户通过 `session/prompt` 提交提示时，代理处理它并通过 `session/update` 通知流式返回响应，包含代理消息块、工具调用通知和进度指示器。编辑器实时渲染这些更新，准确显示代理正在做什么。用户可以随时使用 `session/cancel` 中断处理。

**工具执行**是双向流动的。代理请求操作（读取文件、写入文件、执行终端命令），编辑器根据配置的策略直接执行或提示用户许可。对于文件操作，**所有路径必须是绝对路径**——协议规范明确禁止相对路径。编辑器用操作结果响应，代理将其纳入响应生成中。

**架构图**展示了完整的系统：

```
┌─────────────────────────────────────────────────────────┐
│                    代码编辑器 (Zed/Neovim)              │
│  UI 层：代理面板、多缓冲区差异、TODO 侧边栏            │
│  权限系统：调解所有文件/终端访问                        │
└─────────────────────┬───────────────────────────────────┘
                      │ JSON-RPC 2.0 通过 stdin/stdout
┌─────────────────────▼───────────────────────────────────┐
│              代理进程 (Claude Code/Gemini CLI)          │
│  ClaudeAcpAgent：会话管理、消息转换                     │
│  McpServer：文件操作、终端、bash 执行                   │
│  工具管道：编辑处理、差异生成                           │
└─────────────────────┬───────────────────────────────────┘
                      │ 代理的原生协议
┌─────────────────────▼───────────────────────────────────┐
│                   AI 提供商 API                          │
│            (Anthropic API, Google AI 等)                │
└─────────────────────────────────────────────────────────┘
```

对于 Claude Code 集成，Zed 构建了一个适配器（`@zed-industries/claude-code-acp`），包装了官方 Claude Code SDK。这个适配器在 ACP 的 JSON-RPC 格式和 SDK 的 API 调用之间进行转换，展示了如何在不需要原始供应商采用协议的情况下将现有代理引入 ACP 生态系统。

**MCP 集成**发生在会话初始化级别。创建新会话时，编辑器将可用 MCP 服务器端点列表传递给代理。代理可以在整个对话过程中访问这些服务器，将 MCP 工具视为其统一工具目录的一部分，与内置能力（如文件操作和终端命令）并列。这创建了一个**分层工具访问模型**：ACP 定义编辑器和代理如何通信，而 MCP 定义代理如何访问外部工具和数据。

## 核心能力和特性

ACP 提供了专为代理编码工作流设计的**丰富特性集**，远超简单的消息传递。

**上下文管理**允许精确控制代理看到的信息。用户可以 @-提及文件、符号（函数、类）、先前的对话线程，甚至粘贴图像以获取视觉上下文。协议支持获取网页内容作为上下文，并自动发现项目根目录中的 `CLAUDE.md` 配置文件以提供代理特定的指令。令牌使用跟踪显示在编辑器工具栏中，因此开发者知道何时接近上下文限制。

**实时流式传输**创建流畅的交互体验。当代理生成响应时，编辑器立即接收并逐令牌显示更新。工具调用与文本生成交错出现，因此用户实时看到代理搜索文件、阅读文档或执行命令。**跟随模式**使这更加强大——启用时（通过十字准星图标或提交时按住 cmd/ctrl），编辑器自动跟踪代理的焦点，在编辑文件时跳转到文件并滚动到相关代码部分。

**多文件编辑**与复杂的差异可视化使 ACP 区别于基于终端的代理。当代理提议跨多个文件的更改时，编辑器打开多缓冲区视图，同时显示所有修改，具有完整的语法高亮和语言服务器集成。开发者可以接受或拒绝单个代码块或整个文件，更改原子性应用。**检查点系统**允许在需要时将整个代码库恢复到编辑前状态。

**权限控制**通过 `ACP_PERMISSION_MODE` 环境变量实现三层安全模型：

- **default**：对所有文件操作、终端命令和工具执行提示批准。最大安全性但经常中断工作流。
- **acceptEdits**：自动批准文件编辑，但仍询问终端命令和其他敏感操作。推荐用于大多数工作流——在安全性和生产力之间取得平衡。
- **bypassPermissions**：自动批准所有操作。仅在沙盒环境中使用完全信任的代理。

权限模式可以通过提示中的特殊标记在对话中切换：`[ACP:PERMISSION:ACCEPT_EDITS]`、`[ACP:PERMISSION:BYPASS]` 或 `[ACP:PERMISSION:DEFAULT]`，以根据任务敏感性临时提升或降低权限。

**终端集成**提供交互式和后台终端支持。代理可以创建终端、执行命令、检索输出并杀死长时间运行的进程而不释放终端。这支持诸如"在监视模式下运行测试"或"启动开发服务器"的工作流，其中代理管理正在进行的进程。

**斜杠命令**公开代理特定的快捷方式。虽然内置命令支持因代理而异（Claude Code SDK 目前在这方面有限制），但自定义斜杠命令完全有效。示例包括 `/init` 创建 CLAUDE.md 配置、`/login` 进行身份验证或代理定义的自定义命令。

## 入门：实现指南

实现 ACP 取决于你的角色——在 Zed 中使用现有代理、开发自定义代理或为其他编辑器添加 ACP 支持。

### 在 Zed 中使用 Claude Code（最简单的路径）

**先决条件**：Zed v0.202.7 或更高版本（稳定版）和 Anthropic API 密钥或 Claude Pro/Max 订阅。

最快的设置使用 Zed 的自动安装。使用 `cmd-?`（Mac）或 `ctrl-?`（Windows/Linux）打开代理面板，单击 `+` 按钮，然后选择"New Claude Code Thread"。首次使用时，Zed 自动在托管位置安装 `@zed-industries/claude-code-acp` 并保持其更新。无需手动配置。

对于**手动安装**和自定义设置，添加到 `settings.json`：

```json
{
  "agent_servers": {
    "Claude Code": {
      "command": "npx",
      "args": ["@zed-industries/claude-code-acp"],
      "env": {
        "ACP_PERMISSION_MODE": "acceptEdits"
      }
    }
  }
}
```

**身份验证**通过 Claude Code 的原生流程进行，与 Zed 的第一方代理解耦。在代理面板中运行 `/login` 并在 API 密钥或"Log in with Claude Code"（使用你的 Claude 订阅）之间选择。重要提示：添加到 Zed 常规代理设置的 API 密钥不会被 Claude Code 使用——它有自己的身份验证系统。

在 `keymap.json` 中添加键盘快捷键以快速访问：

```json
[
  {
    "bindings": {
      "cmd-alt-c": ["agent::NewExternalAgentThread", { "agent": "claude_code" }]
    }
  }
]
```

### 开发自定义 ACP 代理

构建代理需要在你选择的语言中实现 ACP 协议。从 **TypeScript SDK**（npm 上的 `@zed-industries/agent-client-protocol`）开始，因为它具有最完整的实现和示例。

**TypeScript 中的基本代理结构**：

```typescript
import { AgentSideConnection } from "@zed-industries/agent-client-protocol";

const agent = new AgentSideConnection({
  onInitialize: async (params) => {
    // 返回代理能力
    return {
      protocolVersion: "0.4.0",
      capabilities: {
        streaming: true,
        loadSession: false,
        customCommands: ["analyze", "refactor"],
      },
    };
  },

  onNewSession: async (params) => {
    // 创建新对话会话
    const sessionId = generateSessionId();
    return { sessionId };
  },

  onPrompt: async (sessionId, messages, context) => {
    // 处理用户提示并流式响应
    for await (const chunk of generateResponse(messages)) {
      await agent.sendNotification("session/update", {
        sessionId,
        agent_message_chunk: chunk,
      });
    }
    return { stopReason: "endTurn" };
  },
});

// 开始在 stdin/stdout 上监听
agent.listen();
```

**关键实现要求**：

1. **版本协商**：始终在 `initialize` 中响应你支持的协议版本。如果不兼容，客户端将断开连接。
2. **流式更新**：发送频繁的 `session/update` 通知，以便用户看到进度。不要等到整个响应生成完毕。
3. **绝对路径**：处理文件时，始终使用绝对路径。协议明确禁止相对路径。
4. **工具请求**：通过适当的 JSON-RPC 请求请求文件操作和终端命令，在继续之前等待编辑器响应。
5. **优雅取消**：处理 `session/cancel` 通知，中断生成并干净返回。

**测试和调试**：配置 Zed 运行你的开发代理：

```json
{
  "agent_servers": {
    "Custom Agent": {
      "command": "node",
      "args": ["~/projects/my-agent/dist/index.js"],
      "env": {
        "ACP_DEBUG": "true"
      }
    }
  }
}
```

通过命令面板打开 ACP 日志视图：`dev: open acp logs`。这实时显示 Zed 和你的代理之间交换的所有 JSON-RPC 消息——对调试协议问题非常宝贵。

**参考实现**供研究：

- **Gemini CLI**：Google 的官方 ACP 代理，位于 github.com/google-gemini/gemini-cli
- **Claude Code Adapter**：展示包装现有 API，位于 github.com/zed-industries/claude-code-acp
- **协议示例**：TypeScript 和 Rust 示例，位于 github.com/zed-industries/agent-client-protocol/tree/main/examples

### 为其他编辑器添加 ACP 支持

编辑器开发者需要实现协议的客户端。如果构建原生编辑器，从 **Rust crate**（crates.io 上的 `agent-client-protocol`）开始，或者对于基于 Electron 的编辑器使用 TypeScript SDK。

**核心客户端职责**：

1. **进程管理**：将代理作为子进程生成，管理 stdin/stdout，处理进程生命周期
2. **文件系统调解**：使用权限检查实现 `fs.readTextFile` 和 `fs.writeTextFile`
3. **终端集成**：提供终端创建、命令执行和输出捕获
4. **MCP 服务器集成**：在会话创建期间将可用的 MCP 端点传递给代理
5. **流式传输 UI**：在通知到达时渲染实时逐令牌更新
6. **差异可视化**：使用接受/拒绝控件显示多文件更改

**Neovim 集成**通过 CodeCompanion 提供了一个可行的参考。该插件通过将代理作为作业生成、解析 JSON-RPC 消息并在缓冲区中渲染更新来实现 ACP 客户端。配置示例：

```lua
require("codecompanion").setup({
  adapters = {
    claude_code = function()
      return require("codecompanion.adapters").extend("acp", {
        name = "claude_code",
        command = "npx @zed-industries/claude-code-acp",
        env = {
          ACP_PERMISSION_MODE = "acceptEdits"
        }
      })
    end
  }
})
```

## 协议规范和 API 表面

**官方规范**位于 agentclientprotocol.com，规范的 JSON Schema 位于 github.com/zed-industries/agent-client-protocol/blob/main/schema/schema.json。当前版本是 **0.4.0**（截至 2025 年 10 月），明确标记为"正在大力开发中"——在 v1.0 之前预计会有破坏性更改。

**传输层**专门使用 JSON-RPC 2.0。消息是通过 stdin/stdout 发送的换行符分隔的 JSON 对象。每条消息要么是请求（期望响应）、响应（回答请求）、通知（不期望响应）或错误。

**请求格式**：

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "session/prompt",
  "params": {
    "sessionId": "abc123",
    "messages": [{ "role": "user", "content": "Refactor this function" }]
  }
}
```

**通知格式**（流式传输）：

```json
{
  "jsonrpc": "2.0",
  "method": "session/update",
  "params": {
    "sessionId": "abc123",
    "agent_message_chunk": { "type": "text", "text": "I'll help you" }
  }
}
```

**核心方法**协议定义：

**客户端 → 代理（编辑器发送的内容）**：

- `initialize(capabilities)` → 代理能力和版本
- `authenticate(method)` → 身份验证令牌或 OAuth 流程
- `session/new(params)` → 会话 ID
- `session/load(sessionId)` → 恢复的会话状态
- `session/prompt(sessionId, messages)` → 停止原因
- `session/cancel(sessionId)` [通知]

**代理 → 客户端（编辑器必须处理的内容）**：

- `fs/readTextFile(path)` → 文件内容
- `fs/writeTextFile(path, contents)` → 成功
- `terminal/create()` → 终端 ID
- `terminal/execute(terminalId, command)` → 执行结果
- `mcp/callTool(server, tool, params)` → 工具结果

**内容类型**尽可能重用 MCP JSON 表示：

- 文本内容：`{"type": "text", "text": "..."}`
- 图像内容：`{"type": "image", "source": {"type": "base64", "data": "..."}}`
- 工具结果：`{"type": "tool_result", "tool_use_id": "...", "content": "..."}`

编码工作流的自定义类型：

- 带统一差异格式的文件补丁
- 多文件编辑批次
- 用于 TODO 跟踪的计划条目
- 用于导航的符号引用

**扩展机制**使协议面向未来：

- **`_meta` 字段**：所有类型都包含此对象用于自定义数据，而不会破坏兼容性
- **自定义方法**：以下划线 (\_) 开头的名称保留用于扩展（例如，`_myAgent/customFeature`）
- **自定义能力**：在 `initialize` 响应中宣告，客户端优雅地忽略未知能力

**错误代码**遵循 JSON-RPC 2.0 标准（-32700 到 -32603）加上 ACP 特定代码：

- 需要身份验证：-32001
- 版本不匹配：-32002
- 不支持的能力：-32003
- 找不到会话：-32004

## 与 MCP 和更广泛生态系统的关系

ACP 和 MCP 占据**不同的架构层**，但无缝协作。理解它们的关系可以阐明设计理念和实际集成。

**MCP (Model Context Protocol)** 解决了将 AI 模型连接到数据源的"N×M 集成问题"。在 MCP 之前，每个需要让 Claude 访问 Google Drive、Slack 或 PostgreSQL 的应用程序都需要自定义集成代码。MCP 提供了一个标准接口，其中**一个 MCP 服务器实现**（例如，对于 Google Drive）与**任何 MCP 客户端**（Claude Desktop、Claude Code、IDE、自定义应用程序）配合使用。该协议定义了三种原语：模型自主调用的**工具**、应用程序提供的**资源**和用户控制的**提示**。MCP 对本地服务器使用 JSON-RPC over stdio，对远程服务器使用 HTTP with Server-Sent Events。

**ACP (Agent Client Protocol)** 解决了一个平行的集成问题：将代码编辑器连接到 AI 代理。在 ACP 之前，每个代理 - 编辑器组合都需要自定义集成——Claude Code 只能通过特定接口工作，Gemini CLI 需要自己的设置，Cursor 代理被锁定在 Cursor 中。ACP 提供了一个标准，其中**一个代理实现**在**任何 ACP 兼容的编辑器**中工作。该协议专注于编码特定的 UX：流式响应、多文件差异、权限控制和终端集成。

**它们相互补充**通过一个**分层架构**：

```
开发者在编辑器中编写代码 (Zed/Neovim/IntelliJ)
         ↕ ACP："编辑器和代理如何交谈？"
代理处理请求 (Claude Code/Gemini CLI/Goose)
         ↕ MCP："代理如何访问工具和数据？"
工具和数据源 (GitHub/Postgres/Google Drive/等)
```

在实践中，当 Zed 用户通过 ACP 启动 Claude Code 会话时：

1. **ACP 初始化**：Zed 启动 Claude Code 作为子进程，发送带有可用 MCP 端点的 `initialize`
2. **MCP 发现**：Claude Code 接收 MCP 服务器列表（GitHub、Slack 等）及其工具目录
3. **统一工具**：代理在一个目录中看到 ACP 文件操作和 MCP 工具
4. **分层执行**：代理请求"搜索 GitHub 问题"→ 通过 MCP；"编辑文件"→ 通过 ACP
5. **流式协调**：来自两个协议的结果通过 ACP 的流式传输到编辑器 UI

**协议互操作性**通过共享设计原则实现。ACP 故意**重用 MCP 的 JSON 表示**用于常见数据结构，如文本内容、工具结果和资源引用。文件路径以相同的方式工作（仅绝对路径）。两个协议都使用 Markdown 作为人类可读文本的默认格式。这意味着 MCP 工具结果可以直接流入 ACP 代理消息，无需翻译开销。

**关键架构差异**反映了它们不同的目的：

| 方面         | MCP                              | ACP                           |
| ------------ | -------------------------------- | ----------------------------- |
| **目的**     | 模型 ↔ 工具通信                 | 编辑器 ↔ 代理通信            |
| **连接模型** | 客户端 - 服务器（长期存在）      | 父 - 子进程（编辑器控制代理） |
| **传输**     | stdio（本地）或 HTTP+SSE（远程） | 专门使用 stdio                |
| **安全模型** | 客户端授予权限                   | 编辑器调解所有访问            |
| **流式传输** | 远程 SSE，本地通知               | JSON-RPC 通知                 |
| **焦点**     | 工具/资源发现和执行              | 编码 UX（差异、跟随、会话）   |

**采用轨迹**显示了不同的策略。MCP 推出时获得了广泛的生态系统支持——Anthropic 从第一天起就与 OpenAI、Google DeepMind、Block、Apollo、Zed、Replit 和其他公司合作。该协议迅速成为工具集成的事实标准，在 Python、TypeScript、C#、Java、Kotlin 和 Ruby 中提供官方 SDK。

ACP 采取了"以身作则"的方法。Zed 在内部重构了他们自己的代理以使用 ACP，然后为 Claude Code 构建了适配器，并与 Google 合作使 Gemini CLI 成为参考 ACP 代理。JetBrains 合作伙伴关系（2025 年 1 月）提供了大规模验证，将 ACP 引入 IntelliJ IDEA、PyCharm、WebStorm 和整个 JetBrains 生态系统。这一战略合作伙伴关系将 ACP 从"有趣的 Zed 实验"转变为"新兴的行业标准"。

**IBM 的 Agent Communication Protocol**（不幸的是也是"ACP"）服务于另一个层次：代理之间的协作。IBM 的协议使分布式多代理系统成为可能，其中自主代理协商、委派任务并协调工作。它是 RESTful 而不是 JSON-RPC，针对网络代理而不是编辑器 - 子进程模型进行了优化。这三个协议不竞争——它们在 AI 生态系统中实现不同的协作模式。

## 实际用例和当前限制

ACP 为希望在 AI 工具中获得灵活性而不放弃熟悉编辑器的开发者解决了实际工作流问题。

**多代理工作流**在你可以在不切换工具的情况下切换代理时变得实用。使用 Claude Code 进行复杂的架构重构，其代理推理能力出色，然后切换到 Gemini CLI 进行快速原型设计，其中速度很重要，所有这些都在同一个 Zed 项目中。通过并排运行多个会话来比较代理在同一任务上的性能。这种"适合工作的最佳工具"方法在 ACP 标准化之前是不可能的。

**大规模重构**从 ACP 的多缓冲区差异可视化中受益匪浅。当代理提议跨 15 个文件的更改时，使用完整的语法高亮和语言服务器支持（类型信息、内联错误）同时查看所有差异使审查变得实用。接受看起来完美的三个文件，更仔细地检查接下来的五个，拒绝两个出错的——所有这些都具有细粒度控制。纯终端代理无法提供这种审查能力。

**安全敏感环境**从 ACP 的本地优先架构中获得信心。代理在你的机器上作为子进程运行；代码永远不会通过 Zed 的服务器路由。编辑器通过显式协议请求控制所有文件和终端访问。你可以通过 ACP 日志准确审计代理正在做什么。对于具有严格数据策略的企业来说，这种透明度和本地执行模型很重要。

**自定义代理开发**变得易于访问。为你的领域（固件开发、数据管道工程、学术研究）构建专门的代理不再需要分叉整个编辑器或构建自定义 UI。实现 ACP 协议，你的代理立即获得生产级功能：流式响应、语法高亮差异、文件导航、调试日志。所有编码代理通用的 80% 的功能都是免费的。

**跨编辑器可移植性**解锁了切换成本。如果你是 Neovim 用户但想要 Claude Code 的能力，安装 CodeCompanion 并配置 ACP 适配器——相同的代理，你的编辑器。如果你的团队使用 JetBrains IDE 但你更喜欢 Zed，你们都可以使用相同的代理，行为一致。该协议确保了可移植性。

**当前限制**反映了 ACP 的早期阶段（v0.4.0，"正在大力开发中"）：

**功能差距**与第一方集成相比存在。你无法在外部代理线程中编辑过去的消息，从历史 UI 恢复线程，或依赖所有代理中的检查点（支持各不相同）。SSH 远程项目尚不适用于外部代理。Claude Code SDK 的一些内置斜杠命令未通过 ACP 适配器公开（尽管自定义斜杠命令完全有效）。这些是实现成熟度问题，而不是基本的协议限制。

**SDK 覆盖**问题特别影响 Claude Code。Anthropic 的 SDK 没有公开与原生 Claude Code 完全对等所需的所有功能。钩子尚不受支持。Zed 团队针对可用的 SDK 方法构建了适配器，但一些能力在 Anthropic 扩展 SDK 表面之前仍然无法访问。

**身份验证复杂性**因代理而异。Claude Code 需要 API 密钥或通过其 OAuth 流程登录。Gemini CLI 根据你的设置提供 Google 登录、API 密钥或 Vertex AI。自定义代理实现自己的身份验证。没有统一的身份验证故事——每个代理以不同的方式处理它，这可能会混淆在代理之间切换的用户。

**协议稳定性**不能保证。"正在大力开发中"状态意味着在 v1.0 之前可能会有破坏性更改。代理开发者应该预期在协议演进时更新实现。Zed 团队有一个结构化的更改流程（在协议更改之前讨论，针对错误的问题），但尚未承诺稳定性保证。

**生态系统差距**仍然存在。像 Cursor 这样的主要参与者尚未正式采用 ACP（存在社区适配器）。Aider 集成正在进行中但尚未完成。如果一些流行的代理更喜欢维护自己的接口，它们可能永远不会采用 ACP。网络效应是双向的——如果关键代理不参与，编辑器开发者失去实现客户端支持的动力。

**异步能力**与 IBM 的 Agent Communication Protocol 相比有限。ACP 的 stdin/stdout 子进程模型非常适合请求 - 响应模式，但在需要人类在环反馈超过数小时或数天的长时间运行代理方面遇到困难。检查点/恢复有所帮助，但对于复杂的多日项目来说不是完整的解决方案。

尽管存在限制，ACP 已经为其核心用例实现了产品 - 市场契合：**使 AI 编码代理在编辑器之间可互操作，而无需供应商锁定**。JetBrains 合作伙伴关系验证了这一点——他们评估了这个领域，并决定基于 ACP 构建比自定义集成更好。

## 未来方向和采用势头

**JetBrains 合作伙伴关系**（2025 年 1 月）从根本上改变了 ACP 的轨迹。当 JetBrains 承诺共同开发该协议并将其引入其整个 IDE 阵容——IntelliJ IDEA、PyCharm、WebStorm、GoLand、RubyMine、CLion 等——ACP 从"有趣的实验"转变为"战略基础设施"。JetBrains 有超过 900 万开发者使用他们的工具；ACP 在其生态系统中的支持为任何实现该协议的代理创造了大规模分发。

**当前采用状态**显示了客户端和代理的快速增长：

**支持 ACP 的编辑器**（2025 年 10 月）：

- ✅ **Zed**（原生，v0.201.5+）- 参考实现
- ✅ **Neovim**（CodeCompanion、avante.nvim 插件）- 社区驱动，生产就绪
- ✅ **Emacs**（agent-shell.el）- 功能实现
- 🚧 **JetBrains**（整个生态系统）- 官方合作伙伴关系，正在开发中
- 🚧 **Eclipse**（原型）- 实验性
- ✅ **marimo notebook**（Python notebooks）- 工作集成

**支持 ACP 的代理**：

- ✅ **Gemini CLI**（Google）- 官方参考代理，与 ACP 一起推出
- ✅ **Claude Code**（Anthropic）- 通过 Zed 的 SDK 适配器，生产就绪
- ✅ **Goose**（Square）- 原生 ACP 支持，开源
- 🚧 **Codex**（OpenAI）- 官方适配器正在开发中
- 🚧 **Aider** - 实现正在进行中
- Cursor 和其他的社区适配器存在

**SDK 生态系统**正在成熟，对 TypeScript（npm：@zed-industries/agent-client-protocol）和 Rust（crates.io：agent-client-protocol）提供官方支持，以及 Python、Dart 和 React 中的社区实现。npm 上超过 15 个依赖项目表明开发者采用率正在增长。

**协议演进**遵循结构化的治理模型。Zed 团队维护规范，但通过 GitHub 讨论协议建议和针对错误报告的问题来鼓励社区输入。更改遵循一个审慎的流程：在编码之前讨论架构影响，通过拉取请求提议，根据反馈迭代。Apache 2.0 许可证确保即使 Zed 调整业务战略，协议仍然保持开放。

**近期路线图**（根据公开声明未来 3-6 个月）：

- Zed 中增强的代理选择 UI，具有 MCP 风格的可视化配置
- 随着 Claude Code SDK 和其他代理 API 的成熟，功能对等性改进
- JetBrains 在其 IDE 阵容中推出
- 额外的代理合作伙伴关系"正在进行中，我们还没有准备好分享"
- 协议稳定化，朝向 v1.0，具有向后兼容性保证

**长期愿景**将 ACP 定位为编辑器 - 代理通信的通用标准，类似于 LSP 在语言工具中的作用。在 LSP 之前，每个编辑器为每种语言实现自定义解析器——Eclipse 有一个 Java 解析器，VSCode 有一个 TypeScript 解析器，Vim 有用于所有内容的插件。LSP 使一个语言服务器可以在任何地方工作，释放了语言支持的爆炸式增长。ACP 的目标是相同的结果：**一个代理实现到达每个编辑器，使 AI 编码辅助的快速创新成为可能，而无需集成开销**。

**战略挑战**仍然存在。Cursor 的大规模增长表明，如果 AI 体验卓越，开发者将容忍编辑器锁定。如果领先的代理不采用 ACP，该协议有可能成为"Zed 和 JetBrains 加上小众工具"而不是"通用标准"。stdin/stdout 子进程模型可能被证明对于新兴的代理架构（分布式多代理系统、云原生代理）有限制。协议治理必须从 Zed 控制演变为真正的开放治理，以获得完整的生态系统支持。

**市场时机**有利于 ACP。AI 编码助手领域是混乱的——每周都有新代理推出，初创公司每月都在调整，开发者不断在工具之间流失。标准化在混乱中创造稳定性。评估 AI 编码工具的企业更喜欢开放协议而不是供应商特定的解决方案。LSP 比较与记得碎片化工具之前时代的开发者产生共鸣。

## 程序员需要知道什么

**ACP 解决了集成问题**，阻止开发者混合和匹配编辑器和 AI 代理。该协议通过提供通用接口消除了供应商锁定，就像 USB-C 消除了专有充电电缆一样。你独立选择你的编辑器用于编辑，你的代理用于智能。

**如果你使用 Zed，入门只需几分钟**。打开代理面板，单击 +，选择 Claude Code 或 Gemini CLI，在提示时进行身份验证。编辑器自动安装必要的适配器。为频繁访问添加键盘快捷键。根据信任级别配置权限模式——`acceptEdits` 为大多数用户在安全性和工作流速度之间取得平衡。

**构建自定义代理**需要通过 stdin/stdout 实现 JSON-RPC 2.0。使用 TypeScript 或 Rust SDK 以获得类型安全和辅助函数。研究 Gemini CLI 的实现作为参考。使用自定义代理配置和启用的 ACP 日志在 Zed 中进行测试。该协议正在积极开发中——在 v1.0 之前预计会有 API 更改。

**ACP 和 MCP 是互补的**，而不是竞争的。MCP 将模型连接到工具和数据源。ACP 将编辑器连接到代理。使用 ACP 的代理可以利用 MCP 服务器获得扩展能力。如果你正在构建 AI 工具，理解两者：MCP 用于你的代理可以访问什么，ACP 用于你的代理可以在哪里运行。

**当前限制**如果你需要特定功能很重要。你无法在外部代理线程中编辑过去的消息或恢复旧线程。SSH 项目尚不可用。由于 SDK 差距，一些 Claude Code 功能仍然无法访问。身份验证因代理而异。该协议"正在大力开发中"——在 v1.0 之前不保证 API 稳定性。

**JetBrains 合作伙伴关系验证了 ACP** 不仅仅是 Zed 实验。当行业最大的专业 IDE 供应商承诺共同开发协议时，这表明了战略重要性。代理开发者应该优先考虑 ACP 实现——一个协议现在到达 Zed、Neovim、Emacs，很快还有 IntelliJ IDEA、PyCharm、WebStorm 和整个 JetBrains 生态系统。

**将 ACP 视为基础设施**而不是竞争功能。这是在更高层次实现创新的管道。编辑器专注于编辑，代理专注于智能，两者都独立改进，而协议确保兼容性。这种解耦为针对特定用例优化的专门工具创造了空间，而不是试图做所有事情的整体平台。
