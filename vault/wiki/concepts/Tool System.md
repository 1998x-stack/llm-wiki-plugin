---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI工具, 代码助手, 智能体系统, 工具系统]
aliases: ["Tool System", "Tools"]
relates_to: 
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[AgentTool]]"
    type: contains
  - target: "[[BashTool]]"
    type: contains
  - target: "[[FileReadTool]]"
    type: contains
  - target: "[[FileWriteTool]]"
    type: contains
  - target: "[[WebFetchTool]]"
    type: contains
  - target: "[[WebSearchTool]]"
    type: contains
supersedes: null
---

# Tool System

## 概述
[[Claude Code]]内置的工具系统，包含40+个工具，分为文件系统工具、代码执行工具、网络API工具、多智能体工具、Git版本控制工具和记忆状态工具等多个类别。

## 关键内容
1. **文件系统工具**：包括FileReadTool（读取文件）、File[[Write]]Tool（写入文件）、FileEditTool（精确编辑文件）、FileDeleteTool（删除文件）、DirectoryListTool（列出目录内容）、FileSearchTool（全局文件搜索）、[[GrepTool]]（内容搜索）等。

2. **代码执行工具**：包括[[BashTool]]（执行Shell命令）、NodeTool（执行Node.js代码片段）、[[Python]]Tool（执行[[Python]]代码片段）等，其中[[BashTool]]有专门的安全子系统。

3. **网络与API工具**：包括WebFetchTool（获取网页内容）和WebSearchTool（搜索网络）。

4. **多智能体工具**：包括[[AgentTool]]（生成子Agent）、TaskTool（创建并管理后台任务）、CoordinatorTool（协调多个[[Worker Agent]]）。

5. **Git与版本控制工具**：包括GitCommitTool（创建[[commit]]）、GitDiffTool（查看diff）、GitLogTool（查看提交历史）、PRReviewTool（[[代码审查]]辅助）。

6. **记忆与状态工具**：包括MemoryReadTool（读取[[MEMORY.md]]及topic files）、Memory[[Write]]Tool（更新记忆索引）、TodoReadTool（读取任务列表）、[[TodoWrite-Tool|TodoWrite]]Tool（更新任务列表）。

7. **工具架构**：所有工具都遵循统一的Schema设计，使用Zod进行运行时类型验证，包含name、description、inputSchema、needsPermission、execute、formatResult等关键组件。

## 来源
- [[Claude Code 源码泄露深度解析（二）：核心 Agent 引擎与 40+ 工具系统]] — 全文

## 相关
- [[Claude Code]] — part_of
- [[AgentTool]] — relates_to
- [[BashTool]] — relates_to
- [[Zod]] — uses