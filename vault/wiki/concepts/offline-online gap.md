---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 评估, 工业实践, A/B测试]
aliases: [Offline-Online Gap, 离线在线差距, 评估鸿沟]
relates_to:
  - {target: Deep Neural Networks for YouTube Recommendations, type: compares_to}
  - {target: AUC, type: compares_to}
  - {target: NDCG, type: compares_to}
  - {target: 混合推荐系统, type: compares_to}
supersedes: null
---

# offline-online gap

## 概述
推荐系统中离线评估指标与线上 A/B 测试结果不一致的现象，是工业推荐系统研究的核心挑战之一。

## 关键内容

1. **现象描述**：一些在离线评估（offline evaluation）中看起来更好的方案，在线上 A/B 测试（online evaluation）中并不一定更优。离线指标如 [[AUC]]、[[NDCG]]、[[RMSE]] 等的提升，并不总是转化为线上业务指标的提升。

2. **根源分析**：
   - 离线评估无法完全模拟用户的动态行为
   - 推荐结果本身会改变用户行为（反馈循环 / Feedback Loop）
   - 不同的业务指标之间可能存在权衡
   - 离线数据存在[[选择偏差]]（[[选择偏差|Selection Bias]]）和[[位置偏差]]（[[位置偏差|Position Bias]]）

3. **[[Deep Neural Networks for YouTube Recommendations|YouTube DNN]] 的发现**：[[Deep Neural Networks for YouTube Recommendations]] 坦诚地指出了离线指标与在线效果之间的差距。论文特别提到：用"预测未来的一次观看"替代传统的"随机 holdout"来构造训练标签，虽然在离线指标上差异不大，但在线上 A/B 测试中表现显著更好。

4. **论文金句**："The choice of label and input context to the model is challenging to evaluate offline but has a la[[ripgrep|rg]]e impact on live performance."——这句话道出了推荐系统研究中一个最令人沮丧又最重要的事实。

5. **应对策略**：
   - 尽可能使用线上 A/B 测试验证关键决策
   - 设计更接近线上场景的离线评估协议
   - 使用[[因果推断]]方法处理离线数据中的偏差
   - [[Example Age]] 等去偏技术在一定程度上缓解了 offline-online gap

6. **现代视角**：随着 [[因果推断]]、反事实评估（Counterfactual Evaluation）、以及更精细的离线模拟技术的发展，offline-online gap 正在被逐步缩小，但在真实超大规模场景下，在线验证的不可替代性依然存在。

## 来源
- [[07-youtube-dnn.md]] — Deep Neural Networks for YouTube Recommendations 深度解读

## 相关
- [[Deep Neural Networks for YouTube Recommendations]] — 坦诚指出该问题的论文
- [[AUC]] — 常用离线评估指标
- [[NDCG]] — 常用离线评估指标
- [[Example Age]] — 缓解 offline-online gap 的技术之一
- [[A/B 测试]] — 在线验证的金标准
