---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 生成模型, 分类]
aliases: [GLLM4Rec, Generative LLM for Recommendation]
relates_to:
  - {target: 生成式推荐 (LLM), type: extends}
  - {target: 判别式 LLM 推荐, type: compares_to}
  - {target: P5 论文, type: part_of}
  - {target: 推荐系统基础模型, type: extends}
supersedes: null
---

# 生成式 LLM 推荐

## 概述
使用大语言模型进行[[生成式推荐]]的范式，通过 LLM 自回归生成推荐结果，是 [[P5 论文|P5]] 范式的 LLM 时代延续。

## 关键内容

1. **范式定义**：生成式 LLM 推荐（GLLM4Rec）使用大语言模型（LLaMA、Mistral、Qwen 等 7B-70B 参数）作为骨干，通过自回归生成推荐结果——物品 ID、推荐列表或推荐理由文本。

2. **与[[判别式 LLM 推荐]]的对比**：Wu 等人的综述将 LLM 推荐方法分为判别式（[[判别式 LLM 推荐|DLLM4Rec]]）和生成式（GLLM4Rec）两大范式。生成式侧重灵活性和可解释性，判别式侧重预测准确性。

3. **与[[生成式推荐 (LLM)]]的关系**：生成式 LLM 推荐是 [[P5 论文|P5]] 开创的[[生成式推荐 (LLM)]]范式在 LLM 时代的延续和升级——从 [[T5]]-small/base（60M-223M）到 LLaMA/Mistral/Qwen（7B-70B），从 Prompt 模板到[[指令调优]]。

4. **现代方案特征**：
   - 骨干模型：LLaMA/Mistral/Qwen（7B-70B）
   - ID 表示：[[语义 ID]] / 自然语言描述 / 多模态特征
   - 训练策略：LoRA/QLoRA 等参数高效微调
   - 任务统一：[[指令调优]]替代 Prompt 模板
   - 推理范式：多阶段检索+生成

5. **代表工作**：[[TALLRec]]（LLaMA 推荐微调）、[[InstructRec]]（[[指令调优]]推荐）、[[LC-Rec]]（[[语义 ID]]）、[[LLMRec]]（双表示）、[[DEALRec]]（数据剪枝）、[[VIP5]]（多模态扩展）。

6. **工业界态度**：工业界对完全替代传统推荐模型持谨慎态度，更多将 LLM 作为推荐系统的辅助组件（特征增强、冷启动解决、用户意图理解）。

## 来源
- Wu et al. — A Survey on Large Language Models for Recommendation, ACM TOIS 2024
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022

## 相关
- [[生成式推荐 (LLM)]] — 生成式 LLM 推荐的范式基础
- [[判别式 LLM 推荐]] — 对立范式
- [[P5 论文]] — 生成式推荐的开创性工作
- [[推荐系统基础模型]] — 生成式 LLM 推荐的愿景
- [[指令调优]] — 生成式 LLM 推荐的训练策略
- [[语义 ID]] — 生成式 LLM 推荐的 ID 表示方案
- [[TALLRec]] — 生成式 LLM 推荐代表工作
- [[InstructRec]] — 生成式 LLM 推荐代表工作
- [[LC-Rec]] — 生成式 LLM 推荐代表工作
- [[LLMRec]] — 生成式 LLM 推荐代表工作
- [[DEALRec]] — 生成式 LLM 推荐代表工作
- [[VIP5]] — 生成式 LLM 推荐代表工作
