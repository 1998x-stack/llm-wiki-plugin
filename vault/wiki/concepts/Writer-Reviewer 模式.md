---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [AI工程, Claude Code, 代码审查, 多Agent系统, 最佳实践]
aliases:
- Writer/Reviewer Pattern
- Writer/Reviewer 模式
- 编写者-审查者模式
- 双会话审查模式
relates_to:
  - target: '[[多 Agent 系统]]'
    type: part_of
    confidence: 0.9
  - target: '[[子 Agent 模式（Sub-Agent Pattern）]]'
    type: compares_to
    confidence: 0.8
  - target: '[[上下文窗口]]'
    type: depends_on
    confidence: 0.85
  - target: '[[上下文经济学]]'
    type: part_of
    confidence: 0.8
supersedes: null
---

# Writer/Reviewer 模式（Writer/Reviewer Pattern）

## 概述
[[Write]]r/Reviewer 模式是一种利用两个独立 [[Claude Code]] 会话进行代码编写和审查的并行工作模式，通过分离实现与审查上下文来提高代码质量。

## 关键内容

1. **基本架构**：
   - **会话 A（[[Write]]r）**：负责实现功能，如"实现 API 限流[[ROS (Robot Operating System)|中间件]]"
   - **会话 B（Reviewer）**：独立审查 [[Write]]r 的产出，如"审查 @src/middleware/rateLimiter.ts，寻找边界情况、竞争条件"
   - [[Write]]r 根据 Reviewer 的反馈进行修复，形成迭代循环

2. **上下文隔离优势**：两个会话拥有独立的 [[上下文窗口]]，[[Write]]r 的实现上下文不会污染 Reviewer 的审查视角。这避免了单一会话中"自己审查自己代码"的盲点。

3. **与 [[子 Agent 模式（Sub-Agent Pattern）]] 的区别**：
   - [[子 Agent 模式（Sub-Agent Pattern）|子 Agent 模式]]是主从关系——主 Agent 派发任务给[[子 Agent & 多 Agent 系统|子 Agent]]，[[子 Agent & 多 Agent 系统|子 Agent]] 返回摘要
   - [[Write]]r/Reviewer 是平等关系——两个会话独立运行，可以并行启动，互不依赖

4. **与 [[多 Agent 系统]] 的关系**：[[Write]]r/Reviewer 模式是 [[多 Agent 系统]] 的一种具体实现形态，属于双 Agent 协作的最简形态。更复杂的[[多 Agent 系统]]可以扩展为 [[Write]]r → Reviewer → Approver 的三阶段流水线。

5. **适用场景**：
   - 关键代码路径的审查（安全相关、性能敏感）
   - 复杂逻辑的边界情况发现
   - 需要独立视角的架构决策审查

6. **[[上下文经济学]]意义**：通过分离写入和审查上下文，避免了在单一会话中同时加载实现细节和审查标准导致的上下文过载，是 [[上下文经济学]] 的具体实践。

## 来源
- [[08_claude_code_best_practices.md]] — Anthropic 官方 Claude Code 最佳实践指南

## 相关
- [[多 Agent 系统]] — part_of（是多 Agent 协作的一种具体形态）
- [[子 Agent 模式（Sub-Agent Pattern）]] — compares_to（主从派发 vs 平等协作）
- [[上下文窗口]] — depends_on（依赖独立上下文实现视角隔离）
- [[上下文经济学]] — part_of（通过上下文分离提高审查质量）
