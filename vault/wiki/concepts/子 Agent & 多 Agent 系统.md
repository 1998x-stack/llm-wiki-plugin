---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [architecture, delegation, parallelism, AI工程]
aliases: ["Sub Agent", "Multi Agent System", "Delegation Layer", "子 Agent", "多 Agent 系统"]
relates_to: []
supersedes: null
---

# 子 Agent & 多 Agent 系统

## 概述
[[Claude Code]] 中的委派层，提供受控并行而非无限递归的 [[Agent 架构与设计原则|Agent 架构]]，通过深度限制防止 Agent 扩散失控。

## 关键内容

1. **设计原则**：
   - 受控并行，而非无限递归
   - 子 Agent 提供上下文隔离和并行能力
   - 深度限制防止 Agent 扩散失控

2. **为什么需要子 Agent**：
   - 主 Agent [[上下文窗口]]有限（200k tokens）
   - 并行探索多个实现方案
   - 隔离执行重型探索（不污染主上下文）
   - 专业分工（不同模型处理不同类型工作）
   - 将工作委派给子 Agent，仅将结论返回主上下文

3. **深度限制架构**：
   - 主 Agent -> Sub-Agent A（独立上下文，仅返回结论）
   - 主 Agent -> Sub-Agent B（独立上下文，仅返回结论）
   - 主 Agent -> Sub-Agent C（独立上下文，仅返回摘要）
   - 严格禁止：Sub-Agent -> Sub-Sub-Agent（深度 > 1，阻断）

4. **[[Git Worktree]] 隔离**：
   - 子 Agent 在临时 [[Git Worktree]] 中执行
   - 防止污染主工作目录
   - 子 Agent 的实验性变更不影响主分支
   - 多个子 Agent 可同时安全操作不同文件
   - 子 Agent 完成后自动清理 Worktree

5. **[[模型选择]]策略**：
   - 探索型（搜索、收集信息）：[[Claude-Haiku-4-5|claude-haiku-4-5]]（廉价快速）
   - 实现型（大多数编码）：[[Claude-Sonnet-4-6|claude-sonnet-4-6]]（平衡）
   - 架构决策/深度推理：[[Claude-Opus-4-6|claude-opus-4-6]]（最强）

6. **并行 Agent Teams 模式**：
   - 多个专业化 Agent 同时工作（安全、性能、架构评估）
   - Validator 最终汇总，生成统一报告

7. **Builder-Validator 模式**：
   - Builder Agent 实现功能
   - Validator Agent 验证实现
   - 通过共享任务列表协调

## 来源
- [[05_to_08_combined.md]] — 08 · 子 Agent & 多 Agent 系统

## 相关
- [[Claude Code]] — relates_to
- [[AgentTool]] — relates_to
- [[Architecture]] — relates_to
- [[Parallelism]] — relates_to