---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["工具", "MCP", "文档检索", "开发工具", "工具与框架"]
aliases: ["Context7", "Context7 MCP Server", "@upstash/context7-mcp"]
entity_type: tool
relates_to:
  - target: "[[MCP]]"
    type: implements
  - target: "[[MCP协议层]]"
    type: used_by
  - target: "[[Codex CLI]]"
    type: used_by
supersedes: null
---

# Context7

## 概述
由 Upstash 开发的 MCP 服务器工具，为 AI Agent 提供实时文档检索能力，通过 `npx @upstash/context7-mcp` 启动，支持代码示例和 API 文档的按需查询。

## 关键内容

1. **定位**：Context7 是一个 MCP Server，专注于为 L[[LM Agent]] 提供最新、准确的库和框架文档。解决训练数据过时问题，让 Agent 能查询任意库的当前 API。

2. **使用方式**：
   ```toml
   [mcp_servers.context7]
   command = "npx"
   args = ["-y", "@upstash/context7-mcp@latest"]
   enabled = true
   ```
   通过 stdio 传输协议运行，Codex 启动时自动连接并发现其工具。

3. **典型工具**：暴露 `search_docs`、`get_code_examples` 等工具，Agent 可在推理时按需查询任何库的文档。

4. **在 Codex 中的角色**：作为 config.toml 中声明的 MCP 服务器之一，启动时被 Codex 的 MCP Client 连接，其工具清单通过 `tools/list` 接口获取并注入 LLM 的 system prompt。

## 来源
- [[raw/articles/ai-tools/codex/06_codex_mcp_layer.md]] — Codex MCP Layer 深度解析

## 相关
- [[MCP]] — implements
- [[MCP协议层]] — used_by
- [[Codex CLI]] — used_by
- [[Upstash]] — part_of
