---
type: entity
entity_type: paper
status: active
confidence: 0.95
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 多任务学习, KDD, 顶会论文]
aliases: [Modeling Task Relationships in Multi-task Learning with Multi-gate Mixture-of-Experts]
relates_to: [MMoE, 多任务学习, 负迁移, Mixture-of-Experts, PLE, ESMM]
supersedes: null
---

# MMoE 论文

## 概述
KDD 2018 发表的奠基性论文，提出 MMoE 架构解决[[多任务学习]]中的[[负迁移]]问题，成为推荐系统领域[[多任务学习]]的事实标准。

## 关键内容

### 论文信息
- **标题**：Modeling Task Relationships in Multi-task Learning with [[MMoE|Multi-gate Mixture-of-Experts]]
- **作者**：[[Jiaqi Ma]], [[Zhe Zhao]], Xinyang Yi, Jilin Chen, Lichan Hong, [[Ed H. Chi]]
- **机构**：[[Google]] 推荐系统团队
- **发表**：KDD 2018(第 24 届 ACM SIGKDD 国际知识发现与数据挖掘大会)
- **页码**：pp. 1930-1939
- **DOI**：10.1145/3219819.3220007
- 至今被引用数千次，是[[多任务学习]]在推荐系统领域的奠基性工作之一

### 核心贡献
- 提出 MMoE 架构：为每个任务配备独立门控网络，自适应选择共享专家组合
- 建立研究[[多任务学习]]任务关系的实验范式：通过合成数据精确控制任务相关性
- 在 [[YouTube]] 大规模推荐系统中进行工业验证，离线和在线 A/B 测试均取得正向收益
- 证明当任务相关性降低时，独立门控的价值愈发凸显

### 实验验证
- **合成数据实验**：通过正交[[矩阵]]旋转变换精确控制任务相关性，验证 MMoE 在低相关性场景下的显著优势
- **UCI Census-Income 数据集**：在多任务分类任务中对比 L2-Constrained 和 Cross-Stitch 等方法
- **[[YouTube]] 推荐系统**：同时优化参与度预测和满意度预测，MMoE 在两任务上均优于 Shared-Bottom 基线
- **门控网络可视化**：发现满意度任务门控权重集中在少数专家，参与度任务分布更均匀

### 关键洞察
- "The prediction quality of commonly used multi-task models is often sensitive to the relationships between tasks."
- "The key insight is to use separate gating networks for each task."
- MMoE 以几乎零成本的门控网络换来显著效果提升，体现工程美学

### 影响与后续工作
- 催生 PLE(腾讯, 2020)、ESMM(阿里巴巴, 2018)、DBMTL(2020)、AC-MMoE(2023)、BEnet(2024) 等工作
- 2018-2020 年间成为工业级推荐系统[[多任务学习]]架构的事实标准
- MoE 思想在大模型时代迎来更大规模复兴

## 来源
- raw/books/推荐系统/14-mmoe.md — 深度解读文章

## 相关
- MMoE — 论文提出的核心架构
- [[Jiaqi Ma]] — 第一作者，当时为密歇根大学博士生，在 Google 实习期间完成此工作
- [[Ed H. Chi]] — 通讯作者，Google Research 杰出科学家
- PLE — 最重要的直接继承者
- ESMM — 利用用户行为序列关系建模任务因果依赖的后续工作
