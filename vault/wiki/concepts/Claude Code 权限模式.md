---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 2
tags: ["AI工程", "安全性", "权限管理"]
aliases: ["Permission Modes", "权限模式", "Claude Code Permissions"]
relates_to:
  - target: "[[斜杠命令（Slash Commands）]]"
    type: uses
    confidence: 0.7
  - target: "[[Claude Code 插件系统]]"
    type: relates_to
    confidence: 0.6
  - target: "[[Auto Mode 安全分类器]]"
    type: implements
    confidence: 0.9
  - target: "[[Prompt Injection]]"
    type: defends_against
    confidence: 0.85
supersedes: null
---

# Claude Code 权限模式

## 概述
权限模式控制 [[Claude Code]] 可以执行哪些操作，从完全交互式到完全自动化，提供 6 种权限级别：default、acceptEdits、plan、auto、dontAsk、bypassPermissions。

## 关键内容

1. **六种权限模式**：
   - **default**：默认模式，每步操作前确认
   - **acceptEdits**：自动接受文件编辑，但命令执行需确认
   - **plan**：仅规划模式，不执行任何文件修改或命令
   - **auto**：自动模式，由 [[Auto Mode 安全分类器]] 在每一步执行前审查
   - **dontAsk**：不询问模式，自动执行所有操作
   - **bypassPermissions**：绕过所有权限检查，完全自动化

2. **权限管理的核心矛盾**：
   - **安全需要**：修改文件、运行命令、使用 MCP 工具时应征得用户同意
   - **效率需要**：频繁弹窗破坏工作流，用户在第十次审批时已不再认真审查
   - 传统"默认请求权限"模式创造安全假象，而非真正安全

3. **三种模式对比**：
   - **完全允许（--dangerously-allow-all）**：所有操作直接执行，无任何保护
   - **标准模式（默认）**：所有操作弹窗确认，但用户疲劳导致形同虚设
   - **Auto Mode**：分类器评估 → 安全则执行，危险则阻止+报告，有实质性保护

4. **适用场景**：
   - 最适合：明确定义范围的编码任务、已知安全的批量操作、测试和 CI 环境
   - 仍需手动审批：任务范围模糊、涉及生产数据库、与外部服务首次集成

5. **安全的多层次防御**：
   - 第一层：任务范围定义（用户告诉 Agent 要做什么）
   - 第二层：[[Auto Mode 安全分类器]] 评估（独立模型验证操作合规性）
   - 第三层：沙箱限制（OS 级别的文件系统和网络隔离）

## 来源
- [[09-advanced-features/README.md]] — Claude HowTo 高级功能指南
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/15_claude_code_auto_mode.md]] — Claude Code Auto Mode 深度解析

## 相关
- [[斜杠命令（Slash Commands）]] — uses
- [[Claude Code 插件系统]] — relates_to
- [[Auto Mode 安全分类器]] — implements
- [[Prompt Injection]] — defends_against
