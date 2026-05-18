---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, project-management, verification, AI工程]
aliases: ["Nyquist Validation Layer", "Nyquist验证层", "验证合约", "需求-测试映射"]
relates_to:
  - target: "[[GSD Framework]]"
    type: part_of
  - target: "[[VALIDATION.md]]"
    type: implements
  - target: "[[Test Coverage]]"
    type: extends
supersedes: null
---

# Nyquist Validation Layer

## 概述
GSD框架中的验证层，将每个需求映射到可运行的自动化测试命令，形成"验证合约"，确保代码质量的可靠采样。

## 关键内容

1. **设计原理**：
   - 类比[[奈奎斯特]][[采样定理]]：为了可靠地"采样"到代码质量信号，需要在编码之前就设计好足够密度的[[测试覆盖率|测试覆盖]]
   - 在计划执行前，将每个需求映射到可运行的自动化测试命令

2. **实现方式**：
   - 创建需求-测试映射表，将需求ID与测试命令对应
   - 定义不同类型的[[测试覆盖率|测试覆盖]]（[[单元测试]]、E2E测试等）
   - [[Settings|设置]]Wave 0任务（必须在实现前完成的测试脚手架）

3. **验证机制**：
   - plan-checker的第8个验证维度检查VALIDATION.md是否存在
   - 确保覆盖本阶段所有v1需求
   - 不通过则计划无法被批准执行

## 来源
- [[raw/articles/ai-tools/claude-skills/02-context-file-system.md]] — 功能介绍和设计原理

## 相关
- [[GSD Framework]] — part_of
- [[VALIDATION.md]] — implements
- [[Test Coverage]] — extends