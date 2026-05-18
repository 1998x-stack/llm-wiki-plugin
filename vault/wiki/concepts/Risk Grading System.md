---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, claude-code, tool-system, risk-management, AI工程]
aliases: ["风险分级系统", "Risk Grading System"]
relates_to: []
supersedes: null
---

# Risk Grading System

## 概述
[[Claude Code]]中对Bash命令执行的风险评估机制，根据命令潜在影响程度分为不同风险等级，决定是否需要用户确认。

## 关键内容

1. **风险等级划分**：
   - **LOW风险**：git status, ls, cat file.py → 自动执行，无需确认
   - **MEDIUM风险**：[[Git Commit|git commit]], npm install → 如在白名单中自动执行，否则提示确认
   - **HIGH风险**：rm -rf, DROP TABLE, git push --force → 始终要求用户明确确认
   - **BLOCK级**：rm -rf /, DROP TABLE users → [[Tool Hook Mechanism|PreToolUse Hook]]直接阻止

2. **执行策略**：
   - 低风险命令可自动执行
   - 中等风险命令依据白名单状态决定
   - 高风险命令始终需要人工确认
   - 封禁级命令会被钩子完全拦截

3. **安全控制**：
   - 与[[Tool Hook Mechanism|PreToolUse Hook]]配合工作
   - 提供安全保障的同时维持工作效率

## 来源
- [[03 · 工具生态系统（Tool Ecosystem）]] — 风险分级部分

## 相关
- [[Tool Ecosystem]] — 所属系统
- [[BashTool]] — 应用场景
- [[Security Filter Layer]] — 相关安全措施