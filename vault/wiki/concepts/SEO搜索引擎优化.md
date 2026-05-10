---
type: concept
status: active
confidence: 0.88
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [AI工程]
aliases: ["SEO", "Search Engine Optimization", "搜索引擎优化"]
relates_to:
  - target: "[[GEO生成式引擎优化]]"
    type: compares_to
    confidence: 0.9
  - target: "[[搜索引擎架构]]"
    type: uses
    confidence: 0.8
  - target: "BM25"
    type: uses
    confidence: 0.7
supersedes: null
---

# SEO搜索引擎优化

## 概述

SEO（Search Engine Optimization，搜索引擎优化）是通过优化网站技术架构、内容质量、外部链接，使页面在 [[Google]]/Bing 等传统搜索引擎的自然搜索结果（SERP）获得更高排名的综合策略。市场规模 2024 年达 891 亿美元。

## 关键内容

1. **发展历程**：1990s 关键词堆砌 → 2000s PageRank 主导 → 2010s 熊猫/企鹅[[算法]]（内容/链接质量）→ 2015 RankBrain（机器学习引入排名）→ 2018 E-A-T 框架 → 2021 Core Web Vitals → 2023 E-E-A-T 升级 → 2024 AI Overviews 全量上线 → 2025 GEO 兴起。

2. **四大核心模块**：
   - **技术 SEO**：爬虫可访问性、Core Web Vitals（LCP<2.5s，INP<200ms，CLS<0.1）、移动优先、URL规范化、robots.txt/sitemap
   - **内容 SEO**：E-E-A-T（Experience/Expertise/Authoritativeness/Trustworthiness）、关键词研究与布局、内容深度与权威性
   - **站内 SEO**：标题/H标签/meta优化、内部链接结构、图片 alt、URL 结构
   - **站外 SEO**：反向链接（Backlink）质量与数量、品牌提及、数字 PR

3. **评估指标**：关键词排名（SERP 位置）、自然搜索流量、点击率（CTR）、转化率、Domain Authority（DA/DR）。

4. **SEO vs GEO**：SEO 目标传统 SERP 蓝链，约 10 个竞争位置，30+ 年历史，可量化；GEO 目标 AI 生成答案引用，约 2-7 个竞争位置，2023 年提出，归因困难。两者互补，业界推荐双轨并行。

## 来源

- `raw/articles/ai-engineering/search-retrieval/02_SEO深度解析.md` — 2025 年最新实践
- `raw/articles/ai-engineering/search-retrieval/03_GEO_vs_SEO对比分析.md` — GEO vs SEO 全维度对比

## 相关

- [[GEO生成式引擎优化]] — compares_to
- [[搜索引擎架构]] — uses
- BM25 — uses（搜索引擎排序底层）
