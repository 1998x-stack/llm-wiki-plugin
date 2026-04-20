---
type: concept
status: active
confidence: 0.9
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [AI工程, Agent架构, 推理机制]
aliases:
- Think tool
- think 工具
- "思考工具"
relates_to:
- target: '[[Extended Thinking]]'
  type: compares_to
  confidence: 0.95
- target: '[[Chain-of-Thought]]'
  type: extends
  confidence: 0.9
- target: '[[外化工作记忆]]'
  type: implements
  confidence: 0.85
- target: '[[τ-Bench]]'
  type: uses
  confidence: 0.9
- target: '[[SWE-bench]]'
  type: uses
  confidence: 0.85
- target: '[[上下文工程]]'
  type: part_of
  confidence: 0.8
supersedes: null
---

# Think 工具

## 概述
Think 工具是一种为 LLM Agent 设计的显式"思考空间"机制，允许模型在复杂工具调用链中暂停并分析中间结果，从而提升策略遵从性和决策质量。

## 关键内容

### 核心定义与实现

Think 工具的实现极其简单，仅需一个无副作用的工具定义：
- **名称**：`think`
- **功能**：将想法追加到日志中，不获取新信息、不修改系统状态
- **参数**：仅一个 `thought` 字符串
- **关键特征**：无副作用、透明性（思考内容出现在工具调用日志中可供调试）、最小化接口

### 与 Extended Thinking 的本质区别

| 特性 | Extended Thinking | Think 工具 |
|------|------------------|-----------|
| 触发时机 | 模型开始生成**之前** | 已开始生成**之中** |
| 适用场景 | 深度计划、数学、编程 | 长工具调用链中处理工具输出 |
| 信息基础 | 主要基于用户查询 | 基于**外部工具返回的新信息** |
| 推理深度 | 更全面 | 更聚焦于新发现信息 |
| 最优领域 | 非工具场景（编码/数学/物理） | 策略密集、顺序决策场景 |

直觉类比：Extended Thinking 像是专家**开始工作前**的深度规划；Think 工具像是专家在**看到化验结果后**的即时分析。

### τ-Bench 评估结果

在 τ-Bench 航空域测试中：
- 基准（无 think，无 ET）：pass@1 = 0.332
- Extended Thinking：pass@1 = 0.412
- Think 工具（无 prompt 优化）：pass@1 = 0.404
- **Think 工具 + 优化 prompt**：pass@1 = **0.584**（提升 54%）

核心发现：
1. Think + 优化 prompt 在航空域的改进远超 Extended Thinking
2. 单独 Extended Thinking 和单独 Think 工具性能相近
3. **Prompt 优化是关键杠杆**——策略越复杂，示例越重要

零售域策略相对简单，仅凭 Think 工具（无 prompt 优化）就超过了基准和 Extended Thinking（pass@1 = 0.812 vs 0.783）。

### SWE-Bench 表现

- 实验规模：n=30（有 think 工具） vs n=144（无 think 工具）
- 性能提升：平均提升 1.6%（Welch t 检验：p < 0.001，效应量 d=1.47）
- 效应量相当大但平均提升仅 1.6%，说明 think 工具在编码场景中**改善了稳定性**（减少极端失败），而非系统性提升所有任务

### 认知科学视角：外化工作记忆

Think 工具从认知科学角度可理解为**外化工作记忆（Externalized Working Memory）**。人类在面对复杂问题时也需要"写下来"帮助思考——清单、草稿纸、白板。LLM 在处理长工具调用链时同样面临"工作记忆"压力：
- 之前哪些工具已调用
- 收集到了哪些信息
- 还缺少哪些信息
- 当前状态是否符合策略要求

Think 工具提供了一个**持久化的中间状态缓存**，减轻了模型在下一次推理时需要从对话历史中重新推导中间状态的负担。

### 与 Chain-of-Thought 的关系

Think 工具与 Chain-of-Thought（CoT）提示有内在联系，但存在重要区别：
- CoT 通过 prompt 隐式引导，Think 工具是显式工具调用
- CoT 固定在响应开始，Think 工具**动态**在需要时才触发
- CoT 混在响应文本中，Think 工具是结构化工具调用易于追踪
- Think 工具本质上是**结构化的、按需触发的 CoT**

### 适用与不适用场景

**适用场景**：
1. 工具输出分析：需要仔细处理前一个工具调用的输出并可能需要回溯
2. 策略密集环境：需要遵循详细指南并验证合规性
3. 顺序决策：每个行动都依赖于前一个，错误代价高

**不适用场景**：
1. 非顺序工具调用：仅需单次或多个并行调用时
2. 简单指令遵循：约束少，默认行为已足够好时

### 实践建议

**System Prompt 引导模板**：
```
## 使用 think 工具的时机
在以下情况调用 think 工具：
- 收到工具结果后，验证信息完整性
- 做出不可逆操作前，核对所有策略规则
- 发现多条可能路径时，分析最优选择

示例推理结构：
1. 当前状态：已获得哪些信息
2. 缺失信息：还需要什么
3. 策略检查：当前计划是否合规
4. 下一步：最优行动是什么
```

**监控与迭代**：
- 观察模型实际在 think 中写了什么，识别推理模式
- 若 think 内容质量低，可在 prompt 中提供更具体的示例
- 定期清理工具调用历史，避免 context 膨胀

### 更新说明（2025 年 12 月）

Extended Thinking 能力已大幅提升，在大多数场景下 Anthropic 现推荐使用 Extended Thinking 替代专用的 think 工具。但本文的分析仍具有重要的理论和实践价值。

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/03_think_tool.md]] — The "think" tool: Enabling Claude to stop and think in complex tool use situations

## 相关

- [[Extended Thinking]] — compares_to（两种不同的推理机制，触发时机和适用场景不同）
- [[Chain-of-Thought]] — extends（Think 工具是结构化的、按需触发的 CoT）
- [[外化工作记忆]] — implements（Think 工具实现了认知科学中的外化工作记忆概念）
- [[τ-Bench]] — uses（τ-Bench 是评估 Think 工具效果的主要基准）
- [[SWE-bench]] — uses（Think 工具在 SWE-bench 编码场景中得到验证）
- [[上下文工程]] — part_of（Think 工具是上下文工程中管理中间推理状态的技术）
