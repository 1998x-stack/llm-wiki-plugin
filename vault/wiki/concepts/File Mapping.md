---
type: concept
status: active
confidence: 0.85
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [superpowers, planning, architecture, design]
aliases: ["File Mapping", "文件映射"]
relates_to:
  - target: "[[writing-plans Skill]]"
    type: prerequisite
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[Design Document]]"
    type: follows_from
---

# File Mapping

## 概述
在 [[writing-plans Skill]] 中的第一步关键活动，即在定义任何任务之前，先列出哪些文件将被创建或修改，以及每个文件的职责。这是锁定分解决策的地方，确保设计具有清晰边界和良好定义接口的单元。

## 关键内容

1. **目的**：
   - 明确模块边界和文件职责
   - 防止边写代码边拆分的混乱
   - 在编码开始前就把架构想清楚

2. **实施时机**：
   - 在 [[writing-plans Skill]] 定义任何任务之前
   - 在 [[Design Document]] 已经批准之后
   - 作为计划制定的首要动作

3. **最佳实践**：
   - **小文件原则**：更易推理、更可靠的编辑、高内聚性
   - **单一职责**：每个文件应该有一个明确的职责
   - **相关文件共存**：一起修改的文件应该住在一起（Cohesion）

4. **输出结果**：
   - 创建文件列表：`exact/path/to/file.py`
   - 修改文件列表：`exact/path/to/existing.py:123-145`
   - 测试文件列表：`tests/exact/path/to/test.py`

5. **与架构的关系**：
   - 文件映射是架构设计的具体体现
   - 好的文件映射反映了清晰的模块划分
   - 有助于后续的并行开发和测试

## 来源
- [[03-writing-plans]] — 文件映射作为 writing-plans 的首要动作

## 相关
- [[writing-plans Skill]] — required_before
- [[Superpowers]] — part_of
- [[Design Document]] — basis_for
- [[Module Boundary]] — related_to