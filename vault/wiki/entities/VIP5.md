---
type: entity
entity_type: project
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 多模态, 视觉]
aliases: [VIP5]
relates_to:
  - {target: P5 论文, type: extends}
  - {target: 生成式推荐 (LLM), type: extends}
  - {target: T5, type: uses}
supersedes: null
---

# VIP5

## 概述
将 P5 扩展到多模态（视觉+语言）推荐场景的工作，在 P5 的语言统一基础上增加视觉模态。

## 关键内容

1. **核心思想**：将 [[P5 论文]] 的"[[生成式推荐 (LLM)|Recommendation as Language Processing]]"范式扩展到多模态场景，同时处理视觉和语言信息，实现多模态推荐的统一框架。

2. **与 P5 的关系**：VIP5 是 P5 作者团队自己推出的扩展工作，在 P5 的语言统一基础上增加视觉模态，使模型能够同时理解物品的文本描述和视觉特征。

3. **技术特点**：
   - 在 P5 的 47 个 Prompt 模板基础上增加视觉相关的模板
   - 使用多模态编码器处理图像和文本输入
   - 保持 P5 的"一个模型、一个损失函数、一个数据格式"哲学

4. **应用场景**：适用于需要视觉理解的推荐场景，如时尚推荐、家居推荐、艺术品推荐等，其中物品的视觉特征对推荐决策至关重要。

5. **在 LLM 推荐谱系中的位置**：代表了 P5 范式向多模态方向的扩展，与 [[InstructRec]]、[[TALLRec]] 等纯文本方向的演进形成互补。

## 来源
- VIP5 论文 — Multimodal Extension of P5 for Recommendation
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022

## 相关
- [[P5 论文]] — VIP5 的基础论文
- [[生成式推荐 (LLM)]] — VIP5 扩展的范式
- T5 — VIP5 使用的骨干模型
- [[InstructRec]] — 同期的 P5 后续工作
- [[TALLRec]] — 同期的 P5 后续工作
