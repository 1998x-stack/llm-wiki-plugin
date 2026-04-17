---
type: entity
entity_type: project
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 竞赛, 数据集]
aliases: [Netflix Prize, Netflix 大奖赛]
relates_to:
  - {target: Netflix, type: part_of}
  - {target: BellKor, type: compares_to}
  - {target: Cinematch, type: compares_to}
  - {target: 矩阵分解, type: uses}
  - {target: 模型融合, type: uses}
supersedes: null
---

# Netflix Prize

## 概述
[[Netflix]] 2006-2009 年举办的推荐算法竞赛，100 万美元奖金推动[[矩阵分解]]技术崛起，彻底改变了推荐系统领域的发展轨迹。

## 关键内容

1. **竞赛规则**：2006 年 10 月发起，挑战是将 [[Netflix]] 推荐引擎 [[Cinematch]] 的评分预测精度（RMSE）提升 10%。基线 RMSE 为 0.9514，目标为降至 0.8563 以下。公开了 1 亿条评分、48 万用户、17,770 部电影的数据集。
2. **参赛规模**：持续近三年（2006-2009），吸引来自 186 个国家超过 40,000 支队伍参赛，是推荐系统历史上规模最大的公开竞赛。
3. **技术革命**：竞赛暴露了传统近邻[[协同过滤]]的天花板（稀疏度 98.8%），催生了[[隐因子模型]]的崛起。2006 年 12 月 [[Simon Funk]] 博客发表 [[FunkSVD]]，将 RMSE 从 0.9514 降至约 0.896，跃居排行榜第三。
4. **最终结果**：2009 年 9 月，[[BellKor's Pragmatic Chaos]] 团队以 RMSE 0.8567（10.06% 提升）赢得大奖。另一支队伍 "[[The Ensemble]]" 取得完全相同精度，但因晚了 20 分钟提交而失之交臂。
5. **历史影响**：竞赛确立了[[矩阵分解]]作为推荐系统第一范式的地位，其产生的技术洞察被 [[Spotify]]、[[Amazon]]、[[YouTube]] 等工业界广泛采用。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems
- [[05-bpr-bayesian-personalized-ranking.md]] — BPR 论文时代背景提及

## 相关
- [[Netflix]] — 发起方
- [[BellKor]] — 获胜团队
- [[BellKor's Pragmatic Chaos]] — 最终获胜队伍
- [[The Ensemble]] — 并列但迟到的队伍
- [[Cinematch]] — 被超越的基线系统
- [[矩阵分解]] — 竞赛中确立的主导技术
