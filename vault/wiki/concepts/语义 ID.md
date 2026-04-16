---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, ID表示, 语义]
aliases: [Semantic ID, 语义标识符]
relates_to:
  - {target: P5 论文, type: compares_to}
  - {target: LC-Rec, type: implements}
  - {target: LLMRec, type: implements}
  - {target: Whole-word Embedding, type: compares_to}
  - {target: 嵌入表示, type: extends}
  - {target: 生成式推荐 (LLM), type: extends}
supersedes: null
---

# 语义 ID

## 概述
用语义标识符或自然语言描述替代传统数字 ID 来表示用户和物品，解决 LLM 推荐中 ID 与语义空间的鸿沟问题。

## 关键内容

1. **问题来源**：[[P5 论文]] 使用字面数字 ID（如 "item_1532"）表示物品，后续研究指出这些 ID 本身不携带语义信息，与预训练语言模型的语义空间存在天然鸿沟，影响模型性能。

2. **[[Whole-word Embedding]] 的局限**：[[P5 论文|P5]] 的 [[Whole-word Embedding]] 虽然通过共享[[Whole-word Embedding|全词嵌入]]改善了 ID 表示，但仍然依赖数字 ID 作为基础，无法从根本上解决语义鸿沟问题。

3. **[[LC-Rec]] 方案**：用语义标识符（semantic identifiers）替代数字 ID，通过量化或聚类方法将物品映射到有意义的语义空间，使 ID 本身携带语义信息。

4. **[[LLMRec]] 方案**：同时使用唯一标识符和语义文本作为物品表示，结合 ID 的精确性和文本的语义性，在保留物品可区分性的同时增强语义理解。

5. **优势**：
   - 缓解[[冷启动问题]]：新物品可通过语义描述获得有意义的表示
   - 增强跨域迁移：语义空间比数字 ID 空间更具可迁移性
   - 提升模型理解：语言模型能更好地理解有语义的标识符

6. **挑战**：语义 ID 的构建质量直接影响推荐效果；语义空间的设计需要权衡区分性和泛化性；大规模物品库的语义 ID 构建成本高。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)
- LC-Rec 论文 — Semantic ID for LLM-based Recommendation

## 相关
- [[P5 论文]] — 使用数字 ID 的开创性工作
- [[LC-Rec]] — 用语义标识符替代数字 ID
- [[LLMRec]] — 同时使用唯一标识符和语义文本
- [[Whole-word Embedding]] — P5 的 ID 表示改进方案
- [[嵌入表示]] — 语义 ID 的理论基础
- [[生成式推荐 (LLM)]] — 语义 ID 服务的范式
