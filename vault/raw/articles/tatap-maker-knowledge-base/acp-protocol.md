# ACP 协议规范

Agent Client Protocol (ACP) 基础知识与协议规范。

**来源**: Zed 开源项目
**基础协议**: JSON-RPC 2.0
**日期**: 2025-10-24

---

## 什么是 ACP？

**ACP (Agent Client Protocol)** 是基于 JSON-RPC 2.0 的标准协议，用于编辑器/IDE 与 AI Agent 之间的通信。由 Zed 开发并开源。

**核心优势**:

- ✅ 标准协议，可跨语言实现
- ✅ 支持远程通信（HTTP、WebSocket、STDIO）
- ✅ 将文件操作抽象为 JSON-RPC 请求，实现容器隔离

---

## JSON-RPC 2.0 基础

ACP 基于 JSON-RPC 2.0，有三种消息类型：

### 1. Request（请求）

```typescript
{
  "jsonrpc": "2.0",
  "id": 1,              // 必须有 id
  "method": "prompt",
  "params": { ... }
}
```

**特点**: 需要响应（response），通过 `id` 匹配。

---

### 2. Response（响应）

```typescript
// 成功响应
{
  "jsonrpc": "2.0",
  "id": 1,              // 匹配 request id
  "result": { ... }
}

// 错误响应
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": { ... }
  }
}
```

**特点**: 必须包含 `result` 或 `error`，`id` 匹配原始 request。

---

### 3. Notification（通知）

```typescript
{
  "jsonrpc": "2.0",
  "method": "session/update",  // 有 method
  "params": { ... }            // 无 id
}
```

**特点**: 无 `id`，不需要响应，单向通知。

---

## 核心方法

### Client → Agent

#### initialize

初始化 agent，协商 capabilities。

**Request**:

```typescript
{
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": 1,
    "clientCapabilities": {
      "fs": {
        "readTextFile": true,
        "writeTextFile": true
      }
    }
  }
}
```

**Response**:

```typescript
{
  "id": 1,
  "result": {
    "agentCapabilities": {
      "tools": ["Read", "Write", "Bash", "Glob", "Grep"],
      "streaming": true
    }
  }
}
```

---

#### newSession

创建新的 AI session。

**Request**:

```typescript
{
  "id": 2,
  "method": "newSession",
  "params": {
    "cwd": "/workspace/project",
    "mcpServers": [
      {
        "name": "terminal",
        "transport": {
          "type": "http",
          "url": "http://tool-api:3000",
          "headers": [
            { "name": "Authorization", "value": "Bearer <token>" }
          ]
        }
      }
    ]
  }
}
```

**Response**:

```typescript
{
  "id": 2,
  "result": {
    "sessionId": "sess-abc123",
    "models": ["claude-3-5-sonnet-20241022"]
  }
}
```

---

#### prompt

发送用户消息给 AI。

**Request**:

```typescript
{
  "id": 3,
  "method": "prompt",
  "params": {
    "sessionId": "sess-abc123",
    "prompt": [
      {
        "type": "text",
        "text": "读取 src/index.ts 文件"
      }
    ]
  }
}
```

**Response**: 无返回（通过 notification 推送 AI 响应）

---

#### closeSession

关闭 session。

**Request**:

```typescript
{
  "id": 4,
  "method": "closeSession",
  "params": {
    "sessionId": "sess-abc123"
  }
}
```

**Response**: 无返回

---

## Agent → Client (工具请求)

### fs/readTextFile

读取文件。

**Request**:

```typescript
{
  "id": 456,
  "method": "fs/readTextFile",
  "params": {
    "path": "/workspace/src/index.ts",
    "offset": 0,   // 可选，行偏移
    "limit": 100   // 可选，最多读取行数
  }
}
```

**Response**:

```typescript
{
  "id": 456,
  "result": {
    "content": "export function main() { ... }"
  }
}
```

---

### fs/writeTextFile

写入文件。

**Request**:

```typescript
{
  "id": 457,
  "method": "fs/writeTextFile",
  "params": {
    "path": "/workspace/src/index.ts",
    "content": "export function main() { ... }"
  }
}
```

**Response**:

```typescript
{
  "id": 457,
  "result": {
    "success": true
  }
}
```

---

### terminal/execute

执行命令（通过 MCP Server 提供）。

**Request**:

```typescript
{
  "id": 458,
  "method": "terminal/execute",
  "params": {
    "command": "ls -la",
    "cwd": "/workspace"
  }
}
```

**Response**:

```typescript
{
  "id": 458,
  "result": {
    "stdout": "total 48\ndrwxr-xr-x  ...",
    "stderr": "",
    "exitCode": 0
  }
}
```

---

### fs/glob

文件搜索。

**Request**:

```typescript
{
  "id": 459,
  "method": "fs/glob",
  "params": {
    "pattern": "**/*.ts",
    "cwd": "/workspace"
  }
}
```

**Response**:

```typescript
{
  "id": 459,
  "result": {
    "files": ["src/index.ts", "src/utils.ts"]
  }
}
```

---

## Agent → Client (Notifications)

### session/update

AI 生成的内容。

````typescript
{
  "method": "session/update",
  "params": {
    "sessionId": "sess-abc123",
    "content": {
      "type": "text",
      "text": "文件内容如下：\n```typescript\nexport function main() { ... }\n```"
    }
  }
}
````

