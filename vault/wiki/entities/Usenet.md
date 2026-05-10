---
type: entity
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [互联网, 通信系统, 信息科学]
aliases: ["Usenet", "网络新闻组", "新闻组", "网络新闻传输协议"]
relates_to: 
  - target: "[[GroupLens]]"
    type: "part_of"
  - target: "[[信息过载]]"
    type: "caused"
  - target: "[[Tapestry 系统]]"
    type: "part_of"
  - target: "[[NNTP协议]]"
    type: "uses"
  - target: "[[Xerox PARC]]"
    type: "related_to"
supersedes: null
entity_type: project
---

# Usenet

## 概述
Usenet是诞生于1970年代末的分布式讨论系统，基于NNTP（[[NNTP协议|网络新闻传输协议]]）运行，是1990年代互联网上最活跃的信息交流平台之一，也是[[GroupLens]][[协同过滤]]系统的重要应用场景。

## 关键内容

1. **发展历程**：
   - 诞生于1970年代末，是一种基于[[NNTP协议]]的分布式讨论系统
   - 到1994年初，每天发布约40,000篇文章
   - 到1994年底，日发布量飙升至约100,000篇文章
   - 数据传输量以每年约181%的速率增长
   - 新闻组数量本身也以每年52%的速度扩张

2. **技术架构**：
   - 采用分布式架构，新闻[[服务]]器通过[[NNTP协议]]同步文章
   - 用户使用各种新闻客户端软件访问和发布内容
   - 系统天然支持内容的分布式存储和传播

3. **[[信息过载]]问题**：
   - 在1994年成为[[信息过载]]问题的典型代表
   - 用户面临信息海啸，难以从中筛选有价值内容
   - 传统的过滤方法（版主审核、杀死文件）无法应对爆炸式增长的信息量

4. **[[GroupLens]]应用环境**：
   - Usenet成为[[GroupLens]]系统的主要应用平台
   - [[GroupLens]]通过在Usenet架构基础上添加评分机制来解决[[信息过载]]
   - 巧妙复用了Usenet的新闻传输基础设施，通过创建专用的"评分传输新闻组"来同步用户评分

5. **文化影响**：
   - 在互联网早期扮演了重要的信息交流角色
   - 为后来的论坛、社交媒体等平台提供了早期模式
   - [[Tapestry 系统]]等早期信息过滤研究也针对Usenet环境

## 来源
- [[GroupLens: 从新闻组到推荐系统帝国的奠基之作]]
- [[使用协同过滤编织信息挂毯]]

## 相关
- [[GroupLens]] — 在Usenet上实现协同过滤的系统
- [[信息过载]] — Usenet是1994年信息过载问题的典型案例
- [[NNTP协议]] — Usenet的基础传输协议
- [[Tapestry 系统]] — 针对Usenet等信息源的早期过滤系统