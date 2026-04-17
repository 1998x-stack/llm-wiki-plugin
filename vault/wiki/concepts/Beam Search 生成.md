---
type: concept
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, LLM, 推理, 解码, LLM能力]
aliases: [Beam Search Generation, Beam Search 解码]
relates_to:
  - {target: P5 论文, type: uses}
  - {target: 生成式推荐 (LLM), type: part_of}
  - {target: T5, type: uses}
  - {target: 采样 Softmax, type: compares_to}
supersedes: null
---

# Beam Search 生成

## 概述
[[P5 论文]]使用的推理方法，通过 beam size=20 的束搜索[[AR 模型（自回归模型）|自回归]]生成物品 ID 或文本，是 LLM 推荐的核心推理[[规范化理论|范式]]。

## 关键内容

1. **在 P5 中的应用**：[[P5 论文]] 在推理阶段使用 beam search（beam size=20）进行解码生成，根据不同任务的 Prompt 格式生成评分数值、物品 ID、解释文本或评论摘要。

2. **工作原理**：Beam Search 维护 beam_size 个候选序列，每一步扩展所有候选序列并保留概率最高的 beam_size 个，平衡了贪婪搜索的短视和穷举搜索的计算复杂度。

3. **与传统推荐的对比**：传统推荐模型的推理是向量内积计算（O(1) 或 O(log N) 通过 [[近似最近邻检索]]），而 Beam Search 生成需要[[AR 模型（自回归模型）|自回归]]解码（O(L) 步，L 为生成序列长度），推理延迟远高于传统方法。

4. **与[[采样 Softmax]]的关系**：[[采样 Softmax]] 是[[两阶段推荐架构]][[候选生成]]阶段的加速技术，用于在大规模物品空间中高效采样。Beam Search 生成是 LLM 推荐的推理方式，两者服务于不同的推荐[[规范化理论|范式]]。

5. **局限性**：对于工业级推荐系统，Beam Search 生成的推理延迟可能是不可接受的。这促使工业界更多将 LLM 作为推荐系统的辅助组件而非完全替代传统模型。

6. **现代演进**：现代 LLM 推荐方案探索多阶段检索+生成的推理[[规范化理论|范式]]，结合传统推荐模型的效率和 LLM 的语义理解能力。

## 来源
- Shijie Geng et al. — P5: Recommendation as Language Processing, RecSys 2022 (arXiv:2203.13366)

## 相关
- [[P5 论文]] — 使用 Beam Search 生成的论文
- [[生成式推荐 (LLM)]] — Beam Search 生成的服务范式
- T5 — 使用 Beam Search 的骨干模型
- [[采样 Softmax]] — 传统推荐的候选生成加速技术
- [[近似最近邻检索]] — 传统推荐的推理加速方法
