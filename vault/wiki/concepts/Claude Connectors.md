---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, integration, remote-services, AI工程]
aliases: ["Claude Connectors", "Remote MCP Services"]
relates_to:
  - target: "[[Claude Code]]"
    type: extends
  - target: "[[MCP]]"
    type: part_of
  - target: "[[Slack]]"
    type: integrates_with
  - target: "[[Figma]]"
    type: integrates_with
  - target: "[[Asana]]"
    type: integrates_with
supersedes: null
---

# Claude Connectors

## 概述
[[Claude Code]]的远程MCP[[服务]]，用于连接[[Slack]]、Figma、Asana等SaaS应用，通过OAuth鉴权实现与外部[[服务]]的集成。

## 关键内容

1. **基本特征**：
   - 作为远程MCP[[服务]]运行
   - 连接[[Slack]]、Figma、Asana等SaaS应用
   - 采用OAuth鉴权机制确保安全连接

2. **在扩展机制中的定位**：
   - 与[[MCP|MCP Servers]]同属进程级工具[[服务]]类别
   - 但为远程[[服务]]而非本地进程
   - 是[[Claude Code]]扩展机制全家桶的一部分

3. **与其他扩展机制的关系**：
   - 与[[Agent Skills]]形成对比，[[Skills]]是目录级可复用能力包
   - 与[[MCP|MCP Servers]]相对应，MCP是本地进程级，[[Connect]]ors是远程[[服务]]级

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文

## 相关
- [[Claude Code]] — extends
- [[MCP]] — part_of
- [[Slack]] — integrates_with
- [[Figma]] — integrates_with
- [[Asana]] — integrates_with