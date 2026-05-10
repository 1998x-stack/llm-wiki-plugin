---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [paper, deep-learning, speech, generative-models]
aliases: [van den Oord et al. 2016]
relates_to:
  - target: Aaron van den Oord
    relation: authored_by
  - target: WaveNet
    relation: introduced
  - target: 扩散模型
    relation: influenced
supersedes: null
---

# WaveNet: A Generative Model for Raw Audio (2016 论文)

## 概述
提出 [[WaveNet]] 音频生成模型的论文，使用空洞因果卷积直接建模原始音频波形。

## 关键内容

1. **空洞因果卷积**：使用膨胀卷积扩大[[感受野]]，捕获长距离音频依赖，同时保持因果性（不依赖未来样本）。
2. **高质量语音**：[[WaveNet]] 生成的语音质量远超当时的参数化方法，接近真人水平。
3. **[[AR 模型（自回归模型）|自回归]]生成**：逐样本生成音频，[[计算]]成本高，这一局限后来被 [[扩散模型]] 和并行生成方法部分解决。

## 来源
- [[ai_papers_timeline.md]] — 2016 年时间线条目

## 相关
- [[Aaron van den Oord]] — authored_by
- [[WaveNet]] — introduced
- [[扩散模型]] — influenced
