---
type: project
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [AI工程, 评测基准, Agent]
aliases:
- τ-Bench
- tau-bench
- Tau Benchmark
relates_to:
- target: '[[Think 工具]]'
  type: uses
  confidence: 0.9
- target: '[[SWE-bench]]'
  type: compares_to
  confidence: 0.85
- target: '[[Agent 架构与设计原则]]'
  type: uses
  confidence: 0.8
- target: '[[Anthropic]]'
  type: part_of
  confidence: 0.85
supersedes: null
---

# τ-Bench

## 概述
τ-Bench（tau-bench）是专为测试 LLM 在真实客服场景中使用工具能力而设计的评测基准，评估对话真实性、策略遵从性和工具使用三个核心维度。

## 关键内容

### 评测框架设计

τ-Bench 专为测试 LLM 在真实客服场景中使用工具的能力而设计，评估三个核心能力：
1. **与模拟用户进行真实对话**
2. **一致地遵循复杂客服策略指南**
3. **使用各种工具访问和操作环境数据库**

包含两个主要领域：
- **航空域**：策略复杂，涉及航班取消、改签、退票等多重规则验证
- **零售域**：策略相对简单，涉及订单查询、退换货等常规操作

### 关键评估指标：pass^k

不同于 pass@k（k 次中至少一次成功），pass^k 衡量**k 次独立试验全部成功**的概率。这种指标在客服场景中更有意义——**一致性比偶发成功更重要**。

### τ-Bench 航空域结果

| 配置 | k=1 | k=2 | k=3 | k=5 |
|------|-----|-----|-----|-----|
| 基准（无 think，无 ET） | 0.332 | 0.206 | 0.148 | 0.100 |
| Extended Thinking | 0.412 | 0.290 | 0.232 | 0.160 |
| Think 工具（无 prompt 优化） | 0.404 | 0.254 | 0.186 | 0.100 |
| **Think 工具 + 优化 prompt** | **0.584** | **0.444** | **0.384** | **0.340** |

核心发现：
1. Think + 优化 prompt 在航空域的改进远超 Extended Thinking
2. 单独 Extended Thinking 和单独 Think 工具性能相近
3. **Prompt 优化是航空域的关键杠杆**——策略越复杂，示例越重要

### τ-Bench 零售域结果

| 配置 | k=1 | k=2 | k=5 |
|------|-----|-----|-----|
| 基准 | 0.783 | 0.695 | 0.583 |
| Extended Thinking | 0.770 | 0.681 | 0.548 |
| **Think 工具（无 prompt 优化）** | **0.812** | **0.735** | **0.626** |

有趣的不对称性：零售域策略相对简单，仅凭 Think 工具（无 prompt 优化）就超过了基准和 Extended Thinking。这说明策略简单时，提供思考空间本身就足够；策略复杂时，还需要示例引导思考方向。

### 与 SWE-bench 的对比

| 维度 | τ-Bench | SWE-bench |
|------|---------|-----------|
| 评估对象 | 客服场景 Agent | 软件工程 Agent |
| 核心能力 | 对话 + 策略遵从 + 工具使用 | 代码理解 + Bug 修复 |
| 指标 | pass^k（一致性） | pass@1（单次成功） |
| 场景特点 | 顺序决策、策略密集 | 静态代码分析、测试验证 |

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/03_think_tool.md]] — The "think" tool: Enabling Claude to stop and think in complex tool use situations
- [τ-Bench 论文](https://arxiv.org/abs/2406.12045) — 客服场景 Agent 评测基准

## 相关

- [[Think 工具]] — uses（τ-Bench 是评估 Think 工具效果的主要基准，航空域提升 54%）
- [[SWE-bench]] — compares_to（不同的评测维度：τ-Bench 测客服策略，SWE-bench 测代码修复）
- [[Agent 架构与设计原则]] — uses（τ-Bench 验证了 Agent 在真实场景中的工具使用能力）
- [[Anthropic]] — part_of（τ-Bench 被 Anthropic 用于验证 Claude 的 Agent 能力）
