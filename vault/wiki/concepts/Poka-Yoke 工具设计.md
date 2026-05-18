---
type: concept
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [Agent设计, 工具设计, 防错, ACI, AI设计]
aliases:
- Poka-Yoke 工具设计
- 防错工具设计
- Poka-Yoke Tool Design
relates_to:
- target: '[[ACI (Agent-Computer Interface)]]'
  type: implements
  confidence: 0.95
- target: '[[AI Agent 架构模式]]'
  type: part_of
  confidence: 0.8
- target: '[[SWE-bench]]'
  type: uses
  confidence: 0.85
supersedes: null
---

# Poka-Yoke 工具设计

## 概述
Poka-Yoke 工具设计是一种 Agent [[ACI (Agent-Computer Interface)|工具接口设计]]方法论，源自制造业防错理念，通过修改接口设计使错误在结构上无法发生，而非依赖模型"记住"正确用法。

## 关键内容

1. **核心理念**：Poka-Yoke（防错）思维应用于 Agent 工具设计——通过改变工具接口使错误在结构上无法发生。这比在 prompt 中反复提醒模型"要注意 XX"更有效。

2. **[[SWE-bench]] 实证案例**：[[Anthropic]] 工程师发现 Agent 在从[[仓库]]根目录移动后，使用相对路径时出错。解决方案不是加强 prompt 警告，而是**修改工具定义，要求始终使用绝对路径**。效果：模型随后"无懈可击"地使用此工具。

3. **与 ACI 的关系**：Poka-Yoke 工具设计是 [[ACI (Agent-Computer Interface)]] 设计原则的具体实践。[[Anthropic]] 在 [[SWE-bench]] 上花费在工具优化上的时间多于整体 prompt 优化，证实了[[ACI (Agent-Computer Interface)|工具接口设计]]应获得与 HCI 同等的工程重视。

4. **设计原则**：
   - 参数名称让意图显而易见（如同给初级开发者写优质文档）
   - 通过约束输入格式消除错误可能性
   - 工具定义包含示例用法、边缘情况、与其他工具的清晰边界
   - 建立工作台（workbench）运行大量示例输入，观察工具使用错误并迭代

## 来源

- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/07_swe_bench_sonnet.md]] — 工具设计深度优化案例

## 相关

- [[ACI (Agent-Computer Interface)]] — implements（Poka-Yoke 是 ACI 设计原则的具体实践）
- [[AI Agent 架构模式]] — part_of（Agent 工具设计方法论的一部分）
- [[SWE-bench]] — uses（SWE-bench 是 Poka-Yoke 工具设计的验证平台）
