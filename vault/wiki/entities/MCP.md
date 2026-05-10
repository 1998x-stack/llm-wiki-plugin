---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [protocol, integration, standard]
aliases: ["Model Context Protocol", "模型上下文协议"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# MCP

## 概述
[[MCP（Model Context Protocol）]]是[[Claude Code]]连接外部世界的标准化协议，提供统一接口替代碎片化的专用集成方案。

## 关键内容

1. **架构特点**：
   - 客户端（[[Claude Code]]）通过JSON-RPC与[[MCP Prompts|MCP Server]]通信
   - 支持stdio、SSE、HTTP三种传输模式
   - 封装外部[[服务]]访问逻辑（[[GitHub]]、DB、Browser等）

2. **传输模式**：
   - stdio：本地进程原生隔离，不经过网络
   - SSE：远程HTTP流式，实现实时推送
   - HTTP：远程HTTP非流式，简单请求-响应

3. **上下文保护机制**：
   - Tool Search机制仅加载工具名称（极低Token消耗）
   - [[渐进式披露（Progressive Disclosure）|按需加载]]完整工具Schema到上下文
   - [[Settings|设置]]输出Token上限（默认25,000 tokens）

## 来源
- [[05_to_08_combined]] — MCP章节

## 相关
- [[Tool Ecosystem]] — relates_to
- [[配置权限系统]] — relates_to
- [[Claude Code Hooks System]] — relates_to

## 指令