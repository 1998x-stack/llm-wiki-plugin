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
GSD 系统的结构化计划系统，使用 XML 标签定义任务，相比自然语言描述具有语义边界清晰、机器可处理、Claude 训练数据友好等优势，包含 8 维 plan-checker 验证机制。

## 关键内容

1. **为什么 XML 比自然语言更适合**：
   - **语义边界清晰**：标签创造硬性边界，消除猜测空间
   - **训练数据友好**：Claude 训练时见过大量 XML（API 文档、配置文件）
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
   1. 需求覆盖完整性
   2. 技术一致性（与 PROJECT.md 约定）
   3. 计划原子性（单上下文可完成）
   4. 依赖关系正确性
   5. 并行安全性（同波次无文件冲突）
   6. 可验证性（`<verify>` 可执行）
   7. 上下文一致性（与 CONTEXT.md 决策）
   8. Nyquist 验证覆盖（测试合约）

5. **文件命名**：
   - `{phase}-{plan}-[[XML Plan|PLAN.md]]`
   - 例：`02-01-[[XML Plan|PLAN.md]]`（第 2 阶段第 1 个计划）

6. **原子性原则**：
   - 每个 PLAN 文件包含 2-3 个任务
   - 可在干净 200k [[上下文窗口]]内完成
   - 超过 150 个文件操作应拆分

## 来源
- [[05-xml-plan-system]] — XML 结构化计划系统

## 相关
- [[GSD]] — part_of
- [[GSD Commands]] — uses
- [[XML Plan]] — extends
- [[plan-checker]] — uses
