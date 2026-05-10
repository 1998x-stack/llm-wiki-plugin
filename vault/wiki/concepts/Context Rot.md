---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["llm", "context-window", "ai-limitation", "gsd", "LLM能力"]
aliases: ["Context Rot", "上下文腐败"]
relates_to:
  - target: "[[GSD]]"
    type: caused
  - target: "[[Context Engineering]]"
    type: relates_to
---

# Context Rot

## 概述
LLM 在[[上下文窗口]]逐渐填满后，生成质量系统性降级的物理现象，表现为[[注意力预算|注意力稀释]]、风格漂移、幻觉决策等问题。

## 关键内容

1. **发生时机**：上下文填满 50~60% 时可观察到明显症状

2. **典型症状**：
   - **[[注意力预算|注意力稀释]]**：早期关键决策被边缘化（如"用 jose 不用 jsonwebtoken"）
   - **主动压缩**：生成更短更简单的代码，出现"为简洁起见省略"等信号
   - **风格漂移**：命名规范、[[错误处理]]方式开始不一致
   - **幻觉决策**：编造之前不存在的约定，假装记得某些设计决策

3. **上下文消耗估算**（中型项目）：
   - 初期设计讨论：~15,000 tokens
   - 需求文档 + 技术选型：~8,000 tokens
   - 阶段 1-3 完整代码：~90,000 tokens
   - 计划、总结、中间过程：~40,000 tokens
   - **合计**：~153,000 tokens（已用 76%）

4. **传统解决方案的局限**：
   - BMAD：引入 Jira/故事点，solo 开发者无法承受
   - Speckit：规格静态，缺乏自动化桥接
   - 手动 `/clear`：清空后完全失忆
   - 超长 system prompt：自身就消耗大量 token
   - [[CLAUDE.md]]：对多阶段复杂项目控制力不足

5. **GSD 的解决方案**：
   - 每个命令只加载真正需要的文件
   - [[Subagents-in-Claude-Code|子智能体]]拥有独立的干净 200k 上下文
   - 主会话上下文保持在 30-40%

## 来源
- [[01-overview-context-rot]] — Context Rot 与上下文工程

## 相关
- [[GSD]] — caused
- [[Context Engineering]] — relates_to
- [[Context Window]] — part_of
