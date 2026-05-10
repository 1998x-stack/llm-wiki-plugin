---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [ai-tools, agent-patterns]
aliases: ["Ralph Loop 原理", "Loop Mechanism", "外循环机制"]
relates_to:
  - target: "[[Ralph Loop 系统]]"
    type: part_of
  - target: "[[完成信号机制]]"
    type: implements
  - target: "[[状态持久化系统]]"
    type: implements
supersedes: null
---

# Ralph Loop 核心原理

## 概述

[[Ralph Loop]] 核心原理解析了 Bash while 循环 × 全新 Agent 实例 × 文件持久化状态 三位一体的设计哲学，通过每轮清零上下文、文件系统作为唯一真实状态来源、[[双重验证（Dual Verification）|双重验证]][[完成信号机制（Completion Signal）|完成信号]]，实现可预测的自主编码系统。

## 关键内容

1. **一句话定义**：[[Ralph Loop]] = Bash while 循环 × 全新 Agent 实例 × 文件持久化状态。每一轮迭代，一个"无记忆"的新 Agent 启动，读取文件快速定位，做一件事，写回文件，退出。
2. **[[上下文窗口]]的本质问题**：LLM 上下文类似[[计算]]机内存但只有 malloc() 没有 free()，每次工具调用永久占用上下文空间，无法释放，最终导致质量崩溃。
3. **完整执行流程**：外循环（ralph.sh）cat [[CLAUDE.md]] 注入 [[Claude Code]] → 新鲜 Agent 实例执行启动序列 → 实现一个 Story → 输出 `<promise>COMPLETE</promise>` → 外循环检测信号 + 验证 prd.json → 决定是否继续下一轮。
4. **[[完成信号机制（Completion Signal）|完成信号]]机制**：`<promise>COMPLETE</promise>` 采用 XML 标签格式避免误触发，语义上表示 Agent 主动承诺完成。[[双重验证（Dual Verification）|双重验证]]：先检测文本信号，再验证 prd.json 实际状态，防止 Agent 撒谎。
5. **四层持久化**：上次对话历史 → progress.txt 交班日记；之前写的代码细节 → git history 代码快照；测试结果 → prd.json passes 状态；发现的规律约定 → [[项目约定手册|AGENTS.md]] 累积经验手册。
6. **prd.json 作为唯一真实状态来源（Single Source of Truth）**：每个 Story 的生命周期为 passes: false → Agent 实现 + 测试通过 → passes: true → 下一个 Agent 看到并跳过。
7. **[[固定提示栈（Fixed Prompt Stack）|固定提示栈]]的"浪费性重复"**：每次迭代分配完整规范而非仅差异部分，代价是 N tokens × M 次迭代重复分配，收益是零 compaction 风险，每次迭代都从已知良态开始。
8. **停止条件与安全机制**：最大迭代数防止无限运行；[[双重验证（Dual Verification）|双重验证]]防止假完成；Ctrl+C 优雅退出；每次迭代后延迟允许人工检查；日志持久化可追溯。
9. **与传统方案对比**：相比单次长 Session（上下文累积不可控）和多 Agent 并行（协调复杂度高），[[Ralph Loop]] 实现复杂度低（一个 while 循环），可预测性高（确定性坏 → 确定性结果）。

## 来源

- [[raw/articles/ai-tools/ralph-loop/how-the-loop-works.md]] — 完整原理深度解析

## 相关

- [[Ralph Loop 系统]] — part_of
- [[完成信号机制]] — implements
- [[状态持久化系统]] — implements
