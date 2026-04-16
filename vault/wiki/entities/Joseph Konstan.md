---
type: entity
entity_type: person
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 协同过滤, 学者, ACM Fellow]
aliases: ["Joseph A. Konstan", "Joe Konstan"]
relates_to:
  - target: "[[GroupLens]]"
    type: part_of
  - target: "[[MovieLens]]"
    type: part_of
  - target: "[[Net Perceptions]]"
    type: part_of
  - target: "[[协同过滤]]"
    type: implements
  - target: "[[Item-Based Collaborative Filtering Recommendation Algorithms]]"
    type: part_of
  - target: "[[基于物品的协同过滤]]"
    type: caused
supersedes: null
---

# Joseph Konstan

## 概述
Joseph Konstan 是 [[GroupLens|GroupLens 研究组]]创始人之一，ACM Fellow，1997 年在《Communications of the ACM》上发表了 [[GroupLens]] 大规模部署的详细报告，与 [[John Riedl]] 联合撰写了 [[MovieLens|MovieLens 数据集]]历史与上下文论文（2015），并共同发表了推荐系统领域引用量最高的论文之一 [[基于物品的协同过滤|Item-Based CF]] 论文（2001）。

## 关键内容

1. **[[GroupLens]] 部署报告**：1997 年，Konstan 等人在《Communications of the ACM》上发表了更详细的 [[GroupLens]] 部署报告（Konstan, J. A., Miller, B. N., Maltz, D., Herlocker, J. L., Gordon, L. R., & Riedl, J. (1997). "[[GroupLens]]: Applying [[协同过滤|Collaborative Filtering]] to Usenet News." *Communications of the ACM*, 40(3), pp. 77-87），记录了为期七周的公开试验中 250 名用户提交 47,569 条评分、生成超过 600,000 条预测的关键实验发现。

2. **关键实验发现**：
   - 个性化预测显著优于非个性化平均分
   - 按新闻组分区提升评分密度，缓解数据稀疏问题
   - 系统实现了 95% 预测请求在 2 秒内完成、评分提交在 1 秒内完成的性能目标

3. **[[MovieLens|MovieLens 数据集]]文档**：2015 年与 F. Maxwell Harper 联合撰写了 "The [[MovieLens|MovieLens Dataset]]s: History and Context"（*ACM Transactions on Interactive Intelligent Systems*, 5(4), Article 19），这是推荐系统领域最广泛引用的数据集文档之一。

4. **[[基于物品的协同过滤|Item-Based CF]] 论文（2001）**：作为共同作者参与 [[Item-Based Collaborative Filtering Recommendation Algorithms]]（WWW '01），与 [[Badrul Sarwar]]、George Karypis、[[John Riedl]] 共同完成了推荐系统领域引用量最高的论文之一（[[Google]] Scholar 超 10,000 次引用），该论文首次系统性分析和评估了[[基于物品的协同过滤]]方法。

5. **学术地位**：Konstan 后来成为 ACM Fellow，是推荐系统领域最具影响力的学者之一，其工作覆盖了从 [[GroupLens]] 的早期部署到 [[MovieLens|MovieLens 数据集]]的长期维护，再到 [[基于物品的协同过滤|Item-Based CF]] 的开创性研究。

## 来源
- [[raw/books/推荐系统/02-grouplens-collaborative-filtering.md]] — 实验验证与历史地位章节
- [[raw/books/推荐系统/03-item-based-collaborative-filtering.md]] — 第 1 节（Item-Based CF 论文作者信息）

## 相关
- [[GroupLens]] — Konstan 是 GroupLens 研究组核心成员和部署报告第一作者
- [[MovieLens]] — Konstan 是 MovieLens 数据集文档的主要作者
- [[Net Perceptions]] — Konstan 参与创立的推荐引擎商业公司
- [[协同过滤]] — Konstan 是协同过滤大规模验证的关键贡献者
