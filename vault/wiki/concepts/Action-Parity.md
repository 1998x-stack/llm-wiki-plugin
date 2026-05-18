---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [ai-agent, architecture, design-pattern, AI工程]
aliases: ["Action Parity", "Action-Parity"]
relates_to:
  - target: "[[Agent-Native-Architecture]]"
    type: part_of
    confidence: 0.9
  - target: "[[AI-Agent]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Claude Code Skills]]"
    type: implements
    confidence: 0.85
supersedes: null
---

# Action Parity

## 概述
Action Parity 是 [[Agent-Native-Architecture|Agent-Native Architecture]] 的核心概念之一，指 AI Agent 应具备与人类开发者相同的操作能力。

## 关键内容

1. **定义**：
   - Agent 能执行人类能执行的所有操作
   - 确保 AI Agent 具备完整的操作[[Permissions|权限]]和能力

2. **实现方式**：
   - 工具访问[[Permissions|权限]]（如 Git、文件系统等）
   - 编辑能力（创建、修改、删除文件）
   - 执行能力（运行测试、构建、部署等命令）

3. **重要性**：
   - 防止构建出只能做部分动作的伪自主系统
   - 确保 Agent 可以完成端到端的开发任务

## 来源
- [[raw/articles/ai-engineering/prompt-context/compound-engineering-deep-analysis]]
- [[EveryInc/compound-engineering-plugin]]

## 相关
- [[Agent-Native-Architecture]] — part_of
- [[Context-Parity]] — relates_to
- [[AI-Agent]] — relates_to