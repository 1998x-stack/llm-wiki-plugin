---
type: concept
status: active
confidence: 0.5
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 排序学习, 隐式反馈, 贝叶斯方法]
aliases: [BPR, Bayesian Personalized Ranking, BPR 排序, 贝叶斯个性化排序]
relates_to:
  - {target: 协同过滤, type: extends}
  - {target: 矩阵分解, type: implements}
  - {target: 隐式反馈, type: depends_on}
  - {target: Pointwise 学习, type: compares_to}
  - {target: 负采样, type: uses}
  - {target: AUC, type: relates_to}
  - {target: BPR 论文, type: relates_to}
supersedes: null
---

# BPR (Bayesian Personalized Ranking)

## 概述
一种基于[[托马斯·贝叶斯|贝叶斯]]最大后验估计的 pairwise 学习框架，将[[隐式反馈]]推荐问题从评分预测重新定义为个性化偏好排序学习。

## 关键内容

1. **核心思想**：不预测用户对物品的绝对分数，而是学习物品之间的相对偏好排序。对于用户交互过的物品 i 和未交互的物品 j，假设 i >_u j，通过大量 pairwise 比较推导全局排名。

2. **数学推导**：基于[[托马斯·贝叶斯|贝叶斯]] MAP 推导，使用 logistic sigmoid 函数建模偏好似然 p(i >_u j | Θ) = σ(x̂_uij)，施加零均值高斯先验 p(Θ)，得到目标函数 B[[Probabilistic Robotics|PR]]-OPT = Σ ln σ(x̂_uij) - λ‖Θ‖²。

3. **与 [[AUC]] 的等价性**：B[[Probabilistic Robotics|PR]]-OPT 是 [[AUC]] 的可微光滑近似（用 ln σ(x) 替代 Heaviside 阶跃函数），优化 B[[Probabilistic Robotics|PR]] 近似等价于直接优化排序质量。

4. **LearnB[[Probabilistic Robotics|PR]] 算法**：采用 bootstrap 随机采样三元组 (u, i, j) 的 SGD 算法，相比按用户遍历的梯度下降收敛更快、随时可停、梯度估计更均匀。

5. **模型无关性**：B[[Probabilistic Robotics|PR]] 是通用优化准则，可与任何产生评分预测的模型结合，如 B[[Probabilistic Robotics|PR]]-[[矩阵分解|MF]]（[[矩阵分解]]）和 B[[Probabilistic Robotics|PR]]-kNN（自适应 k 近邻）。

6. **局限性**：均匀[[负采样]]信息量低、仅考虑 pairwise 无法建模全局排序、继承[[协同过滤]]的[[冷启动问题]]、对交互行为的假设过于粗糙。

7. **历史影响**：2009年发表后成为[[隐式反馈]]推荐的标准范式，B[[Probabilistic Robotics|PR]] Loss 至今仍是 LightGCN、Neu[[矩阵分解|MF]]、[[DeepFM]] 等模型的核心训练目标，6000+ 引用量。

8. **与[[对比学习]]的关系**：B[[Probabilistic Robotics|PR]] 可理解为[[对比学习]]的早期实践，当 [[InfoNCE]] 损失只使用一个负样本时退化为 B[[Probabilistic Robotics|PR]] Loss。现代图[[对比学习]]推荐模型通常组合 L_B[[Probabilistic Robotics|PR]] + λ·L_CL。

## 来源
- [[BPR 论文]] — Rendle et al. (2009) UAI 2009, BPR 原始论文

## 相关
- [[协同过滤]] — extends
- [[矩阵分解]] — implements
- [[隐式反馈]] — depends_on
- [[Pointwise 学习]] — compares_to
- [[负采样]] — uses
- [[AUC]] — relates_to
- [[BPR 论文]] — relates_to
