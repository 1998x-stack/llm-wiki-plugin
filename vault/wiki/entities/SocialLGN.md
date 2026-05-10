---
type: entity
status: active
confidence: 0.7
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [推荐系统, 社交推荐, 图神经网络]
aliases: [SocialLGN]
relates_to: 
  - {target: "LightGCN", type: extends}
  - {target: "社交推荐", type: implements}
supersedes: null
---

# SocialLGN

## 概述
SocialLGN是基于LightGCN扩展到社交推荐场景的图神经网络推荐模型，将LightGCN的简化设计理念应用于包含社交关系的推荐系统中。

## 关键内容

1. **扩展设计**：
   - 基于LightGCN的简化框架扩展到社交推荐场景
   - 将用户-物品交互图扩展为包含用户-用户社交关系的复合图
   - 保持LightGCN的"少即是多"设计理念，在社交推荐中应用简化的图卷积

2. **应用场景**：
   - 针对具有社交网络信息的推荐场景
   - 利用用户间的社交关系增强推荐效果
   - 在原有用户-物品交互基础上加入用户-用户信任关系

3. **技术贡献**：
   - 证明了LightGCN简化设计在更复杂图结构中的有效性
   - 为社交推荐领域提供了一个轻量级的解决方案
   - 保持了LightGCN易训练、高效的特点

## 来源
- [[15-lightgcn.md]] — LightGCN论文深度解读中提及

## 相关
- [[LightGCN]] — SocialLGN的基础模型，被其扩展
- [[社交推荐]] — SocialLGN解决的核心任务
- [[图神经网络]] — 使用的技术框架