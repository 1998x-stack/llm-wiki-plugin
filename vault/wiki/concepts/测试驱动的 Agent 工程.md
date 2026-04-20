---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Agent工程, 测试, 反馈循环, SWE-bench]
aliases:
- 测试驱动的 Agent 工程
- Test-Driven Agent Engineering
- 测试驱动 Agent 开发
relates_to:
- target: '[[SWE-bench]]'
  type: implements
  confidence: 0.95
- target: '[[评测驱动开发]]'
  type: extends
  confidence: 0.9
- target: '[[Ground Truth 验证]]'
  type: uses
  confidence: 0.9
supersedes: null
---

# 测试驱动的 Agent 工程

## 概述
测试驱动的 Agent 工程是一种利用自动化测试为 Agent 提供客观反馈的开发方法论，形成"生成→测试→分析→修改→重试"的闭环反馈循环。

## 关键内容

1. **核心反馈循环**：
   ```
   生成补丁 → 运行测试 → 分析失败原因 → 修改策略 → 重试
   ```
   SWE-bench 任务的独特优势是代码解决方案可以通过自动化测试验证，形成理想的 Agent 反馈循环。

2. **Ground Truth 验证**：测试结果提供了"ground truth"，让 Agent 能够客观评估自己的进展，而不是依赖模型的自我评判。这避免了 LLM 常见的"自信但错误"的问题。

3. **与评测驱动开发的关系**：测试驱动的 Agent 工程是 [[评测驱动开发]] 方法论在 Agent 开发场景的具体应用，将传统 TDD 理念扩展到 AI Agent 行为。

4. **工程建议**：
   - **测试先行**：为 Agent 提供验证机制，避免 Agent 自我评判
   - 测试结果作为客观反馈信号，指导 Agent 迭代策略
   - 测试覆盖率直接影响 Agent 能可靠完成的任务范围

5. **实践价值**：这种方法论不仅适用于 SWE-bench，也可推广到任何有自动化测试可用场景——Agent 可以通过测试反馈自主修正错误，减少对人工干预的依赖。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — 测试驱动的 Agent 工程分析

## 相关

- [[SWE-bench]] — implements（SWE-bench 是测试驱动 Agent 工程的典型应用场景）
- [[评测驱动开发]] — extends（测试驱动是评测驱动在 Agent 场景的延伸）
- [[Ground Truth 验证]] — uses（测试结果为 Agent 提供 ground truth 反馈）
