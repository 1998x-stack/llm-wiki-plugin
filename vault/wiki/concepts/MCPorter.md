---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [mcp, orchestration, tool-composition, automation, claude-code]
aliases: ["MC Porter", "MCP Tool Orchestration", "MCP 工具编排", "MCP 工具组合运行时"]
relates_to:
  - target: "[[MCP]]"
    type: extends
    confidence: 0.8
  - target: "[[工具组合]]"
    type: implements
    confidence: 0.85
  - target: "[[自动化工作流]]"
    type: enables
    confidence: 0.8
  - target: "[[多 MCP 工作流]]"
    type: implements
    confidence: 0.75
---
# MCPorter

## 概述
MCPorter 是 MCP ([[Model Context Protocol]]) 生态中的高级工具编排运行时，能够将多个 MCP 工具串联成一个复合流程，实现复杂的自动化任务。

## 关键内容
1. **核心概念**：
   - 工具组合运行时：将多个独立的 MCP 工具按逻辑顺序编排
   - 流程自动化：定义多步骤工作流，实现端到端任务执行
   - 参数传递：在工具间传递数据和上下文信息

2. **工作方式**：
   - 定义工具执行序列
   - 处理工具间的输入输出依赖
   - 管理执行状态和[[错误处理]]

3. **典型应用场景**：
   - 日常报告生成（聚合多个数据源）
   - 跨系统同步（协调多个外部[[服务]]）
   - 自动化文档生成（组合内容生成和发布工具）

4. **与普通 MCP 工具对比**：
   - 普通 MCP：单个工具执行单一功能
   - MCPorter：多个工具协同完成复杂任务

5. **架构位置**：
   - 位于 MCP 生态之上
   - 利用现有 MCP 工具进行编排
   - 提供更高层次的抽象

## 来源
- [[raw/assets/claude-howto/05-mcp/README.md]] — Claude How To MCP 高级工具编排介绍

## 相关
- [[MCP]] — extends
- [[工具组合]] — implements
- [[自动化工作流]] — enables
- [[多 MCP 工作流]] — implements
- [[MCP 工具集成]] — related_to