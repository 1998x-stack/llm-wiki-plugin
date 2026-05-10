---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, Prompt, 个性化]
aliases: [Personalized Prompt, 个性化提示]
relates_to:
  - {target: P5 论文, type: part_of}
  - {target: 生成式推荐 (LLM), type: extends}
  - {target: Zero-shot 推荐, type: enables}
  - {target: T5, type: uses}
supersedes: null
---

# 个性化 Prompt

## 概述
[[P5 论文]]提出的核心技术，将用户ID、物品ID、交互历史等个性化信息转化为自然语言序列嵌入 Prompt 模板中。

## 关键内容

1. **核心原则**：将所有个性化信息（用户ID、物品ID、交互历史、评分、评论文本）转化为自然语言序列，嵌入到 Prompt 模板中，使[[Language-Model|语言模型]]能够同时理解任务描述和用户/物品的个性化特征。

2. **模板设计策略**：
   - **多样化措辞**：同一任务设计多个不同措辞的 Prompt 模板，增强模型鲁棒性
   - **部分采样训练**：对每条原始数据只采样部分 Prompt 模板进行训练，保留一些模板作为 [[Zero-shot 推荐]] 评估使用
   - **[[负采样]]策略**：在[[序列推荐]]和直接推荐任务中，随机采样负样本物品填充到需要候选列表的 Prompt 中
   - **混合训练**：预训练阶段将所有任务家族的输入-输出对混合在一起进行[[多任务学习]]

3. **示例模板**：
   - 评分预测："Which star rating will user_15 give item_25? (1 being lowest and 5 being highest)" → "3"
   - [[序列推荐]]："User_32 has purchased item_21, item_45, item_78 in order. What is the next item the user will purchase?" → "item_92"
   - 解释生成："Generate an explanation for user_15 about why item_25 is recommended." → 自然语言解释
   - 直接推荐："Will user_15 like item_25? Yes or No?" → "Yes"

4. **47个 Prompt 模板**：P5 设计了总计 47 个个性化 Prompt 模板，覆盖评分预测、[[序列推荐]]、解释生成、评论摘要、直接推荐五个任务家族。

5. **与[[指令调优]]的关系**：Prompt 模板是 P5（2022）时代的任务统一方式，后续工作如 [[InstructRec]] 和 [[TALLRec]] 转向[[指令调优]]（[[指令调优|Instruction Tuning]]），用更灵活的指令格式替代固定模板。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)

## 相关
- [[P5 论文]] — 提出个性化 Prompt 的论文
- [[生成式推荐 (LLM)]] — 个性化 Prompt 服务的范式
- [[Zero-shot 推荐]] — 个性化 Prompt 部分采样训练带来的能力
- T5 — 使用个性化 Prompt 的骨干模型
- [[指令调优]] — 替代 Prompt 模板的现代方法
- [[InstructRec]] — 使用指令调优的后续工作
- [[TALLRec]] — 使用指令调优的后续工作
