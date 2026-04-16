---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 生成模型, 范式, P5]
aliases: [Recommendation as Language Processing, RLP, LLM-based Generative Recommendation]
relates_to:
  - {target: P5 论文, type: part_of}
  - {target: 生成式推荐, type: compares_to}
  - {target: 推荐系统基础模型, type: extends}
  - {target: 协同过滤, type: compares_to}
  - {target: 矩阵分解, type: compares_to}
  - {target: 序列推荐, type: extends}
  - {target: T5, type: uses}
  - {target: 判别式 LLM 推荐, type: compares_to}
  - {target: 生成式 LLM 推荐, type: part_of}
supersedes: null
---

# 生成式推荐 (LLM)

## 概述
将推荐任务重构为文本生成问题的 LLM 范式，通过语言模型[[AR 模型（自回归模型）|自回归]]生成推荐结果，由 [[P5 论文]]首次系统性提出。

## 关键内容

1. **范式定义**：将推荐系统的所有任务——评分预测、[[序列推荐]]、解释生成、评论摘要、直接推荐——统一为"输入一段文本，输出一段文本"的语言生成问题，不再需要专门的[[协同过滤]]层、评分预测头或排序损失函数。

2. **开创性工作**：[[P5 论文]]（[[RecSys 2022]]）首次系统性地论证了"将推荐系统完全重构为语言处理任务"的可行性，使用 [[T5]] 作为骨干模型，将五大推荐任务完整统一到一个语言模型框架中。

3. **与 [[Meta]] [[生成式推荐]]的区别**：[[Meta]] 的[[生成式推荐]]（[[HSTU]]）将推荐重新定义为端到端序列生成任务，预测用户下一个交互 token（内容+动作），侧重工业级大规模部署。本概念特指基于 LLM 的[[生成式推荐]]，用自然语言 Prompt 驱动推荐，侧重多任务统一和可解释性。

4. **核心能力**：
   - **多任务统一**：从数值回归（评分预测）到二分类（是否推荐）到序列排序再到开放式文本生成
   - **[[Zero-shot 推荐]]**：面对未见过的 Prompt 格式仍能给出合理推荐
   - **可解释性融合**：推荐和解释在同一模型中共享知识
   - **跨域迁移**：一个领域预训练的模型可迁移到其他领域

5. **技术挑战**：推理效率（[[AR 模型（自回归模型）|自回归]]解码延迟远高于向量内积）；物品词汇表可扩展性（百万/亿级 ID 空间）；ID 语义鸿沟（数字 ID 与语言模型语义空间脱节）。

6. **后续演进**：从 [[P5 论文|P5]]（2022，[[T5]]-small/base 60M-223M）到现代方案（2024-2025，LLaMA/Mistral/Qwen 7B-70B），从 Prompt 模板到[[指令调优]]，从数字 ID 到[[语义 ID]]，从全参数微调到 Lo[[rust-analyzer|RA]]/QLo[[rust-analyzer|RA]] 参数高效微调。

7. **学术共识**：[[P5 论文|P5]] 帮助社区形成了"语言是连接不同推荐任务的天然桥梁"的重要共识，使"LLM for Recommendation"从小众方向迅速成长为推荐系统领域最热门的研究主题。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)
- Wu et al. — A Survey on Large Language Models for Recommendation, ACM TOIS 2024

## 相关
- [[P5 论文]] — LLM 生成式推荐的开创性工作
- [[生成式推荐]] — Meta HSTU 的序列生成范式（不同概念）
- [[推荐系统基础模型]] — LLM 生成式推荐的终极愿景
- [[协同过滤]] — 传统推荐范式
- [[矩阵分解]] — 传统推荐范式
- [[序列推荐]] — LLM 生成式推荐统一的任务之一
- [[T5]] — P5 使用的骨干模型
- [[判别式 LLM 推荐]] — LLM 推荐的另一范式
- [[生成式 LLM 推荐]] — LLM 生成式推荐的现代延续
- [[Zero-shot 推荐]] — LLM 生成式推荐的独特能力
- [[指令调优]] — 现代 LLM 生成式推荐的训练策略
- [[语义 ID]] — 解决 LLM 生成式推荐的 ID 表示问题
