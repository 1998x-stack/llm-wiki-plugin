---
type: entity
entity_type: project
status: active
confidence: 0.8
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 数据集, 因果推断]
aliases: [Yahoo! R3 Dataset, Yahoo Music R3]
relates_to:
  - {target: Recommendations as Treatments, type: uses}
  - {target: Yahoo Research, type: part_of}
  - {target: MCAR, type: uses}
  - {target: MNAR, type: uses}
  - {target: MF-IPS, type: uses}
supersedes: null
---

# Yahoo! R3

## 概述
Yahoo Music 歌曲评分数据集，同时包含自然评分（MNAR）和随机强制曝光评分（MCAR），是因果推荐研究中验证去偏方法的标准数据集。

## 关键内容

1. **数据来源**：由 [[Yahoo Research]] 收集，包含 Yahoo Music 平台上的用户歌曲评分数据。

2. **独特设计**：数据集同时包含两部分：
   - **自然评分**（MNAR 数据）：用户自然产生的评分，约 30 万条（5400 用户 × 1000 首歌），用于训练
   - **随机评分**（MCAR 数据）：通过随机强制曝光实验收集的评分，约 5.4 万条，作为无偏的 ground truth 用于评估

3. **在因果推荐中的作用**：Yahoo! R3 的独特价值在于同时拥有有偏的训练数据和无偏的测试数据。研究者可以在有偏数据上训练模型，然后在无偏测试数据上评估真实性能，从而验证去偏方法是否真正有效。

4. **在 ICML 2016 论文中的使用**：[[Tobias Schnabel]] 等人在 [[Recommendations as Treatments]] 中使用 Yahoo! R3 验证 [[MF-IPS]] 的效果。[[MF-IPS]] 在该数据集上的 MSE 达到 1.115，接近甚至超过了此前最佳的已发表结果。

5. **与其他数据集的对比**：与 Coat Shopping 数据集类似，Yahoo! R3 也同时拥有 MNAR 和 MCAR 数据。但 Yahoo! R3 规模更大（30 万条 vs Coat 的约 8.7 万条），且来自真实的音乐推荐场景。

## 来源
- [Recommendations as Treatments (Schnabel et al., ICML 2016)](https://arxiv.org/abs/1602.05352)

## 相关
- [[Recommendations as Treatments]] — 首次使用该数据集的论文
- [[Yahoo Research]] — 数据收集机构
- MCAR — 随机评分部分的缺失机制
- MNAR — 自然评分部分的缺失机制
- [[MF-IPS]] — 在该数据集上验证的方法
