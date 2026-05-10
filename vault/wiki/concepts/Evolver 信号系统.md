---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [evolver, signals, ai-tools, system-analysis]
aliases: ["Evolver Signals System", "Evolver 信号系统"]
relates_to: []
supersedes: null
---

# Evolver 信号系统

## 概述
[[Evolver]] 信号系统是从[[会话日志]]、内存文件、用户上下文中提取可操作进化触发信号的核心组件，作为运行时观察与进化决策之间的桥梁。

## 关键内容

1. **信号本质**：
   - 信号是运行时观察与进化决策之间的桥梁
   - 流程：原始日志文本 → 结构化信号列表 → Gene 选择器输入
   - 输入包括：[[会话日志]](.jsonl)、[[MEMORY.md]]、USER.md、recentEvents

2. **信号三[[大类]]别**：
   - **Defensive（防御型）**：错误与缺失检测，优先级最高，会覆盖[[机会型信号]]
     - 基础错误检测（log_error）
     - [[错误签名提取]]（errsig）
     - 重复错误检测（recurring_error）
     - 资源缺失信号（memory_missing, user_missing等）
     - 工具使用统计（high_tool_usage）
   
   - **Opportunity（机会型）**：创新触发，在无错误时检测
     - 功能请求提取（user_feature_request），支持多语言
     - 改进建议提取（user_improvement_suggestion）
     - 性能瓶颈检测（perf_bottleneck）
     - 能力缺口识别（capability_gap）
   
   - **Meta（[[元信号]]）**：系统状态感知
     - 演化停滞检测（evolution_stagnation_detected）
     - 稳定成功平台期（stable_success_plateau）
     - 修复循环检测（repair_loop_detected）
     - 连续失败跟踪（consecutive_failure_streak_N）
     - 基因封禁（ban_gene）

3. **信号去重与防循环机制**：
   - 历史分析：分析最近8个事件，统计各信号类型频次
   - 抑制逻辑：出现>=3次的信号加入抑制集合
   - 断路逻辑：包括修复循环断路、空轮检测、稳态降级、失败连串基因封禁

## 来源
- [[Evolver 信号系统（Signals）深度分析]] — src/gep/signals.js 核心职责

## 相关
- [[Evolver]] — implements
- [[信号去重机制]] — relates_to
- [[错误签名提取]] — relates_to