---
type: concept
status: active
confidence: 0.75
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Agent工程, 验证, 客观性, 测试, AI工程]
aliases:
- Ground Truth 验证
- 地面真值验证
- 客观事实验证
relates_to:
- target: '[[测试驱动的 Agent 工程]]'
  type: part_of
  confidence: 0.95
- target: '[[SWE-bench]]'
  type: uses
  confidence: 0.9
- target: '[[评测驱动开发]]'
  type: part_of
  confidence: 0.8
supersedes: null
---

# Ground Truth 验证

## 概述
Ground Truth 验证是一种利用客观事实（如测试通过/失败）而非模型自我评判来评估 Agent 进展的方法，避免 LLM "自信但错误"的问题。

## 关键内容

1. **核心问题**：LLM 经常表现出"自信但错误"的行为——对自己的输出高度自信，但实际可能完全错误。Ground Truth 验证通过引入客观标准来解决这一问题。

2. **在 [[SWE-bench]] 中的应用**：[[SWE-bench]] 任务中，测试套件自动验证生成的补丁是否能通过所有测试。测试结果提供了不可辩驳的 ground truth——通过或不通过，没有主观判断空间。

3. **反馈循环价值**：
   - Agent 生成补丁 → 运行测试 → 获得 ground truth 反馈 → 调整策略
   - 这种循环让 Agent 能客观评估自己的进展，而非依赖自我评判
   - 测试结果可直接用于引导 Agent 的下一步行动

4. **与模型自我评判的对比**：
   - 模型自我评判：主观、可能错误、无法[[区分]]"看起来对"和"实际对"
   - Ground Truth 验证：客观、可重复、直接反映正确性

5. **推广场景**：任何有自动化验证机制的场景都可应用 Ground Truth 验证——代码测试、数据验证、格式检查等。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — 测试驱动 Agent 反馈循环分析

## 相关

- [[测试驱动的 Agent 工程]] — part_of（Ground Truth 验证是测试驱动 Agent 工程的核心机制）
- [[SWE-bench]] — uses（SWE-bench 利用测试套件提供 ground truth）
- [[评测驱动开发]] — part_of（客观验证是评测体系的基础）
