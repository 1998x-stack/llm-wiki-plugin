---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: [superpowers, skill, planning, tdd]
aliases: ["writing-plans", "writing-plans Skill"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[TDD]]"
    type: implements
  - target: "[[executing-plans Skill]]"
    type: precedes
  - target: "[[plan-document-reviewer]]"
    type: uses
  - target: "[[File Mapping]]"
    type: requires
  - target: "[[03-writing-plans]]"
    type: source_for
---

# writing-plans Skill

## 概述
[[Superpowers]] [[Skills|技能]]，将已批准的规格文档分解为"初级工程师也能执行"的原子级任务清单，每个步骤 2-5 分钟、包含完整代码、精确文件路径、可复现验证命令。

## 关键内容

1. **执行者画像假设**：
   - 技术能力合格，但不了解工具链或问题域
   - 不擅长设计测试
   - 经验不足、品味糟糕、讨厌写测试的初级工程师也能执行

2. **首要动作：[[File Mapping|文件映射]]**：
   - 先列出哪些文件将被创建/修改及职责
   - 锁定分解决策
   - 设计具有清晰边界和良好定义接口的单元
   - 偏好小文件原则（更能推理清晰、编辑可靠、高内聚性）

3. **强制 Header**：
   ```markdown
   # [Feature Name] Implementation Plan

   > **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
   > (recommended) or superpowers:executing-plans to implement this plan task-by-task.

   **Goal:** [一句话描述构建什么]
   **Architecture:** [2-3 句话描述整体方法]
   **Tech Stack:** [关键技术/库]
   ```

4. **任务粒度：2-5 分钟原则**：
   - Step 1: 写失败测试（包含具体测试代码）
   - Step 2: 运行确认失败（具体命令+预期输出）
   - Step 3: 写最少实现代码（完整代码）
   - Step 4: 运行确认通过（具体命令+预期结果）
   - Step 5: Commit（具体git命令）

5. **禁止写法 vs 正确写法**：
   - ❌ "加一个验证函数" → ✅ 提供完整函数代码
   - ❌ "运行测试" → ✅ `pytest tests/specific.py::test_name -v`
   - ❌ "类似地……" → ✅ 每个结构都完整写出
   - ❌ "参考 X 实现" → ✅ 直接写出实现代码
   - ❌ "测试应该覆盖边界条件" → ✅ 写出具体的边界条件测试代码
   - 计划里不能有任何需要执行者自行判断的内容

6. **计划评审子循环**：
   - 写完计划 → 派遣 [[plan-document-reviewer]] 子 Agent 评审
   - 发现问题 → 同一 Agent 修复（保留上下文）
   - 最多 5 次迭代，超出 → 升级给人类
   - 大型计划按 Chunk 分段评审（每段 ≤1000 行）

7. **存储路径**：
   - `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
   - 每个子系统独立一份计划

8. **执行移交路径**：
   - 有子 Agent 平台（Claude Code、Codex）：使用 `[[subagent-driven-development Skill|subagent-driven-development]]`
   - 无子 Agent 平台（如 Gemini CLI）：使用 `[[executing-plans Skill|executing-plans]]`

9. **与 brainstorming 的衔接**：
   - 如果规格文档覆盖多个独立子系统，应拆分为独立计划
   - 每份计划应独立产出可工作、可测试的软件

10. **核心原则**：
   - **DRY**：计划文档本身也要 DRY，重复步骤用引用
   - **YAGNI**：严格按规格实现，不加"将来可能用到的"内容
   - **TDD**：每个 Task 都以写测试开始（Red → Green → Refactor）
   - **频繁 Commit**：每个 Task 完成后立即 Commit
   - **精确路径**：所有文件路径必须是精确的相对路径
   - **完整代码**：代码必须在计划文档里完整写出

## 来源
- [[03-writing-plans]] — writing-plans Skill detailed analysis
- [[Superpowers]]

## 相关
- [[Superpowers]] — part_of
- [[TDD]] — implements
- [[brainstorming Skill]] — precedes
- [[subagent-driven-development Skill]] — required_for
- [[executing-plans Skill]] — followed_by
- [[plan-document-reviewer]] — uses
- [[File Mapping]] — prerequisite
