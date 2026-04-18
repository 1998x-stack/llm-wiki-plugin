---
type: concept
status: active
confidence: 0.9
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [superpowers, skill, planning, tdd]
aliases: ["writing-plans", "writing-plans Skill"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[TDD]]"
    type: implements
---

# writing-plans Skill

## 概述
[[Superpowers]] 技能，将已批准的规格文档分解为"初级工程师也能执行"的原子级任务清单，每个步骤 2-5 分钟、包含完整代码、精确文件路径、可复现验证命令。

## 关键内容

1. **执行者画像假设**：
   - 技术能力合格，但不了解工具链或问题域
   - 不擅长设计测试

2. **首要动作：文件映射**：
   - 先列出哪些文件将被创建/修改
   - 锁定分解决策
   - 偏好小文件原则

3. **强制 Header**：
   ```markdown
   # [Feature Name] Implementation Plan
   > **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development
   **Goal:** [一句话描述]
   **Architecture:** [2-3 句话]
   **Tech Stack:** [关键技术]
   ```

4. **任务粒度：2-5 分钟原则**：
   - Step 1: 写失败测试
   - Step 2: 运行确认失败
   - Step 3: 写最少实现代码
   - Step 4: 运行确认通过
   - Step 5: Commit

5. **禁止写法**：
   - ❌ "加一个验证函数" → ✅ 提供完整函数代码
   - ❌ "运行测试" → ✅ `pytest tests/specific.py::test_name -v`
   - ❌ "类似地……" → ✅ 每个结构都完整写出
   - ❌ "参考 X 实现" → ✅ 直接写出实现代码

6. **计划评审子循环**：
   - 写完计划 → 派遣 plan-document-reviewer 评审
   - 发现问题 → 同一 Agent 修复（保留上下文）
   - 最多 5 次迭代

7. **存储路径**：
   - `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`

## 来源
- [[03-writing-plans]] — writing-plans Skill 解析

## 相关
- [[Superpowers]] — part_of
- [[TDD]] — implements
- [[brainstorming Skill]] — precedes
- [[subagent-driven-development Skill]] — required_for
