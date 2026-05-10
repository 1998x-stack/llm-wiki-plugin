---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [LLM, 工具调用, 工具发现, 工具修正]
aliases: ["CREATOR: Disentangling Abstract and Concrete Reasonings of Large Language Models"]
relates_to: []
supersedes: null
---

# CREATOR

## 概述
CREATOR是由Qian等人提出的统一框架，用于LLM的工具发现与复用，特别强调抽象推理与具体推理的分离。其创新之处在于不仅关注工具的创建和执行，还包含反思和修正环节。

## 关键内容

1. **四阶段框架**：
   - Creation（创造）：判断现有工具是否足够，若不足则抽象生成新工具
   - Decision（决策）：决定使用哪个工具或工具组合
   - Execution（执行）：执行选定的工具或工具序列
   - Rectification（修正）：不只是修复代码错误，还会反思工具设计合理性

2. **核心创新**：
   - Rectification阶段的独特设计：不仅修复执行错误，还会反思工具设计是否合理
   - 抽象推理与具体推理的分离：在创造阶段先写工具规格，再实现

3. **与其它工具制造方法的区别**：
   - 相比LATM等专注于工具制造的方法，CREATOR更强调后期修正
   - 强调工具设计的合理性反思，而非仅关注功能实现

## 来源
- [[llm-skill-research-series.md]] — LLM Skill研究系列
- [[Paper]] — "CREATOR: Disentangling Abstract and Concrete Reasonings of Large Language Models", EMNLP 2023

## 相关
- [[LLM-Skill-技术全景]] — relates_to
- [[Tool-Making]] — relates_to
- [[Tool-Discovery]] — relates_to
- [[Tool-Revision]] — relates_to