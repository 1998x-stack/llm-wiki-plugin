---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 分解模型, 特征交叉, CTR预估]
aliases: [Factorization Machines, FM, 分解机, 因子分解机]
relates_to:
  - {target: Steffen Rendle, type: implements}
  - {target: 矩阵分解, type: extends}
  - {target: SVD++, type: extends}
  - {target: 特征交叉, type: uses}
  - {target: 嵌入表示, type: uses}
  - {target: CTR 预估, type: implements}
  - {target: libFM, type: implements}
  - {target: 隐式反馈, type: uses}
  - {target: Yehuda Koren, type: compares_to}
  - {target: FFM, type: extends}
  - {target: DeepFM, type: extends}
  - {target: Wide & Deep, type: extends}
supersedes: null
---

# Factorization Machines (ICDM 2010)

## 概述
[[Steffen Rendle]] 于 ICDM 2010 发表的论文，提出用[[嵌入表示|隐向量]]内积建模[[特征交叉|特征交互]]的通用预测模型，以线性复杂度解决稀疏数据下的[[特征交叉]]问题，成为 [[CTR 预估]]和推荐系统的基石模型。

## 关键内容

1. **核心公式**：FM 模型由三部分组成：全局偏置 $w_0$、一阶特征权重 $\sum w_i x_i$、二阶[[特征交叉|特征交互]] $\sum_{i<j} \langle \mathbf{v}_i, \mathbf{v}_j \rangle x_i x_j$。通过将交互[[矩阵分解]]为[[嵌入表示|隐向量]]内积，参数量从 $O(n^2)$ 降至 $O(kn)$。
2. **线性复杂度推导**：通过代数变换 $\sum_{i<j} \langle \mathbf{v}_i, \mathbf{v}_j \rangle x_i x_j = \frac{1}{2} \sum_{f=1}^{k} \left( (\sum_i v_{i,f} x_i)^2 - \sum_i v_{i,f}^2 x_i^2 \right)$，将计算复杂度从 $O(kn^2)$ 降至 $O(kn)$，稀疏数据下为 $O(k\bar{n})$。
3. **稀疏数据有效性**：与多项式 SVM 的独立交互参数不同，FM 的[[嵌入表示|隐向量]]通过参数共享机制相互关联，即使特征 $i$ 和 $j$ 从未共现，只要 $\mathbf{v}_i$ 和 $\mathbf{v}_j$ 从其他交互中学到合理表示，FM 仍能预测其交互。
4. **统一框架**：FM 通过不同的特征编码方式可等价表示 [[矩阵分解]]（用户-物品 one-hot 编码）、[[SVD++]]（加入[[隐式反馈]]指示变量）、PI[[TensorFlow|TF]]（用户-物品-标签三元 one-hot）、[[FPMC]] 等专用分解模型，实现了"一个公式统一所有分解模型"。
5. **训练方法**：支持 SGD（大规模在线学习）、[[交替最小二乘法 ALS|ALS]]（回归任务稳定）、MCMC（[[托马斯·贝叶斯|贝叶斯]]推断自动调参）三种优化方法，梯度可在线性时间内计算。
6. **实验验证**：在稀疏[[协同过滤]]数据上显著优于线性 SVM 和多项式核 SVM；在评分预测任务上与 [[矩阵分解|MF]] 性能相当，加入丰富特征编码后可媲美 [[SVD++]]；在 [[Netflix]] 数据集（约1亿条评分）上展示工业级可扩展性。
7. **局限性**：仅支持二阶交叉（高阶 FM 因组合爆炸很少使用）；本质为线性模型，无法学习高度非线性模式；对所有特征对交叉等权处理，无法区分有意义交叉与噪声；[[嵌入表示|隐向量]]维度 $k$ 的选择缺乏理论指导。
8. **历史影响**：直接催生 [[FFM]]（2016）、[[FNN]]（2016）、[[Wide & Deep]]（2016）、[[DeepFM]]（2017）、NFM（2017）、x[[DeepFM]]（2018）、[[AFM]]（2017）等一系列后续工作，是整个 [[CTR 预估]]模型谱系的"始祖"。美团、阿里巴巴、华为、Twitter 等公司在推荐和广告系统中大量使用 FM 及其变体。
9. **与 [[Transformer架构|Transformer]] 的结构相似性**：FM 的交叉项 $\sum_i \sum_j \langle \mathbf{v}_i, \mathbf{v}_j \rangle x_i x_j$ 与 [[Transformer架构|Transformer]] [[自注意力机制]] $\text{softmax}(QK^T/\sqrt{d})V$ 存在结构相似性，都可看作通过"向量内积"衡量元素交互强度。
10. **Rendle 后续贡献**：Rendle 加入 [[Google]] 后，于 2020 年发表 "[[Neural Collaborative Filtering]] vs. [[矩阵分解|Matrix Factorization]] Revisited"，指出精心调优的 [[矩阵分解|MF]]（FM 特例）在多项基准测试上仍可匹敌[[Neural Collaborative Filtering|神经协同过滤]]模型。

## 来源
- [IEEE Xplore](https://ieeexplore.ieee.org/document/5694074/)

## 相关
- [[Steffen Rendle]] — 第一作者
- [[矩阵分解]] — FM 可等价表示的特例
- [[SVD++]] — FM 可等价表示的特例
- [[特征交叉]] — FM 核心建模目标
- [[嵌入表示]] — FM 隐向量的深度学习延伸
- [[CTR 预估]] — FM 主要应用场景
- [[libFM]] — Rendle 开发的 FM 开源实现
- [[隐式反馈]] — SVD++ 通过 FM 编码纳入
- [[FFM]] — FM 的场感知扩展
- [[DeepFM]] — FM + DNN 并行架构
- [[Wide & Deep]] — Wide 部分对应 FM 线性项