---

### session/error

Session 错误。

```typescript
{
  "method": "session/error",
  "params": {
    "sessionId": "sess-abc123",
    "error": {
      "code": "MAX_TURNS_EXCEEDED",
      "message": "Maximum number of turns exceeded"
    }
  }
}
```

---

## Client Capabilities

Client 在 `initialize` 时声明支持的能力：

```typescript
{
  "clientCapabilities": {
    "fs": {
      "readTextFile": true,   // 支持读取文件
      "writeTextFile": true   // 支持写入文件
    }
  }
}
```

**注意**: `terminal` 不在 `clientCapabilities` 中声明，而是通过 `newSession` 的 `mcpServers` 参数提供（MCP Server 架构）。

---

## MCP (Model Context Protocol)

**为什么 terminal 不是 Client Capability？**

因为 `terminal/execute` 不是 ACP 标准的 client capability，而是通过 **MCP (Model Context Protocol) Server** 提供。

**MCP Server 配置示例**:

```typescript
{
  "mcpServers": [
    {
      "name": "terminal",
      "transport": {
        "type": "http",
        "url": "http://tool-api:3000",
        "headers": [
          { "name": "Authorization", "value": "Bearer <JWT>" }
        ]
      }
    }
  ]
}
```

**MCP Server 架构**:

- Agent 调用 `terminal/execute` 时，自动路由到 MCP Server
- MCP Server 是独立的 HTTP 服务，提供 terminal 功能
- 支持多个 MCP Server（terminal、database、web search...）

---

## 完整消息流示例

### 场景：用户发送 "读取 src/index.ts"

```
┌─────────┐
│ Client  │ 1. initialize()
└────┬────┘
     │ JSON-RPC Request
     ▼
┌─────────┐
│  Agent  │ 2. 返回 agentCapabilities
└────┬────┘
     │
     ▼
┌─────────┐
│ Client  │ 3. newSession({ cwd, mcpServers })
└────┬────┘
     │ JSON-RPC Request
     ▼
┌─────────┐
│  Agent  │ 4. 返回 sessionId
└────┬────┘
     │
     ▼
┌─────────┐
│ Client  │ 5. prompt({ sessionId, prompt: "读取 src/index.ts" })
└────┬────┘
     │ JSON-RPC Request
     ▼
┌─────────┐
│  Agent  │ 6. 调用 Claude API
└────┬────┘ 7. AI 返回 tool call: ReadTextFile
     │
     │ JSON-RPC Request
     ▼
┌─────────┐
│ Client  │ 8. 收到 fs/readTextFile 请求
└────┬────┘
     │ 9. 读取文件
     │
     │ JSON-RPC Response
     ▼
┌─────────┐
│  Agent  │ 10. 收到文件内容
└────┬────┘ 11. 继续 Claude SDK 处理
     │ 12. AI 生成最终响应
     │
     │ JSON-RPC Notification
     ▼
┌─────────┐
│ Client  │ 13. 收到 session/update notification
└─────────┘
```

---

## 错误码

### 标准 JSON-RPC 2.0 错误码

```typescript
const ERROR_CODES = {
  PARSE_ERROR: -32700, // JSON 解析失败
  INVALID_REQUEST: -32600, // 请求格式错误
  METHOD_NOT_FOUND: -32601, // 方法不存在
  INVALID_PARAMS: -32602, // 参数错误
  INTERNAL_ERROR: -32603, // 内部错误
};
```

### 错误响应示例

```typescript
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32601,
    "message": "Method not found: unknown_method",
    "data": { "method": "unknown_method" }
  }
}
```

---

## Schema 要求（重要）

### headers 字段

- 必须是 **required** 字段（不能是可选）
- 类型必须是 `Array<{name: string, value: string}>`，而非 `Record<string, string>`
- 即使不需要任何 header，也必须传递空数组 `[]`

**示例**:

```typescript
// ✅ 正确
{
  "transport": {
    "type": "http",
    "url": "http://tool-api:3000",
    "headers": []  // 空数组
  }
}

// ❌ 错误
{
  "transport": {
    "type": "http",
    "url": "http://tool-api:3000",
    "headers": {}  // Record 格式不符合 Schema
  }
}
```

---

### prompt 参数

- 字段名必须是 `prompt`（不是 `messages`）
- 必须是 `ContentBlock[]` 格式：`[{type: "text", text: "..."}]`

**示例**:

```typescript
// ✅ 正确
{
  "method": "prompt",
  "params": {
    "sessionId": "sess-123",
    "prompt": [
      { "type": "text", "text": "读取 src/index.ts" }
    ]
  }
}

// ❌ 错误
{
  "method": "prompt",
  "params": {
    "sessionId": "sess-123",
    "messages": [...]  // 字段名错误
  }
}
```

---

## 外部参考资料

- [ACP Spec](https://github.com/agentclientprotocol/spec) - ACP 协议规范
- [Zed claude-code-acp](https://github.com/zed-industries/zed) - Zed 的 ACP 实现
- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification) - JSON-RPC 规范
- [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) - MCP 协议

---

**维护日志**:

- 2025-10-24: 初版，从 `acp-architecture.md` 提取协议知识
