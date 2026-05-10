---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [gsd, planning, xml, workflow]
aliases: ["XML Plan System", "GSD XML Plan", "XML Plan"]
relates_to:
  - target: "[[GSD]]"
    type: part_of
  - target: "[[GSD Commands]]"
    type: uses
  - target: "[[XML Plan]]"
    type: extends
---

# XML Plan System

## 概述
GSD 系统的结构化计划系统，使用 XML 标签定义任务，相比自然语言描述具有语义边界清晰、机器可处理、[[Claude_Code|Claude]] 训练数据友好等优势，包含 8 维 plan-checker 验证机制。

## 关键内容

1. **为什么 XML 比自然语言更适合**：
   - **语义边界清晰**：标签创造硬性边界，消除猜测空间
   - **训练数据友好**：[[Claude_Code|Claude]] 训练时见过大量 XML（API 文档、[[Configuration|配置]]文件）
   - **可机器处理**：plan-checker 可靠解析任务列表、依赖关系

2. **XML Schema**：
   ```xml
   <task type="auto|manual">
     <n>任务名称</n>
     <files>涉及的文件路径</files>
     <depends_on>依赖的其他任务</depends_on>
     <action>具体执行指令（精确、可执行）</action>
     <verify>验证命令（会被真正执行）</verify>
     <done>完成的语义定义</done>
   </task>
   ```

3. **标签职责**：
   - `<n>`：任务名称（也是 git commit message）
   - `<files>`：精确文件路径，消除猜测
   - `<action>`：必须实现的精确指令
   - `<verify>`：Claude 会真正运行的命令
   - `<done>`：完成的判断标准
   - `<depends_on>`：依赖关系，用于 DAG 分析

4. **Plan-Checker 8 维验证**：
   1. **需求覆盖完整性**（Requirement Coverage）：检查本阶段的所有 v1 需求是否都有对应的任务
   2. **技术一致性**（Technical Consistency）：计划中的技术选型是否与 PROJECT.md 的约束一致
   3. **计划原子性**（Plan Atomicity）：每个 PLAN 文件是否可在单个 200k 上下文窗口内完成，涉及文件数量不超过 20 个，任务数量不超过 5 个
   4. **依赖关系正确性**（Dependency Correctness）：验证 <depends_on> 无循环依赖，跨 PLAN 依赖合理
   5. **并行安全性**（Parallel Safety）：同波次中并行执行的计划是否会产生文件冲突
   6. **可验证性**（Verifiability）：每个任务的 <verify> 字段是否包含可执行的验证命令（如 curl、pnpm test 等），而非人类描述
   7. **上下文一致性**（Context Consistency）：计划的技术决策是否与 CONTEXT.md 中记录的用户偏好一致
   8. **Nyquist 验证覆盖**（Nyquist Validation）：VALIDATION.md 是否存在，其中每个 v1 需求是否都有对应的自动化测试命令

5. **文件命名**：
   - `{phase}-{plan}-[[XML Plan|PLAN.md]]`
   - 例：`02-01-[[XML Plan|PLAN.md]]`（第 2 阶段第 1 个计划）

6. **原子性原则**：
   - 每个 PLAN 文件包含 2-3 个任务
   - 可在干净 200k [[上下文窗口]]内完成
   - 超过 150 个文件操作应拆分

7. **计划粒度控制**（granularity）：
   - **粗粒度**（coarse）：3-5 个阶段，每阶段 1-2 个 PLAN，适合快速原型
   - **标准粒度**（standard）：5-8 个阶段，每阶段 2-3 个 PLAN，日常开发默认
   - **细粒度**（fine）：8-12 个阶段，每阶段 3-5 个 PLAN，生产级开发，高质量要求

8. **SUMMARY.md 存档**：
   每个 PLAN 执行完成后，[[gsd-executor]] 生成对应的 SUMMARY.md，记录：
   - 执行状态和时间轴
   - Git [[commit]]s 详情
   - 实际完成的工作清单
   - 关键决策记录
   - 偏差说明
   - 影响的文件列表

9. **最佳实践原则**：
   - **Action 字段写"不能做什么"和"为什么"**：包含禁止事项和理由，而非仅描述能做什么
   - **Verify 字段要真正运行**：包含可执行的命令（如 curl、pnpm test、pnpm tsc），而非人类描述
   - **Done 字段用清单格式**：明确列出完成标准，而非模糊叙述

## 来源
- [[05-xml-plan-system]] — XML 结构化计划系统

## 相关
- [[GSD]] — part_of
- [[GSD Commands]] — uses
- [[XML Plan]] — extends
- [[plan-checker]] — uses
