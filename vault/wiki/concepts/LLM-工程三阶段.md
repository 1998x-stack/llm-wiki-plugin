---
type: concept
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [LLM工程, "Prompt Engineering", "Context Engineering", "Harness Engineering", LLM能力]
aliases: ["LLM Engineering Three Phases", "Prompt-Context-Harness Engineering", "LLM工程发展三阶段"]
relates_to:
  - target: "[[Prompt-Engineering]]"
    type: compares_to
    confidence: 0.9
  - target: "[[Context-Engineering]]"
    type: compares_to
    confidence: 0.9
  - target: "[[Harness-Engineering]]"
    type: compares_to
    confidence: 0.9
  - target: "[[Language-Model]]"
    type: depends_on
    confidence: 0.8
supersedes: null
---

# LLM 工程三阶段：对比分析与未来预测

## 概述
LLM 工程的三个发展阶段：从 [[Prompt Engineering]]（[[Prompt Engineering|提示工程]]）到 [[Context Engineering]]（[[Context Engineering|上下文工程]]）再到 [[Harness-Engineering|Harness Engineering]]（环境工程），代表了从"手工艺"到"工程学"再到"环境科学"的进化路径。

## 关键内容

1. **[[Prompt Engineering]]（[[Prompt Engineering|提示工程]]）**：
   - 核心问题："怎么说，让 AI 听懂？"
   - 操作对象：自然语言指令文本
   - 关注层次：输入端（Token 级别）
   - 主要工具：文字编辑器、Playground
   - 技术机制：条件概率引导 P(y|prompt)，软约束（语言描述）
   - 可扩展性差，维护成本高

2. **[[Context Engineering]]（[[Context Engineering|上下文工程]]）**：
   - 核心问题："给 AI 什么信息，它才能做好？"
   - 操作对象：[[上下文窗口]]中的信息内容与结构
   - 关注层次：信息流（系统级别）
   - 主要工具：[[LangChain]]、LlamaIndex、向量数据库
   - 技术机制：信息检索 + 上下文组装，半软约束（结构化注入）
   - 有状态（记忆系统），中等可扩展性

3. **[[Harness-Engineering|Harness Engineering]]（环境工程）**：
   - 核心问题："设计什么环境，AI 才能持续做好？"
   - 操作道：代码库环境、约束系统、反馈循环
   - 关注层次：工程环境（组织级别）
   - 主要工具：[[Claude Code]]、CI/CD、Linter、GC Agent
   - 技术机制：机械约束 + 反馈循环，硬约束（CI [[门控机制（Gating Mechanism）|门控]]，不可绕过）
   - 持久状态，高可扩展性，低维护成本
   - 适用于10万行以上的大规模项目

## 来源
- [[AI-Agent--04_comparison_and_future]] — 原始文章

## 相关
- [[Prompt-Engineering]] — relates_to
- [[Context-Engineering]] — relates_to
- [[Harness-Engineering]] — relates_to
- [[Language-Model]] — relates_to