---
type: concept
title: MCP 工具集成
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["AI", "MCP", "工具集成", "Agent", "MemPalace", "工具与框架"]
aliases: ["MCP Tool Integration", "MemPalace MCP 工具"]
relates_to:
  - target: "[[MCP]]"
    type: implements
  - target: "[[MemPalace]]"
    type: part_of
  - target: "[[工具注册机制]]"
    type: extends
  - target: "[[KBS 协议]]"
    type: extends
  - target: "[[MCP 层工程亮点]]"
    type: extends
  - target: "[[HTTP 传输协议]]"
    type: uses
    confidence: 0.7
  - target: "[[Stdio 传输协议]]"
    type: uses
    confidence: 0.8
  - target: "[[OAuth 2.0 认证]]"
    type: supports
    confidence: 0.75
  - target: "[[MCPorter]]"
    type: enables
    confidence: 0.7
  - target: "[[渐进式加载]]"
    type: extends
supersedes: null
---

# MCP 工具集成

## 概述
通过 [[MCP|Model Context Protocol]] 将记忆系统的能力暴露为 AI Agent 可调用的工具。[[MemPalace]] 提供 19 个 MCP 工具，使 Agent 能够查询、导航和操作[[记忆宫殿]]。

## 关键内容
- **规模**：[[MemPalace|MemPalace v3.0.0]] 提供 19 个 MCP 工具，按功能分为 6 组
- **Group 1 状态与导航（3 个）**：`mempalace_status`（全局状态 + [[KBS 协议]]注入）、`mempalace_wing_detail`（Level 2 加载）、`mempalace_room_detail`（Level 3 加载 + Closet）——实现[[渐进式加载]]
- **Group 2 搜索（2 个）**：`mempalace_search`（全文语义搜索，底层调用 [[ChromaDB]] 向量搜索，支持 wing/room 范围过滤）、`mempalace_kg_query`（知识图谱实体查询，用于"某个事实的历史变化"类问题）
- **Group 3 写入（4 个）**：`mempalace_save`（通用写入）、`mempalace_save_decision`（快捷保存决策，自动路由到 decisions Hall）、`mempalace_save_preference`（快捷保存偏好）、`mempalace_kg_update`（更新知识图谱实体状态）
- **Group 4 [[隧道跨域连接|Tunnel]] 发现（1 个）**：`mempalace_tunnel_explore`（探索当前 Room 的跨域连接）
- **Group 5 日记（2 个）**：`mempalace_diary_write`（写入带时间戳日记）、`mempalace_diary_read`（读取最近 N 条日记）——为长期运行 Agent 提供持久化工作日志
- **Group 6 管理工具（7 个）**：`mempalace_list_wings`、`mempalace_list_rooms`、`mempalace_delete`、`mempalace_update`、`mempalace_export`、`mempalace_stats`、`mempalace_rebuild_index`
- **[[Claude Code]] Auto-save**：会话结束时自动调用 `mempalace_save` 保存关键决策和代码变更摘要，通过 `.claude/settings.json` [[Configuration|配置]] triggers（session_end, important_decision）
- **跨模型兼容**：支持 [[Claude_Code|Claude]]（原生）、GPT-4o（API 适配）、[[Gemini CLI|Gemini]]（API 适配）、Llama（[[Ollama]] MCP 插件）、Mistral（API 适配）
- **[[KBS 协议]]**：`mempalace_status` 响应末尾附加 "[[Know Before Speaking 协议|Know Before Speaking]]" 协议指令，强制 Agent 先检索再回答
- **价值**：将记忆系统从被动存储升级为 Agent 可主动使用的工具集

### 典型调用流示例

```
用户问题：为什么我们的 API 要限制每分钟 100 次请求？

Step 1: mempalace_status → 收到 Palace 地图 + KBS 协议
Step 2: mempalace_search → ChromaDB 向量搜索，缩小到 my_app 翼，返回 Top-3 Drawer
Step 3: 读取 Drawer → 找到 2025-09-15 的对话记录（DDoS 压测 + SLA 原因）
Step 4: Agent 回答 → 带完整推理链的答案，标注来源位置
```

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 系列总览篇
- [[raw/articles/ai-tools/mempalace/mempalace_06_mcp_tools.md]] — MemPalace 深度解析第六篇：MCP 工具集成

## 相关
- [[MCP]] — implements
- [[MemPalace]] — part_of
- [[工具注册机制]] — extends
- [[KBS 协议]] — extends
- [[MCP 层工程亮点]] — extends
- [[渐进式加载]] — extends
