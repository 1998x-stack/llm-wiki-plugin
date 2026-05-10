---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [capability-primitives, ai-actions, coding-agent]
aliases: ["Claude Code四大能力基元", "四大能力基元"]
relates_to: 
  - target: "[[Claude Code]]"
    type: extends
  - target: "[[Read]]"
    type: part_of
  - target: "[[Write]]"
    type: part_of
  - target: "[[Execute]]"
    type: part_of
  - target: "[[Connect]]"
    type: part_of
supersedes: null
---

# Claude Code四大能力基元

## 概述
[[Claude Code]]的四大能力基元是构成其核心功能的四种基本操作能力：Read（读）、[[Write]]（写）、[[Execute]]（执行）、[[Connect]]（连接），这些基元共同构成了AI编码代理的能力基础。

## 关键内容
1. **Read（读）**：包括View、LS、Glob、[[GrepTool]]等工具，用于理解代码库和搜索文件。这是AI获取信息和理解上下文的基础能力。

2. **[[Write]]（写）**：包括Edit、[[Write]]/Replace、Create等工具，支持patch、全文替换和新建文件等功能。这使AI能够修改和创建代码。

3. **[[Execute]]（执行）**：主要是Bash（持久Shell会话），用于执行git、npm、docker、pytest等各种命令。这赋予AI运行时操作能力。

4. **[[Connect]]（连接）**：通过[[MCP（Model Context Protocol）|MCP协议]]连接到[[GitHub]]、DB、Sentry、[[Slack]]等外部[[服务]]。这使AI能够与外部系统交互。

5. **组合效应**：这四大能力基元的组合使[[Claude Code]]能够完成复杂的编程任务，从理解现有代码到修改、测试直至部署。

## 来源
- [[01_system_overview.md]] — 四大能力基元部分

## 相关
- [[Claude Code]] — extends
- [[Read]] — part_of
- [[Write]] — part_of
- [[Execute]] — part_of
- [[Connect]] — part_of