---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [llm-strategy, ai-cost-optimization, inference-control]
aliases: ["LLM Inference Strategy", "LLM推理策略", "频率控制策略"]
relates_to: 
  - target: "[[TITAN-智能体]]"
    type: implements
    confidence: 0.8
  - target: "[[决策节点]]"
    type: relates_to
    confidence: 0.8
  - target: "[[API调用优化]]"
    type: implements
    confidence: 0.8
supersedes: null
---

# LLM推理策略

## 概述
LLM推理策略是一套用于优化大型[[Language-Model|语言模型]]调用频率和成本的技术方案，通过频率控制和智能复用来减少不必要的API调用。

## 关键内容

1. **频率控制机制**：
   - 每N步调用一次LLM，而非每步都调用
   - 在[[TITAN-智能体|TITAN]]系统中，默认每5步调用一次LLM进行决策
   - 300步测试仅需约60次LLM调用，而非300次

2. **决策复用策略**：
   - 中间步数复用上次LLM的决策结果
   - 只在指定间隔或特殊情况下调用LLM重新决策
   - 平衡了智能决策需求和成本效益

3. **高级推理组件**：
   - 决策提示词：包含系统指令、游戏知识和当前状态信息
   - 反思机制：当连续无进展时触发深度分析，识别潜在问题

## 来源
- [[TITAN-技术框架核心点报告]] — 第4节核心技术点三: LLM 推理策略

## 相关
- [[TITAN-智能体]] — implements
- [[决策节点]] — relates_to
- [[API调用优化]] — relates_to
- [[LangGraph状态机]] — relates_to