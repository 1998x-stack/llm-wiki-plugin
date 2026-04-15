# MemPalace 深度解析（六）：MCP 工具集成

> 19 个工具，让任何 AI Agent 都能调用你的记忆宫殿

---

## 0. 什么是 MCP？

MCP（Model Context Protocol）是 Anthropic 于 2024 年末提出的标准协议，定义了 AI Agent 与外部工具/数据源之间的通信方式。

简单说：**MCP 是 AI 的 USB 接口**。任何支持 MCP 的工具，都可以被支持 MCP 的 AI（Claude、GPT、Gemini 等）调用，无需为每个模型单独适配。

MemPalace v3.0.0 完整实现了 MCP Server，提供 **19 个工具**，让 AI Agent 能够读写记忆宫殿。

---

## 1. 19 个 MCP 工具全览

MemPalace 的 19 个工具按功能分为 6 组：

### Group 1：状态与导航（3 个）

| 工具 | 功能 |
|------|------|
| `mempalace_status` | 获取 Palace 全局状态（Level 1 加载）+ 注入 KBS 协议 |
| `mempalace_wing_detail` | 展开某个 Wing 的详情（Level 2 加载） |
| `mempalace_room_detail` | 展开某个 Room + Closet（Level 3 加载） |

这三个工具实现了**第四篇介绍的渐进式加载**，是 AI Agent 导航记忆的入口。

### Group 2：搜索（2 个）

| 工具 | 参数 | 功能 |
|------|------|------|
| `mempalace_search` | `query`, `wing?`, `room?`, `limit?` | 全文语义搜索，支持范围过滤 |
| `mempalace_kg_query` | `entity`, `relation?` | 知识图谱实体查询 |

`mempalace_search` 是最常用的工具，底层调用 ChromaDB 的向量搜索。当指定 `wing` 和 `room` 时，搜索范围收窄，精准度显著提升。

`mempalace_kg_query` 查询时序知识图谱，用于"某个事实的历史变化"类问题。

### Group 3：写入（4 个）

| 工具 | 功能 |
|------|------|
| `mempalace_save` | 保存新记忆到指定 Wing/Room/Hall |
| `mempalace_save_decision` | 快捷保存决策（自动路由到 decisions Hall） |
| `mempalace_save_preference` | 快捷保存偏好（自动路由到 preferences Hall） |
| `mempalace_kg_update` | 更新知识图谱中某个实体的状态 |

`mempalace_save` 是通用写入接口：

```json
{
  "tool": "mempalace_save",
  "input": {
    "content": "我们决定把部署频率从每周改为每天，原因是...",
    "wing": "my_app",
    "room": "deploy",
    "hall": "decisions",
    "tags": ["deployment", "ci-cd"]
  }
}
```

### Group 4：Tunnel 发现（1 个）

| 工具 | 功能 |
|------|------|
| `mempalace_tunnel_explore` | 探索当前 Room 的跨域连接 |

当 AI 在处理 `my_app.auth` 时调用这个工具，会发现"还有 `client_portal.auth` 这个关联 Room"，并可选择是否展开查看。

### Group 5：日记（2 个）

| 工具 | 功能 |
|------|------|
| `mempalace_diary_write` | 写入带时间戳的日记条目 |
| `mempalace_diary_read` | 读取最近 N 条日记 |

日记功能为 AI Agent 提供了一个**持久化的工作日志**——每次 Agent 完成重要任务时写入，下次启动时可以回顾。

这对长期运行的 Agent（如 Claude Code 项目）特别有用：Agent 挂掉重启后，可以通过日记快速恢复上下文。

### Group 6：管理工具（7 个）

| 工具 | 功能 |
|------|------|
| `mempalace_list_wings` | 列出所有 Wing |
| `mempalace_list_rooms` | 列出某 Wing 下所有 Room |
| `mempalace_delete` | 删除指定 Drawer |
| `mempalace_update` | 更新指定 Drawer 的内容 |
| `mempalace_export` | 导出指定范围的内容 |
| `mempalace_stats` | 统计信息（各 Wing/Room 的 Drawer 数量）|
| `mempalace_rebuild_index` | 重建向量索引（数据修复用）|

---

## 2. Claude Code 的自动保存集成

MemPalace 为 Claude Code 提供了特殊的 **Auto-save 功能**：

