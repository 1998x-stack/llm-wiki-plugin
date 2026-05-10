---
type: concept
status: active
confidence: 0.85
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [ai-engineering, token-management, context-window, resource]
aliases: [Token Management, Token 资源管理, Token Budget]
relates_to:
  - target: "[[上下文工程]]"
    type: part_of
  - target: "[[Anthropic]]"
    type: part_of
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[工具选择控制]]"
    type: uses
  - target: "[[工具结果缓存]]"
    type: uses
supersedes: null
---

# Token 资源管理

## 概述
Token 资源管理是 AI Agent 工程中的核心资源优化方法论，将 token 视为稀缺资源，通过注意力预算框架实现高效的上下文窗口利用。

## 关键内容

1. **注意力预算框架**：Anthropic 提出的上下文工程核心理念，将 token 使用视为预算分配问题，要求在每个环节考虑 token 成本与收益。

2. **性能预测指标**：研究发现 Token 使用量可解释 80% BrowseComp 方差，证明 token 管理效率是 Agent 性能的关键决定因素。

3. **上下文窗口管理**：
   - Claude Code 最佳实践的核心主题
   - 最小高信噪比 token 集合原则
   - 跨会话状态持久化与恢复

4. **成本优化策略**：
   - 压缩冗余上下文
   - 按需加载知识（渐进式披露）
   - 子 Agent 隔离上下文域

5. **与评测的关系**：Token 使用效率是评测驱动开发的重要指标，直接影响 Agent 架构设计和工具接口优化的方向。

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/00_INDEX.md]] — 跨文章核心主题：Token 即资源

## 相关
- [[上下文工程]] — part_of
- [[Anthropic]] — part_of
- [[Claude Code]] — uses
- [[BrowseComp]] — relates_to
- [[Agent 架构与设计原则]] — relates_to
- [[工具选择控制]] — uses (禁用工具节省 token)
- [[工具结果缓存]] — uses (减少重复调用消耗)
