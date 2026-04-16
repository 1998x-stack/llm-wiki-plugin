---
type: entity
entity_type: person
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [推荐系统, 协同过滤, CSCW, 学者]
aliases: ["Paul Resnick", "Paul Joseph Resnick", "Resnick"]
relates_to:
  - target: "[[GroupLens]]"
    type: part_of
  - target: "[[Tapestry 系统]]"
    type: extends
  - target: "[[协同过滤]]"
    type: implements
supersedes: null
---

# Paul Resnick

## 概述
Paul Resnick 是 MIT 协调科学中心的研究员，与明尼苏达大学的 [[John Riedl]] 团队联合完成了 [[GroupLens]] 论文（1994），是历史上第一个自动化[[协同过滤]]系统的主要设计者之一；与 [[Hal Varian]] 共同主编了 1997 年 CACM 推荐系统特刊，正式确立了"推荐系统"这一研究领域名称。

## 关键内容

1. **学术背景**：1994 年任职于 MIT Center for Coordination Science（MIT 协调科学中心），与明尼苏达大学 [[John Riedl]] 团队联合开展 [[GroupLens]] 研究。

2. **[[GroupLens]] 贡献**：作为 [[GroupLens]] 论文的第一作者，Resnick 与 Riedl 共同领导了这项开创性研究。论文提出了将[[协同过滤]]从手动推进到自动的核心问题，设计了基于 [[Pearson 相关系数]] 的用户相似度计算方法和加权预测公式。

3. **开放架构理念**：Resnick 强调 [[GroupLens]] 的开放式设计哲学——"整个架构是开放的：替代的新闻客户端和 [[Better Bit Bureau]] 软件可以独立开发，并能与我们已开发的组件互操作。"这一理念在 1994 年极为超前，预见了后来的 Web API 设计思潮和联邦学习方向。

4. **隐私保护前瞻**：Resnick 及其团队在 1994 年就将隐私保护作为系统设计的一等公民，论证了假名评分不影响 [[Pearson 相关系数]]计算，这种"隐私不是事后补丁，而是设计之初的一等约束"的思维方式至今仍有指导意义。

5. **社会影响预见**：Resnick 团队在论文中提出"全球村是否会碎裂成一个个部落？"的问题，直接预见了后来被广泛讨论的 [[信息茧房]] 现象，比 Eli Pariser 在 2011 年正式提出"[[信息茧房|过滤气泡]]"概念早了整整 17 年。

6. **研究领域确立**：与 [[Hal Varian]] 共同主编 1997 年 CACM 推荐系统特刊，正式确立"推荐系统"（Recommender Systems）作为研究领域的名称。论文 "Recommender Systems" (CACM, 1997) 是该领域最具影响力的综述之一。

7. **主要论文**：
   - Resnick, P., Iacovou, N., Suchak, M., Be[[ripgrep|rg]]strom, P., & Riedl, J. (1994). "[[GroupLens]]: An Open Architecture for [[协同过滤|Collaborative Filtering]] of Netnews." *Proceedings of CSCW '94*, pp. 175-186.
   - Resnick, P. & [[Hal Varian|Varian]], H.R. (1997). "Recommender Systems." *Communications of the ACM*, 40(3), 56-58.

## 来源
- [[raw/books/推荐系统/01-tapestry-collaborative-filtering.md]] — 全文解读
- [[raw/books/推荐系统/02-grouplens-collaborative-filtering.md]] — 论文基本信息与核心方法章节

## 相关
- [[GroupLens]] — Resnick 是 GroupLens 论文第一作者和核心设计者
- [[Tapestry 系统]] — GroupLens 受 Tapestry 启发，实现自动化协同过滤
- [[协同过滤]] — Resnick 是自动化协同过滤的开创者之一，推动其成为正式研究领域
- [[Pearson 相关系数]] — Resnick 首次将其引入协同过滤
- [[信息茧房]] — Resnick 团队早在 1994 年就预见了这一现象
