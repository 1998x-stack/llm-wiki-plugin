---
type: concept
title: 子 Agent 卸载
status: active
confidence: 0.8
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["context-management", "agent-pattern", "ralph-loop", "subagent", "Agent系统"]
aliases: ["Subagent Offloading", "子代理卸载", "Sub-agent Offloading"]
relates_to:
  - target: "[[上下文策略]]"
    type: part_of
    confidence: 0.9
  - target: "[[Orchestrator-Subagent-Pattern]]"
    type: implements
    confidence: 0.85
  - target: "[[Context-Engineering]]"
    type: implements
    confidence: 0.85
  - target: "[[Ralph Loop]]"
    type: implemented_by
    confidence: 0.8
supersedes: null
---

# 子 Agent 卸载（Subagent Offloading）

## 概述
子 [[子 Agent 模式（Sub-Agent Pattern）|Agent 卸载]]是[[上下文策略]]之一，将消耗大量 tokens 但只需要结论的操作（如运行测试套件、编译、截图分析）卸载给[[子 Agent & 多 Agent 系统|子 Agent]] 执行，主 Agent 仅接收精简的结论摘要，从而将主上下文的增长从数万 tokens 压缩到数十 tokens。

## 关键内容

1. **核心机制**：主 Agent 作为调度层保持精简，将 token 密集型操作 spawn 给[[子 Agent & 多 Agent 系统|子 Agent]] 执行。[[子 Agent & 多 Agent 系统|子 Agent]] 在执行层消耗大量 tokens 但不污染主上下文，最终返回简洁结论。例如：
   - 主 Agent："请用[[子 Agent & 多 Agent 系统|子 Agent]] 运行完整测试套件，告诉我哪些通过，哪些失败"
   - [[子 Agent & 多 Agent 系统|子 Agent]]：执行 `npm test` → 生成 50,000 字符测试输出 → 总结为 "3 pass, 1 fail: auth.test.js line 45"
   - 主上下文增加：~20 tokens（而非 50,000）

2. **适合卸载的操作及 token 节省**：
   | 操作 | 原始 tokens | 卸载后 tokens | 压缩比 |
   |------|------------|-------------|--------|
   | 运行完整测试套件 | ~50,000 | ~100 | 500:1 |
   | 编译大型项目 | ~20,000 | ~50 | 400:1 |
   | 截图分析 | ~8,000 | ~50 | 160:1 |
   | 文件树扫描 | ~10,000 | ~100 | 100:1 |
   | Git diff 大型变更 | ~30,000 | ~100 | 300:1 |

3. **与 [[Orchestrator-Subagent-Pattern]] 的关系**：子 [[子 Agent 模式（Sub-Agent Pattern）|Agent 卸载]]是 [[Orchestrator Agent|Orchestrator]]-Subagent 模式在[[Context Management|上下文管理]]场景的具体应用。调度层（[[Orchestrator Agent|Orchestrator]]）负责决策和协调，执行层（Subagent）负责消耗性操作，两者通过精简的结论摘要通信。

4. **设计原则**：适合卸载的操作满足"消耗大量 tokens 但只需要结论"的特征。如果操作需要主 Agent 持续参与中间过程，则不适合卸载。

## 来源
- [[raw/articles/ai-tools/ralph-loop/context-strategies.md]] — Context Strategies 文档中的策略二

## 相关
- [[上下文策略]] — part_of（子 Agent 卸载是六大上下文策略之一）
- [[Orchestrator-Subagent-Pattern]] — implements（调度-执行分离模式的具体应用）
- [[Context-Engineering]] — implements（通过架构设计减少主上下文 token 消耗）
- [[Ralph Loop]] — implemented_by（Ralph Loop 使用子 Agent 执行测试和验证）
