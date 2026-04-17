---
type: entity
entity_type: company
status: active
confidence: 0.75
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [科技公司, 推荐系统, 深度学习]
aliases: [Google Inc., 谷歌]
relates_to:
  - {target: Wide & Deep, type: part_of}
  - {target: YouTube, type: part_of}
supersedes: null
---

# Google

## 概述
全球领先的科技公司，在推荐系统领域贡献了 [[Wide & Deep]] 模型（2016），该模型在 Google Play 应用推荐中服务 10 亿+用户，开创了"[[记忆与泛化]]统一"的推荐[[规范化理论|范式]]。

## 关键内容

1. **[[Wide & Deep]] 的提出者**：2016 年，Google 研究团队（16 位作者，包括 Google Brain 团队的 Greg Corrado）在 [[DLRS 2016]] 发表 [[Wide & Deep]] 论文，提出将线性模型和深度神经网络[[联合训练]]的推荐框架。
2. **Google Play 推荐系统**：[[Wide & Deep]] 在 Google Play 应用商店落地，服务超过 10 亿活跃用户和 100 万+应用，训练数据超 5000 亿条样本，在线 A/B 测试中实现下载率 3.9% 的提升。
3. **工程实践贡献**：Google 不仅提出算法，还完整展示了大规模推荐系统的工程实践——从数据流水线、模型训练（FTRL+L1 / AdaGrad 差异化优化）、热启动机制到在线服务（10ms 内完成打分排序），为工业界提供了可参考的部署[[规范化理论|范式]]。
4. **[[TensorFlow]] 开源**：[[Wide & Deep]] 的实现被集成到 [[TensorFlow]] 中，作为 `tf.estimator.DNNLinearCombinedClassifier` 提供，极大降低了工业界采用深度学习推荐系统的门槛。
5. **其他推荐系统布局**：Google 在推荐系统领域还有 [[YouTube]] 推荐系统等多项重要工作，持续推动深度学习在工业推荐场景中的大规模落地。

## 来源
- Heng-Tze Cheng et al. — Wide & Deep Learning for Recommender Systems, DLRS 2016 (arXiv:1606.07792)

## 相关
- [[Wide & Deep]] — Google 提出的推荐模型
- [[YouTube]] — Google 旗下视频推荐平台
