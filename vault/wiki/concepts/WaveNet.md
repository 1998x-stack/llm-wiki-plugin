---
type: concept
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [deep-learning, speech, generative-models, audio]
aliases: [WaveNet]
relates_to:
  - target: Aaron van den Oord
    relation: relates_to
  - target: 扩散模型
    relation: influenced
  - target: 空洞卷积
    relation: uses
supersedes: null
---

# WaveNet

## 概述
使用空洞因果卷积直接建模原始音频波形的生成模型，生成高质量语音。

## 关键内容

1. **空洞因果卷积**：使用膨胀卷积扩大[[感受野]]，捕获长距离音频依赖，同时保持因果性。
2. **[[AR 模型（自回归模型）|自回归]]生成**：逐样本生成音频，[[计算]]成本高，但生成质量接近真人水平。
3. **后续影响**：为后续的 [[扩散模型]] 在音频领域的应用奠定基础。

## 来源
- [[ai_papers_timeline.md]] — 2016 年时间线条目

## 相关
- [[Aaron van den Oord]] — relates_to
- [[扩散模型]] — influenced
- [[空洞卷积]] — uses
