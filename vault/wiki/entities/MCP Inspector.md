---
type: entity
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [工具, MCP, 调试, 开发工具]
aliases: ["MCP Inspector", "@modelcontextprotocol/inspector", "MCP调试工具"]
entity_type: tool
relates_to:
  - target: "[[MCP]]"
    type: uses
  - target: "[[MCP协议层]]"
    type: used_by
supersedes: null
---

# MCP Inspector

## 概述
MCP 协议官方调试工具，通过 `npx @modelcontextprotocol/inspector` 启动，用于可视化和调试任意 MCP Server 的工具暴露、资源发现和提示模板。

## 关键内容

1. **定位**：MCP 生态的通用调试客户端，类似 Postman 之于 HTTP API。可以连接任何 MCP Server 并交互式测试其工具、资源和 prompts。

2. **使用方式**：
   ```bash
   # 调试 Codex 作为 MCP Server
   npx @modelcontextprotocol/inspector codex mcp-server
   ```
   Inspector 作为 MCP Client 连接目标 Server，提供 Web UI 展示工具列表、参数 schema、执行结果。

3. **核心功能**：
   - 列出 MCP Server 暴露的所有 tools/resources/prompts
   - 交互式调用工具并查看响应
   - 验证 inputSchema 的正确性
   - 调试 stdio/HTTP/SSE 传输层连接

4. **在开发流程中的角色**：开发 MCP Server 时的标准调试工具，确保工具正确注册、schema 验证通过、响应格式符合协议规范。

## 来源
- [[raw/articles/ai-tools/codex/06_codex_mcp_layer.md]] — Codex MCP Layer 深度解析

## 相关
- [[MCP]] — uses
- [[MCP协议层]] — used_by
- [[Codex CLI]] — uses
