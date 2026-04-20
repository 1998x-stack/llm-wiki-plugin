---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: ["cloud", "kubernetes", "infrastructure", "google"]
aliases: ["GKE", "Google Kubernetes Engine", "Google K8s"]
relates_to:
  - "[[Terminal-Bench 2.0]] — hosts"
  - "[[Anthropic]] — used_by"
  - "[[彩虹部署]] — supports"
supersedes: null
---

# Google Kubernetes Engine (GKE)

## 概述
Google 提供的托管 Kubernetes 服务，用于容器编排和管理，Anthropic 在其 GKE 集群上运行 Agentic 编码评测实验。

## 关键内容
1. **在 AI 评测中的角色**：Anthropic 在 GKE 集群上运行 [[Terminal-Bench 2.0]] 时，发现基础设施错误率高达 6% 的任务因 Pod 错误失败，从而揭示了资源配置对评测结果的影响。
2. **容器资源管理机制**：
   - **requests（保证分配）**：预先保留的资源量
   - **limits（硬性上限）**：超过则触发 [[OOM Kill]] 终止容器
   - 严格执行 requests = limits 配置会导致零余量，任何瞬时资源波动都会导致容器被终止
3. **与沙箱供应商的差异**：Terminal-Bench 官方排行榜的沙箱供应商允许临时超额分配，不立即终止容器，基础设施稳定性更好但评分方式实际上更宽松。
4. **工程建议**：推荐配置 requests 和 limits 之间保持 3× 带宽，如 requests: {cpu: 2, ram: 4GB}，limits: {cpu: 6, ram: 12GB}。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/06_infrastructure_noise.md]] — Quantifying infrastructure noise in agentic coding evals

## 相关
- [[Terminal-Bench 2.0]] — hosts（运行该 Benchmark 的容器环境）
- [[Anthropic]] — used_by（Anthropic 使用 GKE 运行内部评测）
- [[基础设施噪声]] — relates_to（GKE 资源配置是基础设施噪声的主要来源）
- [[OOM Kill]] — triggers（资源超限触发容器终止）
- [[彩虹部署]] — supports（支持 Rainbow Deploy 部署策略）
