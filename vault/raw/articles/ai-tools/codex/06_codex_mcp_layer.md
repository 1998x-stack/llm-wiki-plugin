# Codex CLI 深度解析 Vol.6：MCP Layer — Agent 与外部世界的协议总线

> **组件定位**：MCP（Model Context Protocol）是 Codex CLI 的"USB-C 接口"——标准化的 Agent 工具连接协议。Codex 同时扮演 MCP 客户端（连接外部工具）和 MCP 服务端（将自身暴露给其他 Agent）两个角色，形成可组合的 Agent 生态。

---

## 1. MCP 是什么？

MCP（Model Context Protocol）是 Anthropic 提出、被广泛采用的开放协议：

```
传统方式（每个工具都要定制集成）：
  Agent → [硬编码调用] → GitHub API
  Agent → [硬编码调用] → Slack API
  Agent → [硬编码调用] → 数据库

MCP 方式（统一协议层）：
  Agent (MCP Client) → [MCP Protocol] → GitHub MCP Server
                                      → Slack MCP Server
                                      → 数据库 MCP Server
```

**核心价值：工具与 Agent 解耦。**  
任何支持 MCP 的工具，都可以被任何支持 MCP 的 Agent 使用，无需定制集成代码。

---

## 2. Codex 的 MCP 双重身份

```
                    ┌─────────────────────┐
  外部 MCP 工具      │    Codex CLI        │   其他 Agent
       服务端        │                     │   (Cursor, 另一个
  ──────────────►   │  MCP Client         │    Codex 实例...)
  GitHub Server     │  ──────────────────►│
  Slack Server      │                     │◄──────────────
  Context7 Server   │  MCP Server         │  MCP Client
  ...               │  (codex mcp-server) │
                    └─────────────────────┘
```

**Codex 作为 MCP Client（连接外部工具）：**  
启动时连接 config.toml 中声明的 MCP 服务器，将其工具暴露给 LLM 调用。

**Codex 作为 MCP Server（暴露自身给其他 Agent）：**  
`codex mcp-server` 启动后，其他 MCP 客户端可以把"整个 Codex Agent"作为一个工具调用。

---

## 3. MCP Client 配置

### 3.1 config.toml 中声明 MCP 服务器

```toml
# ~/.codex/config.toml

[mcp_servers.context7]
command = "npx"
args = ["-y", "@upstash/context7-mcp@latest"]
enabled = true

[mcp_servers.github]
command = "npx"
args = ["-y", "@modelcontextprotocol/server-github"]
env = { GITHUB_TOKEN = "$GITHUB_TOKEN" }
enabled = true

[mcp_servers.slack]
command = "python"
args = ["-m", "slack_mcp_server"]
enabled = false   # 按需启用
```

### 3.2 MCP 服务器的传输协议

```
stdio（最常用）：
  Codex 启动 MCP Server 进程，通过 stdin/stdout 通信
  优点：简单，无端口冲突
  
HTTP/SSE（远程服务）：
  MCP Server 运行在远端，通过 HTTP + Server-Sent Events
  支持 bearer-token 认证
  
WebSocket：
  双向实时通信，适合需要服务器主动推送的场景
```

### 3.3 运行时工具发现

Codex 启动时：
1. 按 config.toml 启动各 MCP Server 进程
2. 调用每个 server 的 `tools/list` 接口，获取工具清单
3. 将所有工具注入 LLM 的 system prompt（tool definitions）
4. LLM 的 tool_call 请求被路由到对应 MCP Server

```
系统启动                    LLM 推理时
    │                           │
    ├─ 启动 context7 ─► 获取工具列表   LLM 决定调用 search_code
    ├─ 启动 github  ─► 获取工具列表      ↓
    └─ 启动 slack   ─► 获取工具列表   路由到 context7 MCP Server
                                          ↓
                                       返回搜索结果
                                          ↓
                                       注入 LLM 上下文
```

---

## 4. MCP Server 模式（Codex 自身作为工具）

```bash
# 启动 Codex 作为 MCP Server
codex mcp-server

# 用 MCP Inspector 调试
npx @modelcontextprotocol/inspector codex mcp-server
```

