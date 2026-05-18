---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, coding-agent, terminal, typescript, Agent系统]
aliases: ["Claude Code", "Claude"]
relates_to:
  - target: "[[TAOR Loop]]"
    type: implements
  - target: "[[Anthropic Messages API]]"
    type: uses
  - target: "[[MCP]]"
    type: uses
  - target: "[[Model Context Protocol]]"
    type: uses
  - target: "[[Boris Cherny]]"
    type: developed_by
supersedes: null
---

# Claude Code

## 概述
Claude Code是运行在终端的自主编码智能体，采用极简Harness设计，结合LLM大脑与真实世界身体（Shell、文件系统、外部服务）。

## 关键内容
1. **产品哲学**：The product is the model - 直接暴露模型能力而不层层包裹，让用户直接感受模型本身。相比传统聊天机器人和工作流产品，Claude Code采用模型驱动的循环，实现第三代自主Agent范式。

2. **技术栈**：使用TypeScript作为主要开发语言，React + Ink作为UI框架，Yoga作为布局引擎，Bun作为构建工具。通过Anthropic Messages API直接接入模型能力，并采用MCP（Model Context Protocol）标准化外部服务接入。

3. **系统架构**：包含用户接口层（CLI、VS Code插件、Web UI）、核心Agent层（nO主循环TAOR - Think→Act→Observe→Repeat）、确定性控制层（21个生命周期事件的Hooks系统）、工具生态系统、配置权限层等多个层次。

4. **四大能力基元**：Read（阅读文件、搜索）、Write（编辑、创建文件）、Execute（执行命令）、Connect（连接外部服务）。其中Bash作为通用适配器，使Claude Code可以使用任何人类开发者会使用的工具。

5. **运营指标**：90%的代码由Claude Code自行编写，每位工程师每天约5次发布，GA后3个月ARR突破500M美元。

## 来源
- [[01_system_overview.md]] — 系统总览与技术栈

## 相关
- [[Anthropic Messages API]] — relates_to
- [[MCP]] — relates_to
- [[TAOR Loop]] — relates_to
- [[Model Context Protocol]] — relates_to