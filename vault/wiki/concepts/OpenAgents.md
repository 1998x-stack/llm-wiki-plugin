---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 开放平台, 专门化Agent]
aliases: ["OpenAgents: An Open Platform for Language Agents in the Wild"]
relates_to: []
supersedes: null
---

# OpenAgents

## 概述
Open[[Agents]]是由Xie等人提出的开放平台，为真实环境中的语言代理提供[[服务]]。它构建了三个专门化代理，展示了专门化代理在特定领域远胜通用代理的观点。

## 关键内容

1. **三个专门化代理**：
   - DataAgent：[[Python]][[数据分析]]专家，集成pandas、matplotlib、sklearn、seaborn等工具
   - [[Plugins]]Agent：[[ChatGPT]]插件专家，集成200+Web[[服务]]如wolfram_alpha、web_search等
   - WebAgent：浏览器操作专家，提供click、type、scroll、navigate等DOM操作能力

2. **工程洞见**：
   - 专门化代理（Specialized Agent）在特定领域远胜通用代理（General Agent）
   - 深度垂直的专门[[Skills|技能]]配合代理路由优于试图构建"什么都能做"的超级[[Skills|技能]]

3. **系统架构特点**：
   - 每个代理都是特定[[Skills|技能]]的专家
   - 配合路由机制分发到合适的专门代理
   - 提供了专门化设计的实践案例

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "OpenAgents: An Open Platform for Language Agents in the Wild", 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Specialized-Agent]] — relates_to
- [[Agent-Platform]] — relates_to
- [[Skill-Specialization]] — relates_to