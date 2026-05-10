---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [evolver, gep, mutation, ai-evolution, risk-management]
aliases: ["Mutation System", "变异系统", "突变策略"]
relates_to: 
  - target: "[[Evolver]]"
    type: implements
  - target: "[[GEP]]"
    type: part_of
  - target: "[[自我进化型 AI Agent 协议]]"
    type: extends
  - target: "[[信号去重机制]]"
    type: relates_to
supersedes: null
---

# Mutation 系统与策略预设

## 概述
Mutation 是 GEP（Gene Expression Programming）中的核心变更对象，用于将信号列表转化为带风险级别的显式变更指令。设计遵循"让所有进化决策可审计、可回溯、可拒绝"的理念。

## 关键内容

1. **Mutation 对象结构**：
   - type: 固定为 "Mutation"
   - id: 以 "mut_" 开头的时间戳标识符
   - category: repair（修复）/ optimize（优化）/ innovate（创新）三种类别
   - trigger_signals: 触发变更的信号列表
   - target: 变更目标（如 gene:xxx，behavior:protocol）
   - expected_effect: 预期效果描述
   - risk_level: low/medium/high 三级风险评估

2. **类别决策机制**：
   - 有错误信号 → 优先 repair
   - 启用漂变或有机会信号 → innovate
   - 默认 → optimize
   - 策略预设也可影响类别决策

3. **安全约束机制**：
   - 禁止创新类别与高风险人格结合（严谨度低或风险容忍度过高）
   - 高风险变更需具备"安全人格"（高严谨度+低风险容忍度）

## 来源
- [[Evolver]]
- [[GEP]]
- [[错误签名提取]]

## 相关
- [[GEP]] — part_of
- [[Evolver]] — implements
- [[自我进化型 AI Agent 协议]] — extends
- [[信号去重机制]] — relates_to