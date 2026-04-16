---
type: entity
entity_type: project
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 双表示, ID]
aliases: [LLMRec]
relates_to:
  - {target: P5 论文, type: extends}
  - {target: 语义 ID, type: implements}
  - {target: 生成式 LLM 推荐, type: part_of}
  - {target: LC-Rec, type: compares_to}
supersedes: null
---

# LLMRec

## 概述
同时使用唯一标识符和语义文本作为物品表示的 LLM 推荐方法，结合 ID 精确性和文本语义性。

## 关键内容

1. **核心思想**：同时使用唯一标识符（unique identifiers）和语义文本（semantic text）作为物品表示，结合 ID 的精确区分能力和文本的语义理解能力。

2. **与[[LC-Rec]]的对比**：[[LC-Rec]] 用[[语义 ID|语义标识符]]完全替代数字 ID，LLMRec 则保留两者——ID 确保物品的可区分性，文本增强语义理解。

3. **技术优势**：
   - 保留 ID 的精确性：每个物品有唯一标识符，避免[[语义 ID]] 可能的歧义
   - 增强语义理解：文本描述帮助语言模型理解物品特征
   - 更好的冷启动处理：新物品可通过文本描述获得有意义的表示

4. **在 LLM 推荐谱系中的位置**：属于[[生成式 LLM 推荐]]范式，与 [[LC-Rec]] 共同探索了 ID 表示的最佳实践，代表了两种不同的语义化路径。

## 来源
- LLMRec 论文 — LLM-based Recommendation with Dual Representation
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022

## 相关
- [[P5 论文]] — LLMRec 的思想来源
- [[语义 ID]] — LLMRec 使用的语义表示技术
- [[生成式 LLM 推荐]] — LLMRec 所属范式
- [[LC-Rec]] — 用语义标识符替代数字 ID 的对比方案
