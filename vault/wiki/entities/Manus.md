---
type: entity
entity_type: project
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 1
tags: [AI, 工具, Agent系统]
aliases:
- Manus
- Manus AI
relates_to:
- target: "[[Context-Engineering]]"
  type: implements
  confidence: 0.9
- target: "[[MCP协议层]]"
  type: uses
  confidence: 0.8
- target: "[[即时上下文检索]]"
  type: uses
  confidence: 0.85
supersedes: null
---

# Manus

## 概述

Manus 是一款面向通用任务的 AI Agent 产品，由创始团队从 NLP 领域创业经验出发，选择基于前沿模型的上下文学习能力构建而非训练端到端智能体模型。2025 年被 Meta 收购，将其 AI 能力带给全球企业用户。

## 关键内容

### 技术路线选择

Manus 团队在 NLP 领域有丰富经验，曾从头训练模型用于开放信息提取和语义搜索。GPT-3 和 Flan-T5 的出现使内部模型一夜之间变得无关紧要。这一教训使他们明确选择：**押注[[Context-Engineering|上下文工程]]而非模型训练**。

**核心优势**：
- 几小时而非几周内交付改进
- 产品与底层模型保持正交——如果模型进步是上涨的潮水，Manus 是那条船，而不是固定在海床上的柱子

### 上下文工程六大原则

Manus 通过四次框架重建（他们戏称为"随机研究生下降"）总结出六条核心原则：

1. **围绕 KV 缓存进行设计**：KV-cache 命中率是生产阶段 AI Agent 最重要的单一指标，直接影响延迟和成本
2. **遮蔽，而非移除**：使用[[上下文感知]]的状态机管理工具可用性，通过 logits 掩码而非动态增删工具
3. **使用文件系统作为上下文**：将文件系统视为终极上下文——大小不受限、天然持久化、Agent 可直接操作
4. **通过复述操控注意力**：通过不断重写待办事项列表将全局计划推入模型近期注意力范围
5. **保留错误的内容**：将失败的尝试保留在上下文中，让模型隐式更新其内部信念
6. **不要被少样本示例所困**：在行动和观察中引入结构化变化，打破模式避免 Agent 陷入重复节奏

### 典型任务特征

- 平均约 **50 次工具调用**完成一个任务
- 输入与输出 token 比例约 **100:1**（高度倾斜于预填充）
- 使用虚拟机沙盒作为执行环境

### 在 Anthropic 生态中的位置

Manus 是 Claude [[Context-Engineering|上下文工程]]实践的重要案例研究，其经验被 [[Anthropic]] 官方博客转载分享。

## 来源

- [[raw/articles/ai-engineering/claude-blog/AI代理的上下文工程：构建Manus的经验教训.md]] — Manus 上下文工程六大原则

## 相关

- [[Context-Engineering]] — implements（Manus 是上下文工程的典型实践者）
- [[MCP协议层]] — uses（工具扩展协议）
- [[即时上下文检索]] — uses（文件系统作为按需加载的上下文源）
