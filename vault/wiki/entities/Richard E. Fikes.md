---
type: entity
title: "Richard E. Fikes"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 研究, 计算理论]
aliases: ["Richard Fikes", "R. E. Fikes"]
relates_to:
  - target: "[[STRIPS 规划器]]"
    type: caused
    confidence: 1.0
  - target: "[[Nils J. Nilsson]]"
    type: caused
    confidence: 0.9
  - target: "[[Shakey 机器人]]"
    type: depends_on
    confidence: 0.9
supersedes: null
---

# Richard E. Fikes

## 概述
Richard E. Fikes 是一位杰出的计算机科学家，曾任斯坦福研究院（SRI International）人工智能中心的研究员，后任职于 [[Xerox PARC]] 及斯坦福大学。他最广为人知的成就是与 [[Nils J. Nilsson]] 共同发明了 [[STRIPS 规划器|STRIPS]]（[[STRIPS 规划器|STanford Research Institute Problem Solver]]）规划器。这一工作发表于 1971 年的经典论文《[[STRIPS 规划器|STRIPS]]: A New Approach to the Application of Theorem Proving to Problem Solving》，为自动规划领域奠定了形式化基础。Fikes 的研究生涯专注于知识表示、问题求解及人机交互，其早期工作在 [[Shakey 机器人]]项目中得到了实际验证，对人工智能的发展产生了深远影响。

## 关键内容

### 学术背景与早期生涯
在 1970 年代初期，Richard Fikes 作为 SRI International 的年轻研究员，参与了具有里程碑意义的 [[Shakey 机器人]]项目。当时，人工智能界正面临如何让机器自主决策的挑战，现有的定理证明方法在处理复杂状态空间时效率低下。Fikes 敏锐地意识到需要将规划从纯粹的逻辑推导中剥离出来，设计一种更高效的状态空间搜索机制。

### STRIPS 的发明
Fikes 与 [[Nils J. Nilsson]] 的合作催生了 [[STRIPS 规划器]]。在这项工作中，Fikes 主要负责构建系统的核心逻辑框架，特别是提出了用“前提条件 - 添加列表 - 删除列表”来描述动作效果的创新方法。这种方法不仅解决了“框架问题”的表示难题，还极大地提高了规划效率，使得 [[Shakey 机器人|Shakey]] 能够在真实环境中完成多步任务。这篇论文被认为是自动规划领域的“创世论文”，其提出的表示法至今仍是该领域的标准语言（如 [[PDDL]]）的基础。

### 后续贡献与影响
离开 SRI 后，Fikes 在 [[Xerox PARC]] 继续其研究生涯，参与了早期个人计算环境和知识共享系统的开发。他在知识表示和本体论方面的研究进一步拓展了 AI 的应用边界。Fikes 的工作体现了理论与工程实践的完美结合：他不仅提出了深刻的理论洞见，还致力于将这些理论部署在真实的机器人系统中。他与 Nilsson 共同获得的荣誉，确立了他在人工智能基础理论奠基者中的地位。

## 来源
- [[raw/books/机器人学/04-fikes-nilsson-strips-planner.md]]

## 相关
- [[STRIPS 规划器]]
- [[Nils J. Nilsson]]
- [[Shakey 机器人]]