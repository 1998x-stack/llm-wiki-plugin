---
type: entity
entity_type: company
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 视频平台, 深度学习]
aliases: [YouTube, 油管]
relates_to:
  - {target: 矩阵分解, type: uses}
  - {target: Deep Neural Networks for YouTube Recommendations, type: implements}
  - {target: 两阶段推荐架构, type: implements}
  - {target: 双塔模型, type: implements}
  - {target: TensorFlow, type: uses}
supersedes: null
---

# YouTube

## 概述
全球最大视频平台，工业界推荐系统的引领者。从[[矩阵分解]]到深度神经推荐系统，确立了"[[候选生成]] + 排序"的两阶段架构[[规范化理论|范式]]。

## 关键内容

1. **[[矩阵分解]]的工业采用**：Koren 等人 2009 年论文中描述的[[矩阵分解]]方法被 YouTube 等大量工业推荐系统采用或作为重要的[[候选生成]]策略之一。
2. **推荐场景**：YouTube 的推荐场景包括视频推荐、首页信息流、侧边栏推荐等，[[矩阵分解]]为其提供了大规模用户-视频匹配的基础能力。
3. **深度神经推荐系统**：2016年，[[Paul Covington]]、[[Jay Adams]]、[[Emre Sargin]] 在 RecSys 发表 [[Deep Neural Networks for YouTube Recommendations]]，将深度神经网络引入推荐系统，提出"[[候选生成]] + 排序"两阶段架构，将推荐建模为超大规模多分类问题。该论文确立了工业推荐系统的标准架构[[规范化理论|范式]]，影响了全球几乎所有大型推荐系统。
4. **规模与挑战**：2016年的 YouTube 已有超过十亿活跃用户，每分钟数百小时视频上传，推荐系统面临数十亿视频语料库、毫秒级响应要求、内容多样性等前所未有的挑战。
5. **技术基础设施**：使用 [[TensorFlow]] 作为大规模深度学习训练的基础设施，推动了 [[Embedding]] + [[近似最近邻检索]] 检索生态的发展。

## 来源
- [[04-matrix-factorization-for-recsys.md]] — 深度解读 Matrix Factorization Techniques for Recommender Systems
- [[07-youtube-dnn.md]] — Deep Neural Networks for YouTube Recommendations 深度解读

## 相关
- [[矩阵分解]] — 早期采用的推荐技术
- [[Deep Neural Networks for YouTube Recommendations]] — 确立两阶段架构的里程碑论文
- [[两阶段推荐架构]] — YouTube 确立的推荐系统标准范式
- [[双塔模型]] — YouTube DNN 提出的模型原型
- [[Spotify]] — 同样采用 MF 的工业平台
- [[Amazon]] — 同样采用 MF 的工业平台
- [[TensorFlow]] — 使用的训练基础设施
- [[Paul Covington]] — YouTube DNN 论文第一作者
- [[Jay Adams]] — YouTube DNN 论文第二作者
- [[Emre Sargin]] — YouTube DNN 论文第三作者
