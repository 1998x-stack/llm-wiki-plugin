---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [agents, delegation, parallelism, AI工程]
aliases: ["子 Agent 系统", "多 Agent 系统", "Sub Agent System", "Multi Agent System"]
relates_to: []
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# 子 Agent 系统

## 概述
[[子 Agent & 多 Agent 系统|子 Agent]] 系统是[[Claude Code]]中的委派层，提供受控并行而非无限递归的能力，通过深度限制防止Agent扩散失控。

## 关键内容

1. **设计原则**：
   - 受控并行，而非无限递归
   - 深度限制：严格禁止Sub-Agent创建Sub-Sub-Agent（深度>1会被阻断）
   - 上下文隔离和并行能力

2. **应用场景**：
   - 并行探索多个实现方案
   - 隔离执行重型探索（不污染主上下文）
   - 专业分工（不同模型处理不同类型工作）

3. **实现机制**：
   - [[Git Worktree]]隔离：子Agent在临时[[Git Worktree]]中执行，防止污染主工作目录
   - [[模型选择]]策略：探索型用[[Claude 3 Haiku|Haiku]]（廉价快速）、实现型用Sonnet（平衡）、架构决策用Opus（最强推理）
   - 并行Agent Teams模式：多个专业Agent并行工作后由Validator汇总结果

## 来源
- [[05_to_08_combined]] — 子 Agent & 多 Agent 系统章节

## 相关
- [[Proactive Agent]] — relates_to
- [[Claude Code]] — relates_to
- [[AgentTool]] — relates_to

## 指令