---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [ai-engineering, agent-systems, software-architecture]
aliases: ["Harness Engineering", "Harness 设计", "Harness工程"]
relates_to:
  - target: "[[Prompt-Engineering]]"
    type: extends
    confidence: 0.8
  - target: "[[Context-Engineering]]"
    type: extends
    confidence: 0.8
  - target: "[[渐进式信息披露]]"
    type: uses
    confidence: 0.7
  - target: "[[Repo-as-System-of-Record]]"
    type: uses
    confidence: 0.7
  - target: "[[控制论视角]]"
    type: relates_to
    confidence: 0.7
  - target: "[[OpenAI百万行代码实验]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Harness分层架构]]"
    type: relates_to
    confidence: 0.7
  - target: "[[Harness-Engineering与控制论]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# Harness Engineering

## 概述
Harness Engineering 是一种 AI 时代的软件工程方法论，专注于构建让 AI Agent 能够正确生成代码的系统环境，而非直接编写代码本身。它将重点从人工编码转向设计运行环境、构建反馈回路、将架构约束转化为可执行规则。

## 关键内容

1. **核心理念**：
   - 人负责掌舵（steer），Agent 负责执行（execute）
   - 重点在于设计运行环境，而非直接编写代码
   - 将架构规范、约束和质量标准编码成可执行规则
   - 从写代码转向设计让代码被正确写出来的系统

2. **三个发展阶段**：
   - **[[Prompt Engineering]]**：如何把一句话说清楚（类比：写一封信）
   - **[[Context Engineering]]**：如何把必要信息喂进去（类比：准备一份档案）
   - **Harness Engineering**：如何把整个环境搭成一个可持续运行的系统（类比：建一座工厂）

3. **关键技术组件**：
   - **[[渐进式信息披露]]**：避免一次性将所有文档塞给 Agent，而是[[渐进式披露（Progressive Disclosure）|按需加载]]
   - **[[独立执行环境]]**：每个 Agent 在独立的 git worktree 里工作，互不干扰
   - **[[Repo-as-System-of-Record|仓库即记录系统]]**：任务定义、架构约束、质量标准都写在[[仓库]]里
   - **机械化约束执行**：架构约束通过 CI 规则硬卡，而非 code review 口头传达
   - **嵌入式反馈回路**：测试、验证等反馈回路嵌入 Agent 执行循环内部

4. **重要案例**：
   - [[OpenAI]]的百万行代码实验：3名工程师5个月内使用[[Codex CLI|Codex]] Agent构建超100万行代码产品
   - 实验表明早期进展缓慢是因环境未搭好，而非AI能力不足
   - 成功关键是将规则写下来让机器能读懂，包括依赖方向、Linter规则、[[项目约定手册|AGENTS.md]]文档等

5. **反馈回路机制**：
   - 需要有足够的传感器来感知状态和执行器来修正行为
   - 架构层面的判断需要LLM作为新型传感器和执行器来实现
   - 通过测试、Linter和可观测性作为传感器，LLM作为执行器来闭合反馈回路

## 来源
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — 知乎文章
- [[Harness Engineering: Leveraging Codex in an Agent-First World]] — OpenAI官方文章
- [[OpenAI百万行代码实验]] — OpenAI实验详细分析

## 相关
- [[Prompt-Engineering]] — relates_to
- [[Context-Engineering]] — relates_to
- [[Agent-Native-Architecture]] — relates_to
- [[ReAct]] — relates_to
- [[OpenAI]] — relates_to
- [[Harness分层架构]] — relates_to
- [[Harness-Engineering与控制论]] — relates_to
- [[渐进式信息披露]] — relates_to
- [[Repo-as-System-of-Record]] — relates_to