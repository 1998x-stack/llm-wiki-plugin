---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 2
tags: ["agent-pattern", "iterative-development", "autonomous-coding", "Agent系统"]
aliases: ["Agent Iteration Loop", "迭代循环模式", "单次迭代单 Story"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: implemented_by
  - target: "[[PRD 驱动开发]]"
    type: depends_on
  - target: "[[Agent Harness模式]]"
    type: part_of
  - target: "[[浏览器自动化验证]]"
    type: requires
  - target: "[[完成信号机制（Completion Signal）]]"
    type: uses
  - target: "[[固定提示栈（Fixed Prompt Stack）]]"
    type: depends_on
  - target: "[[子 Agent 模式（Sub-Agent Pattern）]]"
    type: uses
supersedes: null
---

# Agent 迭代循环

## 概述
Agent 迭代循环是一种自主编码代理的工作模式，每个迭代周期严格实现一个 User Story：选定任务 → 实现功能 → 验证通过 → 更新进度 → [[Git Commit|Git 提交]] → 更新交接日记 → 输出[[完成信号机制（Completion Signal）|完成信号]]，由外循环决定是否继续下一轮迭代。

## 关键内容

1. **循环结构**：
   ```
   启动序列（7步确认）→ 选定 Story → 实现 → 验证 → 更新 prd.json → Git 提交 → 更新 progress.txt → 输出 <promise>COMPLETE</promise>
   ```
   每个步骤都是强制性的，不可跳过。

2. **单次单 Story 约束**：每次迭代只实现 ONE 个 User Story，禁止跨 Story 并行。这确保每个 Agent 实例的工作范围清晰、可追踪、可回退。

3. **验证前置**：在更新 prd.json 的 `passes` 状态之前，必须完成实际验证——前端使用 [[Puppeteer MCP]] 截图验证，API 使用 curl 验证。验证失败不可标记完成。

4. **Git 提交规范**：提交信息包含 Story ID、变更点列表、E2E 验证结果和 PRD 进度统计，格式为：
   ```
   feat([story-id]): [简短描述]
   - [变更点 1]
   - [变更点 2]
   - E2E: [验证方式] passed
   PRD: [story-id] ✅ | Remaining: [N]
   ```

5. **异常处理路径**：
   - **Bug 卡住**：尝试 2 次 → 回退 → 标记 BLOCKED → 降级优先级 → 切换下一个 Story
   - **上下文将满**：stash 未完成工作 → [[标注]] Early exit → 提交干净状态 → 输出 COMPLETE
   - **依赖未满足**：检查 dependencies 字段，前置 Story 未完成时跳过

6. **与 [[Agent Harness模式]] 的关系**：Agent 迭代循环是 Harness 模式在自主编码场景下的具体实现。Harness 提供启动序列、验证工具、状态文件等基础设施，循环逻辑定义 Agent 的工作节奏。

7. **外循环与内循环**：内循环（Agent 实例内部）完成单个 Story 的实现与验证；外循环（Ralph 系统）检查 prd.json 完成度，决定是否启动新的 Agent 实例。

## 来源
- [[raw/articles/ai-tools/ralph-loop/CLAUDE.md]] — Ralph Coding Agent 提示词模板中的实现流程
- [[raw/articles/ai-tools/ralph-loop/coding-agent.md]] — Coding Agent 完整协议中的实现流程、异常处理路径、完成信号规范

## 相关
- [[Ralph Loop]] — implemented_by（Agent 迭代循环的具体实现系统）
- [[PRD 驱动开发]] — depends_on（依赖 PRD 提供任务源和进度状态）
- [[Agent Harness模式]] — part_of（Harness 模式的一种具体变体）
- [[浏览器自动化验证]] — requires（前端 Story 验证的必需环节）
- [[Session 交接机制]] — relates_to（每次迭代结束时更新交接文件）
- [[完成信号机制（Completion Signal）]] — uses（每次迭代结束必须输出完成信号）
- [[固定提示栈（Fixed Prompt Stack）]] — depends_on（每次迭代从相同的规范起点开始）
- [[子 Agent 模式（Sub-Agent Pattern）]] — uses（重型操作委托给子 Agent 保护主上下文）
