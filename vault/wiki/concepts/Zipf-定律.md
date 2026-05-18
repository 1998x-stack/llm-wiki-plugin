---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [context-engineering, distributed-systems, power-laws, AI工程]
aliases: ["齐夫定律", "Zipf's Law"]
relates_to: []
supersedes: null
---

# Zipf-定律

## 概述
Zipf定律是一种经验定律，描述在自然语言中词汇频率分布的规律：在语料库中，一个词的频率与其排名成反比。在Context Design中，Zipf定律指导将上下文按热度分层，实现热/温/冷存储策略。

## 关键内容

1. **数学表述**：
   在一个语料库中，词频与词的排名呈反比关系，即频率最高的词出现次数大约是第二高词的两倍，第三高词的三倍，以此类推。

2. **在Context Design中的应用**：
   基于Zipf/Pareto定律，绝大多数价值来自少数热点上下文，因此需要做热/温/冷分层，而不是所有历史平权处理。这种分层方式能够优化上下文利用率。

3. **实际意义**：
   - 热数据频繁访问，需要快速存取
   - 温数据偶尔访问，可适当延迟
   - 冷数据很少访问，可归档存储

## 来源
- [[raw/articles/ai-engineering/prompt-context/context-design.md]] — 在Context Design中的应用
- [[统计语言学理论]] — 理论基础

## 相关
- [[Context Design]] — applies_to
- [[Pareto-原理]] — relates_to
- [[分层记忆]] — implements