---
type: concept
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [kubernetes, container, resource-management, reliability, AI工程]
aliases: ["OOM Kill", Out of Memory Kill, 内存溢出终止]
relates_to:
  - "[[Google Kubernetes Engine (GKE)]] — mechanism_of"
  - "[[基础设施噪声]] — contributes_to"
  - "[[Token 资源管理]] — relates_to"
supersedes: null
---

# OOM Kill

## 概述
Kubernetes 容器资源管理机制，当容器内存使用超过 limits 硬性上限时，系统立即终止该容器，是 Agentic 编码评测中基础设施错误的主要来源。

## 关键内容
1. **触发机制**：Linux 容器资源有两个参数——requests（保证分配，预先保留）和 limits（硬性上限）。当容器内存使用超过 limits 时，触发 OOM Kill，容器被立即终止。
2. **在 Agentic 评测中的影响**：
   - 严格执行 requests = limits [[Configuration|配置]]（零余量）时，任何瞬时资源波动超过上限都会导致容器被终止
   - 在 [[Terminal-Bench 2.0]] 的 1x [[Configuration|配置]]下，多达 6% 的任务因 Pod 错误（含 OOM Kill）失败
   - 增加到 3x [[Configuration|配置]]后，基础设施错误率降至 2.1%（降低 63%，p < 0.001）
3. **与解题能力的混淆**：大多数 Pod 错误与模型解题能力无关，而是容器资源问题导致的。一个任务因 OOM Kill 失败，不代表 Agent 无法解决该问题。
4. **[[Claude Code 沙箱机制|沙箱]]供应商差异**：[[Terminal-Bench]] 官方排行榜的[[Claude Code 沙箱机制|沙箱]]供应商允许临时超额分配，不立即终止容器，基础设施稳定性更好但评分方式实际上更宽松。
5. **缓解策略**：推荐[[Configuration|配置]] requests 和 limits 之间保持 3× 带宽，如 RAM requests: 4GB，limits: 12GB，为瞬时资源波动提供余量。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/06_infrastructure_noise.md]] — Quantifying infrastructure noise in agentic coding evals

## 相关
- [[Google Kubernetes Engine (GKE)]] — mechanism_of（GKE 的容器资源管理机制）
- [[基础设施噪声]] — contributes_to（OOM Kill 是基础设施错误的主要来源）
- [[Terminal-Bench 2.0]] — affects（导致 Terminal-Bench 任务因 Pod 错误失败）
- [[Token 资源管理]] — relates_to（同属资源管理范畴，但层级不同）
