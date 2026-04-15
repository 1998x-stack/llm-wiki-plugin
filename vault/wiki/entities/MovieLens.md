---
type: entity
entity_type: project
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 数据集, 协同过滤, 电影推荐]
aliases: ["MovieLens Dataset", "MovieLens 数据集"]
relates_to:
  - target: "[[GroupLens]]"
    type: part_of
  - target: "[[协同过滤]]"
    type: uses
  - target: "[[Item-Based Collaborative Filtering Recommendation Algorithms]]"
    type: uses
  - target: "[[基于物品的协同过滤]]"
    type: uses
  - target: "[[平均绝对误差 MAE]]"
    type: uses
  - target: "[[Net Perceptions]]"
    type: compares_to
supersedes: null
---

# MovieLens

## 概述
MovieLens 是从 [[GroupLens|GroupLens 研究组]]于 1997 年直接孵化出的在线电影推荐平台，同时产出了推荐系统领域最重要的公开数据集，从 MovieLens 100K 到 MovieLens 25M，每年被下载数十万次，是全球推荐算法研究的标准基准。

## 关键内容

1. **起源**：1997 年从 [[GroupLens]] 研究组直接孵化，是一个面向公众的在线电影推荐平台。其初衷不仅提供服务，更是为了收集大规模用户评分数据以推动推荐系统研究。

2. **数据集系列**：
   - **MovieLens 100K**：943 个用户、1,682 部电影、100,000 条评分（1-5 分整数评分），数据稀疏度约 93.7%（用户平均只评价了约 6.3% 的电影），从超过 43,000 个注册用户中随机抽样，只保留评价过至少 20 部电影的用户。最早被 [[Item-Based Collaborative Filtering Recommendation Algorithms]] 使用的基准数据集。
   - **MovieLens 1M**：100 万条评分，6,000 用户对 4,000 部电影的评分
   - **MovieLens 10M**：1,000 万条评分，包含标签数据
   - **MovieLens 25M**：2,500 万条评分，当前最广泛使用的版本
   - 评分[[矩阵]]填充率仅约 10%，典型地体现了推荐系统中的数据稀疏性问题

3. **学术影响**：过去三十年中绝大多数[[协同过滤]]算法论文都直接或间接使用了 MovieLens 数据集。它提供了一个标准化的比较平台，使得不同研究团队可以在相同数据上评估算法性能。

4. **与 [[Net Perceptions]] 的关系**：[[Net Perceptions]] 是 [[GroupLens]] 团队于 1996 年创立的商业公司，而 MovieLens 则保持了学术研究定位，两者共同推动了推荐系统从学术到产业的转化。

5. **数据特征**：
   - 显式评分（1-5 分制）
   - 包含用户人口统计学信息（年龄、性别、职业、邮编）
   - 包含电影元数据（标题、类型、上映年份）
   - 较新版本包含标签（tags）和时间戳数据

## 来源
- [[raw/books/推荐系统/02-grouplens-collaborative-filtering.md]] — GroupLens 历史影响章节
- [[raw/books/推荐系统/03-item-based-collaborative-filtering.md]] — 第 7.1 节（MovieLens 100K 数据集详情）
- [The MovieLens Datasets (Harper & Konstan 2015)](https://doi.org/10.1145/2827872)

## 相关
- [[GroupLens]] — MovieLens 的母研究组
- [[协同过滤]] — MovieLens 数据集主要服务于协同过滤算法研究
- [[Net Perceptions]] — 同源的商业化推荐系统公司
