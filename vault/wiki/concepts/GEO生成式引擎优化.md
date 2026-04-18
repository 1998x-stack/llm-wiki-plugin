---
type: concept
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 2
tags: [AI工程]
aliases: ["GEO", "Generative Engine Optimization", "生成式引擎优化", "AEO", "LLMO"]
relates_to:
  - target: "[[SEO搜索引擎优化]]"
    type: extends
    confidence: 0.9
  - target: "[[检索增强生成]]"
    type: uses
    confidence: 0.85
  - target: "[[检索重排序]]"
    type: uses
    confidence: 0.8
supersedes: null
---

# GEO生成式引擎优化

## 概述

GEO（Generative Engine Optimization，生成式引擎优化）是专为 AI 驱动的生成式搜索引擎设计的内容优化[[规范化理论|范式]]，目标是让内容被 ChatGPT、Perplexity、[[Google]] AI Overviews、Claude 等 LLM 在生成答案时**主动引用**。由普林斯顿/IIT Delhi 于 2023 年提出，KDD 2024 收录。

## 关键内容

1. **市场规模（2025）**：AI 搜索替代传统搜索比例 58%、AI 引荐流量同比增长 +527%（2025 H1）、每次 AI 答案平均只引用 2-7 个域名（vs 传统搜索 10 条蓝链），竞争高度集中。

2. **生成式引擎多阶段检索**：广域文档检索 → 重排模型（ChatGPT 用 ret-rr-skysight-v3）→ LLM 合成生成（从 2-7 个精选域名提取事实）→ 带引用的自然语言答案。

3. **内容被 AI 选中的四大维度**：
   - **语义密度**：每 150-200 字中可提取的事实/数据/定义数量
   - **权威信号**：作者资质、引用来源、机构背书
   - **结构化程度**：清晰标题层级、FAQ 格式、模块化段落
   - **E-E-A-T**：Experience · Expertise · Authoritativeness · Trustworthiness

4. **核心优化策略**：
   - 内容结构：直接答案优先（前 40-60 字）、FAQ 格式、语义分块（每段落可脱离上下文被提取）、每 150-200 字嵌入一条具体数据点
   - 权威构建：原创研究/白皮书、透明作者署名、被高权威网站引用
   - 技术实现：Schema Markup（结构化数据）、AI 爬虫友好（不屏蔽 GPTBot/ClaudeBot/PerplexityBot）

5. **平台差[[异化]]**：ChatGPT 偏好权威深度内容；Perplexity 偏好时效性强的社区讨论；[[Google]] AI Overviews 偏好已有高 SEO 排名的内容；Claude 偏好可溯源、有引用的结构化内容。

6. **衡量指标**：AIGVR（AI Visibility Rate）、Citation Rate（引用率）、CER（内容提取率）、C2CR（AI 引用→业务转化率）。

7. **核心挑战**：黑盒特性（选源逻辑不透明）、零点击风险（AI 直接给答案，用户不访问原网站）、归因困难。

8. **最佳实践**：SEO + GEO 双轨并行，而非单独押注。GEO 不是 SEO 的替代品，是 AI 搜索时代的必要延伸。

## 来源

- `raw/articles/ai-engineering/search-retrieval/01_GEO深度解析.md` — arXiv:2311.09735 / KDD 2024
- `raw/articles/ai-engineering/search-retrieval/03_GEO_vs_SEO对比分析.md` — 全维度对比报告

## 相关

- [[SEO搜索引擎优化]] — extends（AI 时代的延伸）
- [[检索增强生成]] — uses（生成式引擎底层 RAG 架构）
- [[检索重排序]] — uses（生成式引擎多阶段重排）
- [[搜索引擎架构]] — compares_to
