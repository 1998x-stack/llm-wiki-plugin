---
type: concept
status: active
confidence: 0.92
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-16
source_count: 2
tags: [技术, AI, 方法论, Agent系统]
aliases: ["Multi-Agent Architecture", "多智能体架构", "多Agent系统", "Orchestrator-Worker"]
relates_to:
  - target: "[[Agent工作流模式]]"
    type: extends
    confidence: 0.92
  - target: "[[生成器-评估器架构]]"
    type: related_to
    confidence: 0.85
  - target: "[[Agent Harness模式]]"
    type: related_to
    confidence: 0.85
  - target: "[[结构化笔记法]]"
    type: uses
    confidence: 0.8
  - target: "[[subagent-driven-development Skill]]"
    type: implements
    confidence: 0.9
  - target: "[[Context Window Pollution]]"
    type: addresses
    confidence: 0.9
  - target: "[[Two-Stage Review]]"
    type: supports
    confidence: 0.85
supersedes: null
---

# 多 Agent 架构

## 概述

多 [[Agent 架构与设计原则|Agent 架构]]是将复杂任务分配给并行运行的多个专门 Agent 实例的系统设计模式。核心价值：**[[子 Agent & 多 Agent 系统|子 Agent]] 通过各自独立[[上下文窗口]]进行并行探索，再将精简摘要返回给主 Agent**，从而实现超越单 Agent 上下文限制的任务规模。

## 关键内容

### 多 Agent 系统的适用条件

[[Anthropic]] 研究表明，多 [[Agent 架构与设计原则|Agent 架构]]在以下场景最有价值：
- **重度并行化**的任务（如广度优先研究：同时探索多个独立方向）
- **信息量超过单个[[上下文窗口]]**的任务
- **连接大量复杂工具**的任务
- 任务价值足以支付 **~15× 于聊天的 token 成本**

**不适合**：大多数编码任务（真正可并行的子任务较少）、Agent 间需要实时协调的场景。

### Token 消耗与性能的关系

[[Anthropic]] 在 [[BrowseComp]] 基准测试上的分析显示，**三个因素解释了 95% 的性能方差**：

| 因素 | 性能方差解释比例 |
|------|---------------|
| Token 使用量 | **80%** |
| 工具调用次数 | ~10% |
| [[模型选择]] | ~5% |

**关键结论**：多 [[Agent 架构与设计原则|Agent 架构]]的本质是**通过并行 Agent 分布 token 使用来扩展容量**。[[子 Agent 系统|多 Agent 系统]] vs 单 Agent [[Claude_Code|Claude]] Opus 4：内部研究 eval 上提升 **90.2%**。

### 编排者-工人模式（研究系统实现）

[[Anthropic]] Research 系统的具体架构：
```
用户查询
   ↓
LeadResearcher（编排者）
  - 分析查询，制定策略
  - 写研究计划保存到 Memory（防 Context 截断）
  - 同时派遣 3-5 个并行 Subagent
       ↓
Subagent 1, 2, 3... （并行探索）
  - 各自独立上下文，执行深度搜索
  - 使用 Interleaved Thinking 评估结果，精炼查询
  - 返回精简摘要（1000-2000 token）而非原始数据
       ↓
LeadResearcher 综合结果
  - 判断是否需要更多研究
  - 传递给 CitationAgent 处理引用
```

### 子 Agent 作为"压缩器"

[[子 Agent & 多 Agent 系统|子 Agent]] 的核心贡献不只是并行，而是**[[上下文压缩]]**：
- 每个[[子 Agent & 多 Agent 系统|子 Agent]] 可能消耗数万 token 探索信息
- 但只返回 1000-2000 token 的精简摘要给主 Agent
- 实现关注点分离：主 Agent 专注综合，[[子 Agent & 多 Agent 系统|子 Agent]] 专注深度探索

### 提示工程的特殊挑战

[[子 Agent 系统|多 Agent 系统]]的提示涉及协调，不只是行为控制：

1. **教导编排者如何委派**：明确目标、输出格式、工具使用指导、任务边界——否则[[子 Agent & 多 Agent 系统|子 Agent]] 重复工作或留下空白
2. **按查询复杂度缩放努力**：嵌入明确的规模规则（简单事实查询：1 个 Agent + 3-10 次工具调用；复杂研究：10+ [[子 Agent & 多 Agent 系统|子 Agent]]）
3. **从宽到窄的搜索策略**：先用短宽泛查询探索，再逐步聚焦
4. **引导思考过程**：让主 Agent 用 [[扩展思维|Extended Thinking]] 规划方法，[[子 Agent & 多 Agent 系统|子 Agent]] 用 [[交错式思考|Interleaved Thinking]] 评估每次工具结果

### 工程可靠性挑战

**[[错误复合|错误传播]]与状态**：Agent 运行时间长，错误可传播。建议：
- 结合 AI 的适应性（让 Agent 知道工具失败，自行适应）与确定性保障（重试逻辑、定期检查点）

**调试**：非确定性行为，同一提示不同运行产生不同结果。建议完整生产追踪。

**部署**：使用[[彩虹部署]]（[[Rainbow]] [[应用部署|Deploy]]ment）避免更新中断运行中的 Agent。

**当前局限**：大多数实现中主 Agent 同步等待[[子 Agent & 多 Agent 系统|子 Agent]] 完成，创建信息流瓶颈。异步执行是下一步。

### 并行工具调用

多 Agent 并行外，单个 Agent 内的[[并行工具调用]]也至关重要：
- [[子 Agent & 多 Agent 系统|子 Agent]] 并行调用 3+ 个工具，而非顺序调用
- 研究系统中此优化将复杂查询研究时间缩短 **90%**

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/How we built our multi-agent research system.md]]
- [[raw/articles/ai-engineering/anthropic-engineering/Building a C compiler with a team of parallel Claudes.md]]

## 相关

- [[Agent工作流模式]] — extends（多 Agent 是编排者-工人工作流的规模化实现）
- [[生成器-评估器架构]] — related_to（生成器-评估器是二元多 Agent 的特例）
- [[即时上下文检索]] — related_to（子 Agent 用 JIT 策略独立检索信息）
- [[结构化笔记法]] — uses（跨会话的信息传递机制）
- [[上下文腐烂]] — related_to（多 Agent 是绕过单 Agent 上下文限制的架构方案）
- [[subagent-driven-development Skill]] — implements（具体的多 Agent 执行技能）
- [[Context Window Pollution]] — addresses（多 Agent 架构解决上下文污染问题）
- [[Two-Stage Review]] — supports（支持多 Agent 系统的质量保证流程）
