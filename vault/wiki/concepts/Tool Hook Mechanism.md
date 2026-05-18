---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, claude-code, tool-system, hooks, AI工程]
aliases: ["PreToolUse Hook", "PostToolUse Hook", "工具钩子机制"]
relates_to: []
supersedes: null
---

# Tool Hook Mechanism

## 概述
[[Claude Code]]中的工具钩子机制，包括PreToolUse Hook和PostToolUse Hook，在工具调用前后执行特定检查和处理逻辑。

## 关键内容

1. **PreToolUse Hook**：
   - 在工具实际执行前进行检查
   - 可以拦截工具执行（exit 2）或放行
   - 用于[[Permissions|权限]]检查、安全过滤、风险评估
   - 阻止不符合条件的工具调用

2. **PostToolUse Hook**：
   - 在工具执行完成后触发
   - 作为质量门（Quality Gate）检查
   - 用于[[Transcript vs Outcome|结果验证]]、日志记录、后续处理
   - 确保工具输出符合预期标准

3. **执行流程**：
   - LLM输出工具调用
   - PreToolUse Hook检查（可能拦截）
   - 工具在[[Claude Code 沙箱机制|沙箱]]环境执行
   - PostToolUse Hook质量检查
   - 结果加入对话历史

## 来源
- [[03 · 工具生态系统（Tool Ecosystem）]] — 钩子机制部分

## 相关
- [[Tool Ecosystem]] — 所属系统
- [[Security Filter Layer]] — 配合使用的安全层