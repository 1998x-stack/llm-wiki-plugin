---
type: entity
entity_type: project
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 基准平台, 开源]
aliases: [OpenP5, Open P5]
relates_to:
  - {target: P5 论文, type: extends}
  - {target: Shijie Geng, type: part_of}
  - {target: Yongfeng Zhang, type: part_of}
  - {target: 生成式推荐 (LLM), type: implements}
supersedes: null
---

# OpenP5

## 概述
P5 作者团队推出的标准化基准平台，方便后续研究者在 P5 范式下进行公平对比实验。

## 关键内容

1. **项目背景**：[[P5 论文]] 发表后，大量后续工作涌现，但缺乏统一的开发和评估框架，导致基准测试和结果对比面临诸多不确定性。OpenP5 旨在解决这一可复现性问题。

2. **核心功能**：提供标准化的数据预处理、Prompt 模板管理、训练流程和评估指标，使不同研究者可以在相同条件下对比实验结果。

3. **与 P5 的关系**：由 [[Shijie Geng]] 和 [[Yongfeng Zhang]] 团队开发，是 P5 范式的官方基准实现，支持 P5 的五大任务家族和 47 个 Prompt 模板。

4. **学术影响**：为 LLM 推荐系统这一快速发展的新领域提供了可复现性基础设施，被后续工作广泛引用和采用。

5. **局限性**：一项发表于 RecSys 2024 的研究专门探讨了 P5 的可复现性问题，指出即使在 OpenP5 框架下，由于 LLM 推荐系统的快速发展，基准测试和结果对比仍面临诸多不确定性。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)
- GitHub: github.com/agiresearch/OpenP5

## 相关
- [[P5 论文]] — OpenP5 的基础论文
- [[Shijie Geng]] — OpenP5 的开发者
- [[Yongfeng Zhang]] — OpenP5 的开发者
- [[生成式推荐 (LLM)]] — OpenP5 实现的范式
