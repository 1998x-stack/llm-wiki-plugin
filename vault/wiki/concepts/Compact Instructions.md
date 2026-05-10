---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [compression, context-management, optimization]
aliases: ["Compact Instructions", "压缩指令", "上下文压缩指令"]
relates_to: []
supersedes: null
---

# Compact Instructions

## 概述
[[上下文压缩（Context Compaction）|Compact]] Instructions 是 [[CLAUDE.md]] 中定义的压缩策略，用于在[[上下文窗口]]达到 92% 阈值时触发 [[Compressor wU2]]，确保重要的内容在压缩过程中得以保留。

## 关键内容

1. **压缩策略定义**：
   - 在 [[CLAUDE.md]] 文件中通过 [[上下文压缩（Context Compaction）|Compact]] Instructions 定义保留规则
   - 指定哪些内容必须在压缩过程中保持不变
   - 常见保留项：API 端点签名、数据库模式变更、标记为 [CRITICAL] 的 TODO 注释

2. **压缩触发条件**：
   - 当[[上下文窗口]]达到 92% 阈值时自动触发 [[Compressor wU2]]
   - 确保在空间不足时优先保留最重要的信息

3. **压缩优先级**：
   - 高优先级：旧的工具调用输出（体积大，可重新获取）
   - 中优先级：早期对话历史（总结保留）
   - 保留：用户显式请求 + 关键代码片段
   - 保留：[[CLAUDE.md]] 规则（跨会话持久，不受压缩影响）

4. **手动控制命令**：
   - `/compact focus on the API changes` - 保留 API 相关内容
   - `/compact` - 默认压缩策略
   - `/context` - 查看当前 Token 占用

## 来源
- [[05_to_08_combined.md]] — 05 · CLAUDE.md & 上下文管理系统

## 相关
- [[CLAUDE.md]] — relates_to
- [[上下文管理系统]] — relates_to
- [[Context Management]] — relates_to
- [[Compression]] — relates_to