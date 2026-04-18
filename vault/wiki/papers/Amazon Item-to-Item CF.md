---
type: paper
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [推荐系统, 协同过滤, 工业推荐, Amazon]
aliases: ["Amazon Item-to-Item CF", "ItemCF", "Amazon.com Recommendations: Item-to-Item Collaborative Filtering"]
relates_to:
  - target: "[[Greg Linden]]"
    type: authored_by
  - target: "[[Amazon]]"
    type: published_by
  - target: "[[GroupLens]]"
    type: extends
  - target: "[[Item-Based 协同过滤]]"
    type: implements
---

# Amazon Item-to-Item CF

## 概述
工业推荐系统的里程碑论文（IEEE Internet Computing 2003），提出从"用户相似度"转向"物品相似度"，通过离线预计算物品相似度表实现毫秒级在线推荐，支撑 Amazon 35% 的销售额。

## 关键内容

1. **核心洞察**：不要计算用户与用户之间的相似度，改为计算物品与物品之间的相似度

2. **离线预计算**：
   - 计算所有物品对的共购相似度
   - 只保存每个物品的 Top-K 相似物品
   - 定期更新（非实时）

3. **在线推荐**：
   - 查表获取用户历史物品的相似物品
   - 聚合排序（出现多次的相似物品权重更高）
   - 复杂度 O(K)，毫秒级响应

4. **优势对比**：
   | 维度 | User-CF | Item-CF |
   |------|---------|---------|
   | 计算时机 | 在线实时（慢） | 离线预计算（快） |
   | 稳定性 | 用户行为动态变化 | 物品相似度相对稳定 |
   | 可解释性 | 弱 | "买了X的人也买了Y"直观 |
   | 冷启动 | 新用户无解 | 新用户买一件就有推荐 |

5. **商业影响**：
   - 推荐系统贡献 Amazon 约 35% 销售额
   - 成为工业推荐系统设计的基本原则

## 来源
- [[02_Amazon_ItemCF_2003]] — Amazon Item-to-Item CF：工业推荐系统的真正落地

## 相关
- [[Greg Linden]] — authored_by
- [[Amazon]] — published_by
- [[GroupLens]] — extends
- [[Item-Based 协同过滤]] — implements
