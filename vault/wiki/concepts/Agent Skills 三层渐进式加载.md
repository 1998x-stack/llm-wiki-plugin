---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, performance, efficiency, AI工程]
aliases: ["Progressive Disclosure in Agent Skills", "Three-Level Loading"]
relates_to:
  - target: "[[Agent Skills]]"
    type: implements
  - target: "[[渐进式加载]]"
    type: relates_to
supersedes: null
---

# Agent Skills 三层渐进式加载

## 概述
[[Agent Skills]]中最精妙的设计之一，解决"大量[[Skills|Skill]]导致[[Context Window]]爆炸"的核心矛盾，采用三层加载机制优化上下文效率。

## 关键内容

1. **三层加载机制**：
   - 第1层（启动时，始终加载）：
     - skill-a: name + description     ~100 tokens
     - skill-b: name + description     ~100 tokens
     - skill-n: name + description     ~100 tokens
   - 第2层（任务匹配后，[[渐进式披露（Progressive Disclosure）|按需加载]]）：
     - skill-b: 完整[[SKILL.md]]内容      <5,000 tokens
   - 第3层（执行过程中，明确需要时）：
     - skill-b/references/REFERENCE.md 仅在[[Claude_Code|Claude]]决定需要时加载

2. **上下文占用估算**：
   - 20个[[Skills]]常驻：20 × 100 = 2,000 tokens（仅~0.5%典型上下文）
   - 激活2个[[Skills]]：2 × 5,000 = 10,000 tokens
   - 总开销：~12,000 tokens，完全可控

3. **解决的问题**：
   - 避免大量[[Skills]]导致[[Context Window]]过载
   - 实现上下文效率的最优化
   - 在保持丰富功能的同时控制上下文成本

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文

## 相关
- [[Agent Skills]] — implements
- [[渐进式加载]] — relates_to