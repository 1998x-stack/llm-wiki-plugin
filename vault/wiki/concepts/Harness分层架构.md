---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-engineering, agent-systems, architecture, AI工程]
aliases: ["Harness Layer Architecture", "Harness分层架构", "Agent Harness Layers"]
relates_to:
  - target: "[[Harness-Engineering]]"
    type: part_of
    confidence: 0.9
  - target: "[[Agent-Native-Architecture]]"
    type: relates_to
    confidence: 0.7
  - target: "[[Coding-Agents]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Agent-Orchestrators]]"
    type: part_of
    confidence: 0.8
supersedes: null
---

# Harness分层架构

## 概述
Harness分层架构是一种7层分类框架，描述了Agent系统中Harness的组成部分，强调模型几乎无关紧要，Harness才是一切。

## 关键内容

1. **七层架构模型**：
   - **第1层 - Human Oversight（人类监督）**：最终决策权
   - **第2层 - Spec [[Tool System|Tools]]（规格工具）**：把需求变成Agent可执行的任务描述
   - **第3层 - Full Lifecycle Platforms（全生命周期平台）**：从spec到部署的端到端管理
   - **第4层 - Task Runners（任务执行器）**：大任务拆解为可并行的子任务
   - **第5层 - Agent [[Orchestrator Agent|Orchestrator]]s（Agent编排器）**：协调多个Agent协作
   - **第6层 - Harness Frameworks/Runtimes（Harness框架和运行时）**：通用执行环境
   - **第7层 - [[编码 Agent 协议|Coding Agent]]s（编码Agent）**：商品化层（[[Claude Code]]、[[Cursor]]、[[Codex CLI|Codex]]等）

2. **价值分布**：
   - 最底层的[[编码 Agent 协议|Coding Agent]]s是最容易被替代的商品化层
   - 壁垒在上面几层：如何定义spec、如何编排任务、如何做人类监督
   - 模型几乎无关紧要，Harness才是一切

3. **设计模式**：
   - **[[渐进式信息披露]]**：不一次性把所有文档塞给Agent，而是根据需要[[渐进式披露（Progressive Disclosure）|按需加载]]
   - **[[独立执行环境]]**：每个Agent在独立的git worktree里工作，互不干扰
   - **[[Repo-as-System-of-Record|Repo as System of Record]]**：任务定义、架构约束、质量标准全部写在[[仓库]]里
   - **机械化约束执行**：架构约束通过CI规则强制执行，而非口头约定
   - **嵌入式验证反馈**：测试、验证反馈回路嵌入Agent执行循环内部

4. **性能影响**：
   - [[SWE-agent]]论文显示：仅靠[[Agent计算机接口|Agent-Computer Interface]]设计改进，获得64%的性能提升
   - [[LangChain]]在[[Terminal-Bench|Terminal Bench]] 2.0上的成绩从52.8%升到66.5%，排名从Top 30跳到Top 5
   - 模型未改变，仅优化Harness架构带来的显著提升

## 来源
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — 关于Harness七层架构的详细描述

## 相关
- [[Harness-Engineering]] — relates_to
- [[Agent-Native-Architecture]] — relates_to
- [[Coding-Agents]] — relates_to
- [[Agent-Orchestrators]] — relates_to
- [[Spec-Tools]] — relates_to