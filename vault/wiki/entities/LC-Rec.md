---
type: entity
entity_type: project
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 语义ID, ID表示]
aliases: [LC-Rec]
relates_to:
  - {target: P5 论文, type: extends}
  - {target: 语义 ID, type: implements}
  - {target: 生成式 LLM 推荐, type: part_of}
  - {target: Whole-word Embedding, type: compares_to}
supersedes: null
---

# LC-Rec

## 概述
用[[语义 ID|语义标识符]]替代数字 ID 的 LLM 推荐方法，解决了 [[P5 论文|P5]] 的 ID 语义鸿沟问题。

## 关键内容

1. **核心问题**：[[P5 论文]] 使用字面数字 ID（如 "item_1532"）表示物品，这些 ID 本身不携带语义信息，与预训练语言模型的语义空间存在天然鸿沟。

2. **解决方案**：用[[语义 ID|语义标识符]]（semantic identifiers）替代数字 ID，通过量化或聚类方法将物品映射到有意义的语义空间，使 ID 本身携带语义信息。

3. **与[[Whole-word Embedding]]的对比**：[[P5 论文|P5]] 的 [[Whole-word Embedding]] 通过共享[[Whole-word Embedding|全词嵌入]]改善了 ID 表示，但仍然依赖数字 ID。LC-Rec 从根本上用[[语义 ID]] 替代数字 ID，是更彻底的解决方案。

4. **技术优势**：
   - 缓解[[冷启动问题]]：新物品可通过语义描述获得有意义的表示
   - 增强跨域迁移：语义空间比数字 ID 空间更具可迁移性
   - 提升模型理解：语言模型能更好地理解有语义的标识符

5. **在 LLM 推荐谱系中的位置**：属于[[生成式 LLM 推荐]]范式，与 [[LLMRec]]（同时使用唯一标识符和语义文本）共同探索了 ID 表示的最佳实践。

## 来源
- LC-Rec 论文 — Semantic ID for LLM-based Recommendation
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022

## 相关
- [[P5 论文]] — LC-Rec 试图解决的问题来源
- [[语义 ID]] — LC-Rec 的核心技术
- [[生成式 LLM 推荐]] — LC-Rec 所属范式
- [[Whole-word Embedding]] — P5 的 ID 表示方案，LC-Rec 的对比对象
- [[LLMRec]] — 同时使用唯一标识符和语义文本的方案
