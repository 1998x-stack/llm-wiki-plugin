---
type: entity
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 5
tags: [ai-memory, rag, memory-palace, context-engineering, 开源, 本地运行, AI工程]
aliases: [MemPalace AI Memory, mempalace, MemPalace v3.0.0]
relates_to:
  - target: "[[记忆宫殿]]"
    type: implements
  - target: "[[MemPalace 宫殿架构]]"
    type: part_of
  - target: "[[分层记忆系统]]"
    type: compares_to
  - target: "[[渐进式加载]]"
    type: extends
  - target: "[[Mem0]]"
    type: compares_to
  - target: "[[Zep]]"
    type: compares_to
  - target: "[[ChromaDB]]"
    type: uses
  - target: "[[MCP]]"
    type: implements
supersedes: null
---

# MemPalace

## 概述
本地运行、完全开源的 AI 长期记忆系统，将古希腊[[记忆宫殿]]（[[记忆宫殿|Method of Loci]]）技术移植到 AI 记忆工程架构中。核心理念："存储一切，然后让它变得可以被找到"。

## 关键内容
- **项目背景**：2026 年 4 月由 [[Milla Jovovich]]（好莱坞女演员）和 [[Ben Sigman]]（工程师）使用 [[Claude Code]] 协作开发，48h 内 7000+ Star，当前 11200+ Star，MIT 许可证
- **核心哲学**：不要让 AI 决定记什么。与 Mem0/Zep 相反，不做 AI 摘要、不做信息提取、不让模型决定什么值得记忆
- **六层架构**：Wing（翼）→ Room（房间）→ Hall（大厅）→ Drawer（抽屉）→ [[隧道跨域连接|Tunnel]]（隧道）→ Closet（壁橱），每层都在剪枝噪声
- **检索提升**：从扁平向量搜索的 60.9% 到宫殿结构检索的 94.8%，提升 34 个百分点
- **[[LongMemEval]] 成绩**：[[候选生成|Recall]]@5 达到 96.6%（原文模式），对比 Mem0/Zep 的 ~85% 提升约 11pp
- **架构迭代史**：朴素向量搜索 60.9% → [[LLM 路由]] v1 灾难性失败 34.2% → 关键词路由 v2 75.6% → 宫殿+[[混合搜索]] v3 88.9% → Hybrid v5 96.6%
- **[[LoCoMo]] 成绩**：R@10 = 88.9%，超过 [[Memori]] 的 81.95%
- **核心发现**：[[原文逐字存储]] + 结构化检索的朴素方案，打败了让 AI 决定记什么的复杂方案。AAAK 和 Rooms 模式的分数低于原文模式，其价值在于降低 Token 消耗而非提升召回率
- **社区透明度**：发布数小时内社区发现 token 估算和 benchmark 模式问题，官方当天修正并公开承认，赢得社区好感
- **技术栈极简**：仅两个依赖 — [[ChromaDB]]（本地向量数据库）+ PyYAML。没有 [[LangChain]]、LlamaIndex、[[OpenAI]] SDK
- **设计原则**：内存层应该是确定性的、免费的、离线的。所有 Room 检测、内容分类、压缩用正则和关键词评分完成
- **MCP 集成**：提供 19 个 MCP 工具赋能 AI Agent
- **快速上手**：`pip install mempalace` → `mempalace init` → `mempalace mine` → `mempalace search`

### 与传统方案对比

| 维度 | 传统方案（Mem0 / Zep） | MemPalace |
|------|----------------------|-----------|
| 存储方式 | AI 提取关键信息 | [[原文逐字存储]] |
| 索引结构 | 平铺向量数据库 | 分层宫殿结构 |
| 运行环境 | 依赖云 API | 完全本地 |
| 信息损耗 | 提取时丢失推理链 | 零损耗 |
| LLM 调用 | 写入/读取时频繁调用 | 内存层零 LLM 调用 |

## 来源
- [[raw/articles/ai-tools/mempalace/mempalace_02_palace_architecture.md]] — MemPalace 深度解析第二篇：记忆宫殿架构
- [[raw/articles/ai-tools/mempalace/mempalace_01_overview.md]] — MemPalace 深度解析系列总览篇
- [[raw/articles/ai-tools/mempalace/mempalace_03_aaak.md]] — MemPalace 深度解析第三篇：AAAK 方言
- [[raw/articles/ai-tools/mempalace/mempalace_06_mcp_tools.md]] — MemPalace 深度解析第六篇：MCP 工具集成
- [[raw/articles/ai-tools/mempalace/mempalace_05_mining_pipelines.md]] — MemPalace 深度解析第五篇：三种挖掘管道
- [[raw/articles/ai-tools/mempalace/mempalace_07_benchmarks.md]] — MemPalace 深度解析第七篇：Benchmark 深度解析

## 相关
- [[记忆宫殿]] — implements
- [[MemPalace 宫殿架构]] — part_of
- [[分层记忆系统]] — compares_to
- [[渐进式加载]] — extends
- [[Mem0]] — compares_to
- [[Zep]] — compares_to
- [[ChromaDB]] — uses
- [[MCP]] — implements
- [[Milla Jovovich]] — created_by
- [[Ben Sigman]] — created_by
- [[AAAK 方言]] — uses
- [[Closet-Drawer 架构]] — implements
- [[Token 经济学]] — implements
- [[挖掘管道]] — implements
- [[MD5 去重]] — implements
- [[增量挖掘]] — implements
- [[Exchange 切块模式]] — implements
- [[对话平台适配器]] — implements
- [[正则提取模式]] — implements
- [[交互式配置]] — implements
- [[LoCoMo]] — used_by
- [[Memori]] — compares_to
- [[Recall@K]] — uses
- [[混合搜索]] — implements
- [[精确短语引号提取]] — implements
- [[人名权重增强]] — implements
- [[记忆/怀旧模式识别]] — implements
- [[距离缩减]] — implements
- [[LLM 路由]] — implements
- [[词汇不匹配问题]] — solves
