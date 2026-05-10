---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [command-line, shell, adapter-pattern, automation]
aliases: ["Bash适配器", "通用适配器"]
relates_to: 
  - target: "[[Claude Code]]"
    type: relates_to
  - target: "[[Command Line Interface]]"
    type: extends
supersedes: null
---

# Bash通用适配器

## 概述
Bash通用适配器是指在[[Claude Code]]中使用Bash作为通用适配器，使AI系统能够使用任何人类开发者会用的工具，而无需专用集成。

## 关键内容
1. **通用性**：Bash作为通用适配器，让[[Claude Code]]可以使用任何人类开发者会用的工具，包括git、npm、docker、pytest等命令行工具。

2. **无需专用集成**：通过Bash，[[Claude Code]]可以调用现有的命令行工具，而不是为每个外部[[服务]]开发专用的API集成。

3. **在[[Claude Code]]中的作用**：Bash是[[Execute]]能力基元的核心组件，提供持久Shell会话，使得AI可以执行各种系统级操作。

4. **优势**：降低了集成成本，因为无需为每个工具开发专门的接口；同时提供了极大的灵活性，可以访问整个命令行生态。

## 来源
- [[01_system_overview.md]] — 四大能力基元部分

## 相关
- [[Claude Code]] — relates_to
- [[Execute]] — implements
- [[Command Line Interface]] — relates_to