---
type: entity
entity_type: project
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 竞赛团队, 矩阵分解]
aliases: [BellKor]
relates_to:
  - {target: Netflix Prize, type: part_of}
  - {target: Yehuda Koren, type: part_of}
  - {target: Robert Bell, type: part_of}
  - {target: Chris Volinsky, type: part_of}
  - {target: 矩阵分解, type: uses}
supersedes: null
---

# BellKor

## 概述
[[Netflix Prize]] 竞赛传奇团队，由 [[Yehuda Koren]]、[[Robert Bell]]、[[Chris Volinsky]] 组成，队名融合三人姓氏，最终赢得 100 万美元大奖。

## 关键内容

1. **团队组成**：BellKor 队名由三位核心成员姓氏融合而成——Bell（[[Robert Bell]], AT&T Labs）+ Kor（[[Yehuda Koren]], [[Yahoo Research]]）。[[Chris Volinsky]]（AT&T Labs）也是核心成员。
2. **竞赛历程**：
   - 2007 年获得 Progress Prize（[[RMSE]] 0.8712，8.43% 提升）
   - 2008 年以 "[[BellKor in BigChaos]]" 身份参赛（[[RMSE]] 0.8616，约 9.4% 提升）
   - 2009 年 9 月以 "[[BellKor's Pragmatic Chaos]]" 身份最终获胜（[[RMSE]] 0.8567，10.06% 提升）
3. **技术方案**：方案融合了超过 100 个模型，其中[[矩阵分解]]方法是绝对主力。融合了[[矩阵分解]]、近邻方法、受限玻尔兹曼机等多种模型进行集成。
4. **历史地位**：BellKor 团队的工作将 [[Netflix Prize]] 竞赛中的实战经验升华为系统化的学术知识，其核心方法论通过 Koren 等人 2009 年 IEEE Computer 论文传播至整个计算机科学界。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems

## 相关
- [[Netflix Prize]] — 参与竞赛
- [[Yehuda Koren]] — 核心成员
- [[Robert Bell]] — 核心成员
- [[Chris Volinsky]] — 核心成员
- [[BellKor's Pragmatic Chaos]] — 最终获胜队伍名
- [[BellKor in BigChaos]] — 2008 年队伍名
- [[矩阵分解]] — 核心技术
