---
type: entity
entity_type: paper
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: [推荐系统, 图神经网络, 工业级推荐, KDD 2018]
aliases: [PinSage, PinSAGE]
relates_to:
  - {target: 协同过滤, type: implements}
  - {target: NGCF, type: compares_to}
  - {target: Embedding, type: uses}
  - {target: 近似最近邻检索, type: uses}
  - {target: TensorFlow, type: uses}
supersedes: null
---

# PinSage

## 概述
[[Pi-Agent|Pi]]nterest 于 KDD 2018 发表的工业级图推荐系统，首次在数十亿节点规模上部署基于图卷积的推荐模型，证明了 GCN 在推荐领域的工业可行性。

## 关键内容

1. **核心贡献**：[[Pi-Agent|Pi]]nSage 是首个在工业规模（数十亿节点、数百亿边）上成功部署的图卷积推荐系统。使用[[随机游走]]和邻域采样策略，避免了全图传播的计算瓶颈。

2. **技术特点**：（a）利用节点的丰富特征（如 [[Pi-Agent|Pi]]n 的图片嵌入）；（b）使用[[重要性采样]]选择关键邻居；（c）生成式训练策略；（d）支持在线推理，为新节点快速生成嵌入。

3. **与 [[NGCF]] 的区别**：[[Pi-Agent|Pi]]nSage 面向工业级规模，使用邻域采样和[[随机游走]]；[[NGCF]] 面向学术实验，使用全图传播。[[Pi-Agent|Pi]]nSage 利用节点特征（图片嵌入），[[NGCF]] 仅使用 ID 嵌入。

4. **工业影响**：[[Pi-Agent|Pi]]nSage 的成功部署证明了图推荐在大规模生产环境中的可行性，为后续工业级图推荐系统（如 Alibaba 的 EGES、Tencent 的图推荐系统）奠定了基础。

5. **历史地位**：与 GC-MC（KDD 2018）、[[NGCF]]（SIGIR 2019）共同奠定了图推荐方向。[[Pi-Agent|Pi]]nSage 代表了"工业可行"路线，而 [[NGCF]]/[[LightGCN]] 代表了"学术精简"路线。

## 来源
- [[15-lightgcn.md]] — LightGCN 论文中提及的图推荐标志性工作

## 相关
- [[NGCF]] — 同期学术级图推荐工作
- [[协同过滤]] — PinSage 解决的核心任务
- [[Embedding]] — PinSage 的核心表示方式
- [[近似最近邻检索]] — PinSage 使用的检索技术
- [[TensorFlow]] — PinSage 使用的框架
