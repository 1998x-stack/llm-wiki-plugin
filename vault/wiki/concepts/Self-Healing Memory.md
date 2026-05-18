---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [memory-system, ai-agent, self-healing, AI工程]
aliases: [自愈记忆, Self-Healing Memory System]
relates_to: 
  - target: "[[三层记忆架构]]"
    type: characteristic
    confidence: 0.8
  - target: "[[MEMORY.md]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Topic Files]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Strict Write Discipline]]"
    type: relates_to
    confidence: 0.8
supersedes: null
---

# Self-Healing Memory

## 概述
Self-Healing Memory（自愈记忆）是 [[Claude Code]] 中的一种[[三层记忆架构]]，能够自主维护、更新和修正记忆内容，确保记忆系统的一致性和准确性。

## 关键内容

1. **核心机制**：
   - [[矛盾检测与解决]]：当 Agent 发现当前观察与记忆中的信息矛盾时，以当前观察为准更新对应的 topic file，并更新时间戳
   - 从观察到事实的升华：将暂时观察（Tentative Observation）逐渐升华为已验证事实（Verified Fact）
   - [[AutoDream]] 整合：当用户闲置时，后台守护进程对记忆进行整合，去除矛盾、提升事实确信度

2. **三层架构组成**：
   - 第一层：[[MEMORY.md]] — 轻量级指针索引
   - 第二层：[[Topic Files]] — [[Topic Files|按主题组织的知识库]]
   - 第三层：[[Transcripts]] — 只 Grep 不全读的[[Transcripts|历史记录]]

3. **自愈特性**：
   - 主动维护：Agent 主动维护和更新记忆系统
   - 防止污染：通过 [[Strict Write Discipline]] 防止错误信息污染记忆系统
   - 纠错能力：能够识别并纠正记忆中的错误信息

## 来源
- [[raw/articles/ai-tools/claude-code/03_memory_architecture.md]] — Claude Code 源码泄露深度解析（三）

## 相关
- [[三层记忆架构]] — characteristic
- [[MEMORY.md]] — relates_to
- [[Topic Files]] — relates_to
- [[Strict Write Discipline]] — relates_to
