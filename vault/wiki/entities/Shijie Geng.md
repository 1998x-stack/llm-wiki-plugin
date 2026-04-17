---
type: entity
entity_type: person
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 研究者]
aliases: [Shijie Geng, 耿世杰]
relates_to:
  - {target: P5 论文, type: part_of}
  - {target: Yongfeng Zhang, type: part_of}
  - {target: OpenP5, type: part_of}
  - {target: Rutgers University, type: part_of}
supersedes: null
---

# Shijie Geng

## 概述
[[P5 论文]]第一作者，[[Rutgers University]] 研究者，提出了将推荐系统统一为语言处理任务的开创性范式。

## 关键内容

1. **[[P5 论文]]第一作者**：2022 年作为第一作者发表 "[[生成式推荐 (LLM)|Recommendation as Language Processing]] (RLP): A Unified Pretrain, [[个性化 Prompt|Personalized Prompt]] & Predict Paradigm (P5)"，发表于 [[RecSys 2022]]，该论文被选为杰出论文之一，引用量 545+。

2. **核心贡献**：首次系统性地论证了"将推荐系统完全重构为语言处理任务"的可行性，将五大推荐任务（评分预测、[[序列推荐]]、解释生成、评论摘要、直接推荐）统一到一个基于 T5 的语言模型框架中。

3. **后续工作**：领导开发了 [[OpenP5]] 标准化基准平台，方便后续研究者在 P5 范式下进行公平对比实验。

4. **学术影响**：P5 工作帮助推荐系统社区形成了"语言是连接不同推荐任务的天然桥梁"的重要共识，直接催生了 LLM for Recommendation 这一热门研究方向。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)

## 相关
- [[P5 论文]] — 第一作者的开创性论文
- [[Yongfeng Zhang]] — 通讯作者/合作者
- [[OpenP5]] — 后续标准化基准平台
- [[Rutgers University]] — 所属机构
- T5 — P5 使用的骨干模型
