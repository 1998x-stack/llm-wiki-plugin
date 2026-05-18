---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [architecture-pattern, agent-system, loop-pattern, AI工程]
aliases: ["TAOR Loop", "nO 主循环", "Think-Act-Observe-Repeat"]
relates_to:
  - target: "[[Claude Code]]"
    type: implemented_by
  - target: "[[Agent Loop]]"
    type: pattern_type
  - target: "[[Control Loop]]"
    type: related_pattern
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# TAOR Loop

## 概述
TAOR Loop（Think → Act → Observe → Repeat）是 [[Claude Code]] 的核心[[游戏主循环模式|主循环]]模式，是一种模型驱动的控制循环，用于实现自主 AI 代理的行为。

## 关键内容
1. **四个阶段**：
   - **Think**：分析当前状态和上下文，制定计划或决策
   - **Act**：执行具体的操作，如调用工具、修改文件、运行命令
   - **Observe**：观察行动的结果和[[环境反馈设计|环境反馈]]
   - **Repeat**：重复循环过程，继续处理下一个决策点

2. **架构特征**：
   - 单线程执行
   - 扁平消息历史
   - h2A 实时转向缓冲队列（human-to-Agent）

3. **设计优势**：
   - 使模型能够自主控制执行流程
   - 提供连续的感知-行动循环
   - 支持基于[[环境反馈设计|环境反馈]]的自适应行为

4. **应用场景**：在 [[Claude Code]] 中作为 [[nO 主循环]]，驱动整个 AI 代理的运行，使其能够自主地完成编码任务。

## 来源
- [[01_system_overview.md]] — Claude Code 系统总览

## 相关
- [[Claude Code]] — implemented_by
- [[Agent Loop]] — pattern_type
- [[Control Loop]] — related_pattern

## 指令