**暴露的工具（示例）：**

```json
{
  "tools": [
    {
      "name": "codex_exec",
      "description": "在 Codex Agent 会话中执行编码任务",
      "inputSchema": {
        "type": "object",
        "properties": {
          "prompt": {"type": "string", "description": "任务描述"},
          "workspace": {"type": "string", "description": "工作目录"}
        }
      }
    },
    {
      "name": "codex_review",
      "description": "对代码变更进行 AI Code Review"
    }
  ]
}
```

**使用场景：**
```
父级 Orchestrator Agent
    ↓
    ├── 调用 codex_exec("为这个模块写测试")    → Codex 子 Agent
    ├── 调用 codex_exec("生成 API 文档")       → Codex 子 Agent
    └── 调用 codex_review("检查这个 PR")       → Codex 子 Agent
    
父 Agent 负责协调，Codex 负责执行具体编码任务
```

---

## 5. Plugins 系统

2026 年初 Codex 引入了基于 MCP 的 **Plugins** 系统：

```bash
# 浏览已安装 plugins
/plugins

# Plugin 的发现与安装
# Codex 在启动时自动同步 product-scoped plugins
# 支持安装/卸载，并处理 auth/setup 流程
```

Plugins 与普通 MCP Server 的区别：

| 维度 | 普通 MCP Server | Plugin |
|------|---------------|--------|
| 发现 | 手动配置 config.toml | 自动从 plugin registry 同步 |
| 认证 | 手动设置 env/token | Plugin 框架统一处理 |
| 更新 | 手动更新配置 | 自动版本管理 |
| TUI 集成 | 无 `/plugins` 面板 | 有专属 UI |

---

## 6. MCP 工具调用的安全控制

MCP 工具调用同样受 Approval 机制保护：

```toml
# 精细控制 MCP elicitation 的审批行为
approval_policy = { granular = {
  mcp_elicitations = true,    # MCP 请求权限时展示给用户确认
  request_permissions = true, # request_permissions 工具需要确认
} }
```

**破坏性操作自动需要审批：**

```
MCP 工具的 annotations：
  read-only: true    → 自动放行（reading GitHub PR）
  destructive: true  → 强制要求审批（closing GitHub issues）
  
即使 approval_policy = "never"，
带 destructive annotation 的 MCP 工具调用仍然需要审批
```

---

## 7. 环境变量隔离（Shell Environment Policy）

MCP Server 进程和工具执行进程都从 Codex 继承环境变量，这可能泄露密钥：

```toml
# 精细控制哪些环境变量传递给子进程
[shell_environment_policy]
inherit = "none"                    # 不继承任何 env var
set = { PATH = "/usr/bin:/usr/local/bin" }  # 只传递必要的
exclude = ["AWS_*", "AZURE_*"]      # glob 模式排除
include_only = ["PATH", "HOME", "GITHUB_TOKEN"]  # 白名单

# 默认行为：自动排除包含 KEY/SECRET/TOKEN 的 env var
ignore_default_excludes = false
```

---

## 8. MCP 增强确定性的方式

| 不确定性来源 | MCP 的应对 |
|------------|-----------|
| LLM 对外部系统状态"猜测" | 通过 MCP 工具直接读取真实状态 |
| 工具接口不稳定，Agent 调用出错 | MCP schema 强类型约束，load-time 验证 |
| 工具调用暴露系统权限 | Approval gate + destructive annotation 强制确认 |
| 密钥通过 env 泄露给工具进程 | Shell environment policy 精细过滤 |
| Agent 对工具能力误解 | `tools/list` 接口的 description 字段规范化 |

---

## 9. 工程哲学摘要

> **MCP Layer 的本质是把"工具集成"从编程问题变成配置问题。**
>
> 过去：每接入一个新工具，就需要写一段集成代码、处理认证、解析响应格式。
> 现在：在 config.toml 里加一段配置，工具自动可用。
>
> Codex 同时是客户端和服务端这一设计，
> 实现了 Agent 的"可组合性"——
> 任何 Codex 实例都可以成为更大 Agent 系统的一个工具节点。

---

*下一篇：Vol.7 — Multi-Agent：并行编码的调度与协同*
