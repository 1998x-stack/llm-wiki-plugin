---
type: entity
status: active
confidence: 0.6
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["person", "ai-engineering", "evaluation"]
aliases: ["Gian Segato"]
relates_to:
  - "[[Anthropic]] — works_at"
  - "[[Terminal-Bench 2.0]] — researches"
  - "[[SWE-bench]] — researches"
supersedes: null
---

# Gian Segato

## 概述
Anthropic 工程师，发表关于 Agentic 编码评测中基础设施噪声量化的研究，揭示了资源配置对 Benchmark 分数的显著影响。

## 关键内容
1. **核心研究**：通过受控实验量化了基础设施配置对 [[SWE-bench]] 和 [[Terminal-Bench 2.0]] 的影响，发现在 Terminal-Bench 2.0 上不同资源配置之间的成功率差距可达 **6 个百分点**（p < 0.01）。
2. **关键发现**：执行方法论会改变 Benchmark 实际测量的内容——资源配置不同的 Agent 实际上在"做不同的测试"。
3. **工程建议**：提出分别规定 Kubernetes 资源的"保证分配"（requests）和"硬性上限"（limits），推荐 3× requests 作为 limits 的起点，可将基础设施错误率降低 2/3。
4. **方法论贡献**：推动 AI 评测领域向工程严谨性靠拢，揭示"模型能力"与"基础设施行为"之间的边界比单一 Benchmark 分数所暗示的更加模糊。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/06_infrastructure_noise.md]] — Quantifying infrastructure noise in agentic coding evals

## 相关
- [[Anthropic]] — works_at（任职于 Anthropic Engineering）
- [[Terminal-Bench 2.0]] — researches（研究该 Benchmark 的基础设施噪声）
- [[SWE-bench]] — researches（进行交叉验证实验）
- [[基础设施噪声]] — authored（提出并量化此概念）
