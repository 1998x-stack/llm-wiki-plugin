---
type: concept
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [algorithm, graph-theory, computer-science, shortest-path, 计算理论]
aliases: ["Dijkstra Algorithm", "迪杰斯特拉算法", "单源最短路径算法"]
relates_to:
  - target: "[[Edsger W. Dijkstra]]"
    type: invented_by
    confidence: 0.95
  - target: "[[图论]]"
    type: belongs_to
    confidence: 0.9
  - target: "[[最短路径问题]]"
    type: solves
    confidence: 0.95
  - target: "[[加权图]]"
    type: applies_to
    confidence: 0.9
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Dijkstra算法

## 概述
[[Edsger Dijkstra|Dijkstra]][[算法]]是由荷兰[[计算]]机科学家[[Edsger W. Dijkstra]]于1956年发明的单源最短路径[[算法]]，用于[[计算]]加权图中从单一节点到其他所有节点的最短路径。该[[算法]]采用贪心策略，保证在所有边权重非负的情况下找到最短路径。

## 关键内容
1. **[[算法]]原理**：[[算法]]维护一个顶点集合，已确定最短路径的顶点放入集合，逐步扩展。每次选择距离源点最近的未处理顶点，更新其邻居的距离估计值。

2. **应用场景**：广泛应用于路由[[算法]]、社交网络分析、游戏AI寻路、地图导航等领域。是图论和[[计算]]机科学中的经典[[算法]]之一。

3. **时间复杂度**：使用优先队列（如斐波那契堆）时时间复杂度为O(V log V + E)，其中V为顶点数，E为边数。

4. **约束条件**：要求图中所有边的权重均为非负数。若存在负权重边，则需使用其他[[算法]]如Bellman-Ford[[算法]]。

## 来源
- [[算法导论]] — 经典教材
- [[原始论文分析]] — raw/books/计算机科学/06-dijkstra-goto-considered-harmful.md（提及发明背景）

## 相关
- [[Edsger W. Dijkstra]] — invented_by
- [[图论]] — belongs_to
- [[最短路径问题]] — solves
- [[加权图]] — applies_to