---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["ai-engineering", "evaluation", "统计", "非确定性"]
aliases: ["pass@k", "pass^k", "pass at k", "pass to the k"]
relates_to:
  - target: "[[Agent 评测体系]]"
    type: part_of
  - target: "[[评测驱动开发]]"
    type: uses
supersedes: null
---

# pass@k vs pass^k

## 概述
pass@k 和 pass^k 是处理 Agent 非确定性的两种核心统计指标，分别衡量"至少一次成功"和"所有次均成功"的概率，适用于不同的业务场景。

## 关键内容

1. **pass@k（至少一次成功）**：
   - 公式：P(至少一次成功 | k 次尝试)
   - k 增大 → 分数升高
   - 适用于：允许多次重试的场景、代码生成（找到一个有效解就够）
   - 直观理解：给 Agent 多次机会，只要有一次成功就算通过

2. **pass^k（所有次均成功）**：
   - 公式：P(全部成功 | k 次尝试) = p^k（p 为单次成功率）
   - k 增大 → 分数下降
   - 适用于：**面向用户的 Agent**——用户期望每次可靠
   - 直观理解：Agent 必须每次都成功，不容许失败

3. **直观数字对比**（单次成功率 75%）：
   - pass@1 = 75%
   - pass^3 = (0.75)³ ≈ 42%
   - pass@10 → 接近 100%
   - pass^10 = (0.75)^10 ≈ 6%
   - 两者在 k=1 时相同，k 增大后说的是完全相反的故事

4. **选择指南**：
   - **代码生成/搜索任务**：用 pass@k（找到一个解就够）
   - **面向用户的对话/操作 Agent**：用 pass^k（用户期望每次可靠）
   - **内部工具/可重试场景**：用 pass@k
   - **生产环境/不可重试场景**：用 pass^k

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 非确定性处理章节

## 相关
- [[Agent 评测体系]] — part_of（非确定性处理是评测体系的核心组成部分）
- [[评测驱动开发]] — uses（pass@k/pass^k 是评测指标选择的关键决策）
- [[LLM-as-Judge]] — relates_to（LLM 评分器也面临非确定性问题）
