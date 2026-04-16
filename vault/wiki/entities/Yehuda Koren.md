---
type: entity
entity_type: person
status: active
confidence: 0.7
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 矩阵分解, 机器学习]
aliases: [Yehuda Koren, 尤达·科伦]
relates_to:
  - {target: Matrix Factorization Techniques for Recommender Systems, type: implements}
  - {target: Factorization Machines, type: compares_to}
  - {target: SVD++, type: implements}
  - {target: Netflix Prize, type: part_of}
  - {target: BellKor, type: part_of}
  - {target: 矩阵分解, type: uses}
supersedes: null
---

# Yehuda Koren

## 概述
推荐系统领域研究者，[[矩阵分解]]技术先驱，[[Netflix Prize]] 冠军团队 [[BellKor]] 核心成员，2009 年发表 [[Matrix Factorization Techniques for Recommender Systems|MF 综述论文]]奠定[[隐因子模型]]范式。

## 关键内容

1. **学术身份**：2009 年任职于 [[Yahoo Research]]，与 [[Robert Bell]]、[[Chris Volinsky]] 共同发表 *[[Matrix Factorization Techniques for Recommender Systems]]*（IEEE Computer, 2009），该论文成为推荐系统领域引用最多的文献之一（[[Google]] Scholar 15,000+）。
2. **[[Netflix Prize]] 贡献**：作为 [[BellKor]] 团队核心成员参与 [[Netflix Prize]] 竞赛，该团队最终于 2009 年 9 月以 [[RMSE]] 0.8567（10.06% 提升）赢得 100 万美元大奖。其[[矩阵分解]]方法是竞赛方案中的绝对主力。
3. **技术贡献**：提出了由简到繁的[[矩阵分解]]建模框架，包括基本 [[矩阵分解|MF]] 模型、Bias 项引入、[[SVD++]]（融合[[隐式反馈]]）、[[timeSVD++]]（时间动态建模）等层层递进的模型变体，构建了推荐系统领域长达十余年的技术基石。
4. **核心洞察**：提出"正确处理时间动态对精度的影响，大于设计更复杂的推荐架构"这一实践智慧，强调对数据特性的尊重优于模型复杂度。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems
- [[06-factorization-machines.md]] — SVD++ 被 FM 框架等价表示，Koren 的隐式反馈融合思想被纳入统一框架

## 相关
- [[Robert Bell]] — 合作者，BellKor 团队成员
- [[Chris Volinsky]] — 合作者，BellKor 团队成员
- [[BellKor]] — 所属团队
- [[Netflix Prize]] — 参与竞赛
- [[Matrix Factorization Techniques for Recommender Systems]] — 第一作者论文
