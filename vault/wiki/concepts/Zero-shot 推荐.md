---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 泛化能力, Prompt]
aliases: [Zero-shot Recommendation, 零样本推荐]
relates_to:
  - {target: P5 论文, type: part_of}
  - {target: 生成式推荐, type: extends}
  - {target: 个性化 Prompt, type: uses}
  - {target: 冷启动问题, type: compares_to}
supersedes: null
---

# Zero-shot 推荐

## 概述
模型在面对从未见过的 Prompt 格式或推荐场景时仍能给出合理推荐的能力，由 [[P5 论文]]首次在推荐系统中系统展示。

## 关键内容

1. **概念定义**：Zero-shot 推荐指模型在训练阶段未见过特定 Prompt 模板或任务格式的情况下，仅凭对语言的理解自行组织合适的对话来完成推荐任务的能力。这是传统推荐模型完全不具备的。

2. **P5 中的验证**：[[P5 论文]] 设计了 47 个[[个性化 Prompt]] 模板覆盖五类任务家族，采用部分采样训练策略——对每条原始数据只采样部分 Prompt 模板进行训练，保留一些模板作为 zero-shot 评估使用。实验证明，无论使用训练中见过的还是未见过的 Prompt 模板，P5 都能取得相近的性能。

3. **与传统[[冷启动问题]]的区别**：[[冷启动问题]]关注新用户/新物品缺乏交互历史时的推荐，而 zero-shot 推荐关注模型对新任务格式/新 Prompt 的泛化能力，两者解决的是不同层面的泛化问题。

4. **实现机制**：通过多样化措辞的 Prompt 模板训练增强模型鲁棒性；语言作为统一媒介使模型能够理解未见过的任务描述；预训练语言模型本身的 zero-shot 能力迁移到推荐场景。

5. **意义**：暗示了一种更灵活、更可扩展的推荐交互方式的可能性——用户可以用自然语言描述新的推荐需求，模型无需重新训练即可适配。

6. **后续发展**：现代 LLM 推荐方案（如 [[TALLRec]]、[[InstructRec]]）通过[[指令调优]]进一步增强了 zero-shot 能力，使模型能够遵循更复杂的指令完成推荐任务。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)

## 相关
- [[P5 论文]] — 首次系统展示 zero-shot 推荐能力
- [[生成式推荐]] — zero-shot 推荐的范式基础
- [[个性化 Prompt]] — zero-shot 推荐的技术手段
- [[冷启动问题]] — 不同层面的泛化问题
- [[指令调优]] — 进一步增强 zero-shot 能力的方法
- [[TALLRec]] — 展示 zero-shot 能力的 LLM 推荐工作
- [[InstructRec]] — 通过指令调优增强 zero-shot 能力
