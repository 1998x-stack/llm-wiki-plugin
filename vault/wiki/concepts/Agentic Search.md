---
type: concept
status: active
confidence: 0.92
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 3
tags: [AI工程, Agent系统]
aliases: ["智能体搜索", "Agentic Retrieval", "Deep Research"]
relates_to:
  - target: "[[检索增强生成]]"
    type: extends
    confidence: 0.95
  - target: "[[Agent工作流模式]]"
    type: uses
    confidence: 0.9
  - target: "[[ReAct 风格循环]]"
    type: implements
    confidence: 0.9
  - target: "[[向量空间模型]]"
    type: uses
    confidence: 0.8
  - target: "BM25"
    type: uses
    confidence: 0.8
supersedes: null
---

# Agentic Search

## 概述

Agentic Search（智能体搜索）将搜索/检索行为嵌入 AI Agent 决策循环中：LLM 主动决定**何时**搜索、**搜什么**（动态构造查询）、**搜多少次**（迭代直到满足需求）、**如何整合**多次结果。是RAG 的动态决策版超集。

## 关键内容

1. **与 RAG 的本质区别**：RAG 是"一次检索→生成"的静态管道（开卷考试类比）；Agentic Search 是"LLM 主动循环搜索"的动态决策循环（研究助理类比）。RAG 是 Agentic Search 的底层工具之一，传统 RAG 是 Agentic Search 的特例。

2. **Agentic Search 工作流**：用户任务 → LLM 规划（任务分解、子问题生成）→ 工具调用（向量搜索/BM25/文件读取/API/代码执行）→ 结果观察（评估是否满足需求）→ 迭代判断（需要更多信息则重新搜索）→ 生成最终答案。

3. **主流实现模式**：
   - **[[ReAct]] 模式**：Reasoning → Action → Observation → 循环
   - **RAISE 模式**：[[ReAct]] + 短期记忆 + 长期记忆
   - **CRAG（Corrective RAG）**：检索后自动评估质量，质量差则重新搜索
   - **Self-RAG**：模型本身输出"是否需要检索"的判断令牌
   - **Deep Research**：多轮搜索 + 规划 + 报告生成（Perplexity/[[Gemini CLI|Gemini]] Deep Research）

4. **代码领域的 Agentic Search**：RAG 在代码域的核心问题是 Chunking 破坏代码结构、静态索引快速过期、符号导航需要动态追踪依赖链。[[Boris Cherny]]（[[Claude Code]] 负责人）："早期版本用了 RAG + 向量数据库，但很快发现 Agentic Search 通常效果更好——更简单，没有安全、隐私、数据过期和可靠性问题。"最优解是"像资深工程师一样探索"（查看目录结构、追踪 import、读整个文件建立心智模型），工具集：Glob/Grep/Read/LSP/Bash。

5. **技术栈**：编排层 LangGraph/AutoGen/CrewAI/Agno；工具层 MCP 工具集；检索工具 向量库+grep+LSP+文件系统；记忆层 [[上下文窗口]]+外部存储；评估层 [[LLM-as-Judge]]。

6. **选型指南**：
   - 知识库 QA/文档问答（FAQ 类）→ 传统 RAG 即可（延迟低、可预测）
   - 多跳推理/跨文档综合/代码[[仓库]]探索/实时数据 → Agentic Search
   - 最佳实践：**以 Agentic Search 为[[骨骼系统|骨架]]，RAG 为其工具之一**的混合架构

## 来源

- `raw/articles/ai-engineering/search-retrieval/Agentic Search 与 RAG：定义、联系与对比.md`
- `raw/articles/ai-engineering/search-retrieval/代码领域的 Agentic Search 设计指南.md`
- `raw/articles/ai-engineering/search-retrieval/代码领域：RAG vs Agentic Search 选型决策框架.md`

## 相关

- [[检索增强生成]] — extends（Agentic Search 是 RAG 的动态决策超集）
- [[Agent工作流模式]] — uses
- [[ReAct 风格循环]] — implements
- BM25 — uses（作为其工具之一）
- [[近似最近邻检索]] — uses（向量检索工具）