```json
// Claude Code MCP 配置（.claude/settings.json）
{
  "mcp_servers": {
    "mempalace": {
      "command": "mempalace",
      "args": ["serve"],
      "auto_save": {
        "enabled": true,
        "triggers": ["session_end", "important_decision"],
        "wing": "claude_code_sessions"
      }
    }
  }
}
```

启用后，每次 Claude Code 会话结束时，它会自动调用 `mempalace_save` 保存本次会话的关键决策和代码变更摘要，无需手动触发。

---

## 3. MCP 工具的调用流（完整示例）

以下是一个典型的 AI Agent 使用 MemPalace 回答问题的完整流程：

**用户问题**：`为什么我们的 API 要限制每分钟 100 次请求？`

```
Step 1: Agent 调用 mempalace_status
  → 收到 Palace 地图：有 my_app, alice, client_portal 三个翼
  → 注入 KBS 协议（先查记忆再回答）

Step 2: Agent 调用 mempalace_search
  Input: { query: "API rate limit 100 per minute", wing: "my_app" }
  → ChromaDB 向量搜索，缩小到 my_app 翼
  → 返回 Top-3 相关 Drawer

Step 3: Agent 读取 Drawer 内容
  → 找到 2025-09-15 的对话记录：
    "我们决定把速率限制设为 100/min，因为 DDoS 测试显示
     超过这个阈值后数据库连接池会耗尽。另外免费层用户
     的 SLA 不需要更高的吞吐量..."

Step 4: Agent 回答用户
  "根据 2025 年 9 月的架构讨论，选择 100/min 有两个原因：
   1. DDoS 压测发现超过此阈值会导致数据库连接池耗尽
   2. 免费层 SLA 不需要更高吞吐量
   [原始讨论来自 my_app.api.decisions]"
```

**关键点**：Agent 给出了带完整推理链的答案，不是凭模型训练数据猜测的，而是从保存的原始对话中检索出来的。

---

## 4. 跨模型兼容性

MemPalace 的 MCP Server 遵循标准协议，支持以下模型：

| 模型 | MCP 支持 | 状态 |
|------|---------|------|
| Claude（Anthropic） | 原生 | ✅ 完整支持 |
| GPT-4o（OpenAI） | 通过 API 适配 | ✅ 支持 |
| Gemini（Google） | 通过 API 适配 | ✅ 支持 |
| Llama（本地） | 通过 Ollama MCP 插件 | ✅ 支持 |
| Mistral | 通过 API 适配 | ✅ 支持 |

**因为 AAAK 本质上是结构化的英语缩写，任何能读英文的模型都能理解 Closet 内容，不需要针对特定模型做适配。**

---

## 5. 安装与配置

### 5.1 启动 MCP Server

```bash
pip install mempalace

# 启动 MCP Server（监听默认端口 8765）
mempalace serve
```

### 5.2 Claude Desktop 配置

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "mempalace": {
      "command": "mempalace",
      "args": ["serve", "--stdio"]
    }
  }
}
```

### 5.3 Claude Code 配置

```bash
# 在项目根目录运行
claude mcp add mempalace -- mempalace serve --stdio
```

### 5.4 验证安装

```
claude> /tools
  可用工具：
  ✅ mempalace_status
  ✅ mempalace_search
  ✅ mempalace_save
  ... (共 19 个)
```

---

## 6. "Know Before Speaking" 协议的 MCP 实现

每次调用 `mempalace_status` 时，响应体末尾会附加：

```
⚠️ PROTOCOL: BEFORE RESPONDING about any person, project, or past event:
   call mempalace_kg_query or mempalace_search FIRST.
   Do not rely on training data for questions about this user's history.
```

这是软约束，不是硬锁。但大语言模型在看到 System Prompt 级别的协议指令时，遵从率很高。

这个设计确保 MemPalace 不仅仅是"有了就用"的工具，而是 Agent 工作流中的**强制检查点**。

---

## 7. MCP 层的工程亮点

**无状态 Server**：MCP Server 本身不维护任何会话状态，所有状态在 ChromaDB 和 KG 文件里。这意味着 Server 可以随时重启，不丢失数据。

**工具粒度设计**：19 个工具被刻意设计成小粒度，而不是一个"do everything"工具。这让 AI Agent 能精确表达意图，也让 token 消耗可预测。

**错误友好性**：所有工具返回结构化的错误信息，包含建议的下一步操作（如"该 Wing 不存在，可用 Wing 列表：..."），降低 Agent 的重试成本。

---

*下一篇：[MemPalace 深度解析（七）：Benchmark 深度解析——96.6% 是怎么来的]*
