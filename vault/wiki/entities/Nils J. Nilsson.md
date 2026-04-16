---
type: entity
title: "Nils J. Nilsson"
status: active
confidence: 1.0
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 1
tags: [AI, 研究, 机器人学]
aliases: ["Nils Nilsson", "N. J. Nilsson"]
relates_to:
  - target: "[[STRIPS 规划器]]"
    type: caused
    confidence: 1.0
  - target: "[[A*搜索算法]]"
    type: caused
    confidence: 1.0
  - target: "[[Shakey 机器人]]"
    type: depends_on
    confidence: 1.0
  - target: "[[Richard E. Fikes]]"
    type: caused
    confidence: 0.9
supersedes: null
---

# Nils J. Nilsson

## 概述
Nils J. Nilsson（[[威廉·卡汉|1933-]]2019）是人工智能领域的先驱人物，斯坦福大学计算机科学系奠基性教授之一，曾任 SRI International 人工智能中心负责人。他对 AI 的贡献具有双重奠基意义：一是与 Peter Hart 和 Bertram Raphael 共同发明了 [[A*搜索算法]]，定义了通用启发式搜索的标准；二是与 [[Richard E. Fikes]] 共同发明了 [[STRIPS 规划器]]，确立了自动规划的形式化框架。Nilsson 是 [[Shakey 机器人]]项目的主要负责人，他的工作将搜索理论与规划实践紧密结合，深刻影响了过去半个世纪的人工智能发展轨迹。

## 关键内容

### 双重奠基：搜索与规划
Nilsson 在 AI 基础理论上的贡献罕见地覆盖了两个核心支柱。
1.  **搜索算法**：1968 年，他参与提出的 A* 算法证明了在满足特定启发式条件下，可以找到从初始状态到目标状态的最优路径。这一算法成为了路径规划、游戏 AI 及各类优化问题的基石。
2.  **自动规划**：1971 年，他与 Fikes 合作开发的 [[STRIPS 规划器]]，创造性地将规划问题转化为状态空间搜索问题，并设计了高效的动作表示法。这使得复杂的逻辑推理能够应用于实时机器人控制。

这两项工作内在联系紧密：[[STRIPS 规划器|STRIPS]] 本质上是将 A* 风格的搜索策略应用到了由逻辑谓词定义的状态空间中。

### Shakey 机器人项目的领导角色
作为 [[Shakey 机器人|Shakey]] 项目的核心领导者，Nilsson 不仅负责技术指导，还亲自参与了关键算法的设计。他推动了感知、推理和行动在单一系统中的集成，证明了符号主义 AI 在物理世界中的可行性。在他的领导下，[[Shakey 机器人|Shakey]] 成为了第一个能理解自然语言指令、自主规划并执行任务的移动机器人，展示了 AI 从理论走向现实的巨大潜力。

### 教育与传承
Nilsson 在斯坦福大学任教期间，培养了大批优秀的计算机科学家。他撰写的教科书《Artificial Intelligence: A New Synthesis》以及他在经典教材《Artificial Intelligence: A Modern Approach》中的贡献，使得 [[STRIPS 规划器|STRIPS]] 和 A* 成为全球 AI 课程的核心教学内容。他的治学风格强调数学严谨性与工程实用性的统一，为后世研究者树立了榜样。Nilsson 于 2019 年去世，但他留下的算法和思想依然是现代智能系统的核心组件。

## 来源
- [[raw/books/机器人学/04-fikes-nilsson-strips-planner.md]]

## 相关
- [[STRIPS 规划器]]
- [[A*搜索算法]]
- [[Shakey 机器人]]
- [[Richard E. Fikes]]