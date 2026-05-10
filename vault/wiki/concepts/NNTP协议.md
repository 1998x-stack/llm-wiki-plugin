---
type: concept
status: active
confidence: 0.75
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 2
tags: [网络协议, 互联网, 通信协议]
aliases: ["NNTP协议", "网络新闻传输协议", "Network News Transfer Protocol", "NNTP"]
relates_to: 
  - target: "[[Usenet]]"
    type: "uses"
  - target: "[[GroupLens]]"
    type: "part_of"
  - target: "[[Tapestry 系统]]"
    type: "part_of"
  - target: "[[Better Bit Bureau]]"
    type: "uses"
supersedes: null
---

# NNTP协议

## 概述
NNTP（Network News Transfer Protocol，网络新闻传输协议）是用于传输[[Usenet]][[Usenet|新闻组]]文章的互联网应用层协议，RFC 977定义了该协议的标准规范，为分布式[[Usenet|新闻组]]系统提供了底层通信机制。

## 关键内容

1. **协议作用**：
   - 专门设计用于[[Usenet]][[Usenet|新闻组]]系统的文章传输
   - 支持分布式、异步的[[Usenet|新闻组]]消息传递
   - 允许新闻[[服务]]器之间同步文章内容

2. **在[[Usenet]]中的应用**：
   - 作为[[Usenet]]分布式架构的核心协议
   - 实现新闻[[服务]]器间的自动同步
   - 支持[[Usenet|新闻组]]文章的发布、检索和管理

3. **在[[GroupLens]]中的利用**：
   - [[GroupLens]]巧妙地复用了现有的NNTP基础设施
   - 通过创建专用的"评分传输[[Usenet|新闻组]]"来传输用户评分数据
   - 无需建设新的传输系统，降低了部署复杂度

4. **在[[Better Bit Bureau]]中的作用**：
   - [[Better Bit Bureau|评分服务器]]通过NNTP协议与其他[[服务]]器共享评分
   - 利用[[Usenet|新闻组]]机制实现评分数据的分布式传播

5. **技术特点**：
   - 基于文本的协议，易于理解和实现
   - 支持高效的批量传输
   - 具备一定的扩展性和灵活性

## 来源
- [[GroupLens: 从新闻组到推荐系统帝国的奠基之作]]
- [[使用协同过滤编织信息挂毯]]

## 相关
- [[Usenet]] — NNTP协议的主要应用场景
- [[GroupLens]] — 复用NNTP基础设施的系统
- [[Better Bit Bureau]] — 通过NNTP协议共享评分数据