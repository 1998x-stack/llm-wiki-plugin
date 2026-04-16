---
type: entity
entity_type: person
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 4
tags: [推荐系统, 分解模型, 机器学习, CTR预估]
aliases: [Steffen Rendle, 施特芬·伦德勒]
relates_to:
  - {target: Factorization Machines, type: implements}
  - {target: libFM, type: implements}
  - {target: 矩阵分解, type: extends}
  - {target: PITF, type: implements}
  - {target: FPMC, type: implements}
  - {target: Google, type: part_of}
  - {target: University of Konstanz, type: part_of}
  - {target: Yehuda Koren, type: compares_to}
supersedes: null
---

# Steffen Rendle

## 概述
德国康斯坦茨大学计算机科学家，[[Factorization Machines]] ([[Factorization Machines|FM]]) 提出者，开源工具 [[libFM]] 和 xLearn 的开发者，后加入 [[Google]] 继续推动推荐系统研究。

## 关键内容

1. **[[Factorization Machines]] (2010)**：在 ICDM 2010 发表 [[Factorization Machines|FM]] 论文（28,000+ 引用，截至2026年），提出用[[嵌入表示|隐向量]]内积建模[[特征交叉|特征交互]]的通用预测模型，以线性复杂度解决稀疏数据下的[[特征交叉]]问题，统一了[[矩阵分解]]、[[SVD++]]、PI[[TensorFlow|TF]]、[[FPMC]] 等专用分解模型。
2. **[[libFM]] 开发**：开发并开源 [[libFM]] 库，实现了 [[Factorization Machines|FM]] 的 SGD、[[交替最小二乘法 ALS|ALS]]、MCMC 三种优化方法，极大推动了 [[Factorization Machines|FM]] 在工业界的普及和应用。后续发表 *[[Factorization Machines]] with [[libFM]]*（ACM T[[重要性采样|IS]]T, 2012）。
3. **PI[[TensorFlow|TF]] (2010)**：与 Schmidt-Thieme 合作提出 Pairwise Interaction Tensor Factorization，针对标签推荐任务的成对交互张量分解模型，后被证明可被 [[Factorization Machines|FM]] 框架等价表示。
4. **[[FPMC]] (2010)**：提出 Fusion of [[矩阵分解|Matrix Factorization]] and [[马尔可夫链|Markov Chain]]s，融合[[马尔可夫链]]和[[矩阵分解]]的[[序列推荐]]模型，同样被纳入 [[Factorization Machines|FM]] 统一框架。
5. **[[Google]] 时期**：后加入 [[Google]] 继续推荐系统研究。2020 年发表 "[[Neural Collaborative Filtering]] vs. [[矩阵分解|Matrix Factorization]] Revisited"，指出精心调优的[[矩阵分解]]（[[Factorization Machines|FM]] 特例）在多项基准测试上仍可匹敌甚至超过[[Neural Collaborative Filtering|神经协同过滤]]模型，提醒业界不要低估简单模型的力量。
6. **核心洞察**："The interactions of a factorization machine are not independent but they depend on each other."——参数分解打破独立性假设，让模型在从未见过的特征组合上做出合理预测，这一思想与深度学习中的权重共享、参数绑定等技术一脉相承。
7. **学术影响**：[[Factorization Machines|FM]] 论文仅6页篇幅却改变了整个推荐系统和 [[CTR 预估]]领域的格局，后续几乎所有重要的[[特征交叉|特征交互]]模型（[[FFM]]、[[DeepFM]]、x[[DeepFM]]、[[Wide & Deep]] 等）都直接或间接继承了 [[Factorization Machines|FM]] 的思想。

## 来源
- [Factorization Machines (Rendle 2010)](https://arxiv.org/abs/1209.3994)
- [Factorization Machines with libFM (Rendle 2012)](https://doi.org/10.1145/2168752.2168771)
- [NeuCF vs Matrix Factorization Revisited (Rendle 2020)](https://arxiv.org/abs/2005.09683)
- [BPR: Bayesian Personalized Ranking (Rendle et al. 2009)](https://arxiv.org/abs/1205.2618)

## 相关
- [[Factorization Machines]] — 代表作
- [[libFM]] — 开发的开源工具
- [[PITF]] — 合作提出的标签推荐模型
- [[FPMC]] — 合作提出的序列推荐模型
- [[Google]] — 后期任职机构
- [[University of Konstanz]] — FM 发表时任职机构
- [[Yehuda Koren]] — 同时期推荐系统领域重要研究者
