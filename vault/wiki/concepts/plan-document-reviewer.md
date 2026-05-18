---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [superpowers, skill, planning, review, AI工程]
aliases: ["plan-document-reviewer", "Plan Document Reviewer"]
relates_to:
  - target: "[[writing-plans Skill]]"
    type: used_by
  - target: "[[Superpowers]]"
    type: part_of
---

# plan-document-reviewer

## 概述
计划文档评审[[子 Agent & 多 Agent 系统|子 Agent]]，由 [[writing-plans Skill]] 触发，用于自动评审计划文档的质量和完整性。这是计划评审子循环中的关键组件。

## 关键内容

1. **触发时机**：
   - 在 [[writing-plans Skill]] 完成计划文档编写后立即触发
   - 是计划正式交付给执行阶段前的质量保证环节

2. **评审机制**：
   - 对完整的计划文档进行全面检查
   - 如发现问题，由原编写 Agent 进行修复（保持上下文）
   - 评审过程最多迭代 5 次，超过则升级给人类

3. **评审范围**：
   - 计划的原子任务粒度是否符合 2-5 分钟原则
   - 每个任务的步骤是否足够详细和明确
   - 文件路径和命令是否精确
   - 测试代码是否完整

4. **大型计划处理**：
   - 对于超过 1000 行的大型计划，按 Chunk 分段进行评审
   - 每段以 `## Chunk N:` 为分隔符
   - 防止单次评审窗口溢出

5. **质量标准**：
   - 确保计划文档达到"初级工程师也能执行"的标准
   - 验证任务间的依赖关系是否清晰
   - 检查验证命令和预期输出是否明确

## 来源
- [[03-writing-plans]] — plan-document-reviewer 在计划评审循环中的作用

## 相关
- [[writing-plans Skill]] — triggers
- [[Superpowers]] — part_of
- [[File Mapping]] — reviews