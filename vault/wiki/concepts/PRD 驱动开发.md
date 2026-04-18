---
type: concept
status: active
confidence: 0.85
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 3
tags: [development-methodology, prd, agent-driven]
aliases: ["PRD-Driven Development", "PRD 驱动", "prd.json 驱动"]
relates_to:
  - target: "[[Ralph Loop]]"
    type: implemented_by
  - target: "[[Agent 迭代循环]]"
    type: enables
  - target: "[[Session 交接机制]]"
    type: relates_to
  - target: "[[PRD 生成提示词]]"
    type: extends
  - target: "[[User Story 粒度原则]]"
    type: depends_on
  - target: "[[prd.json 格式规范]]"
    type: implements
supersedes: null
---

# PRD 驱动开发

## 概述
PRD 驱动开发是一种以产品需求文档（prd.json）为进度驱动核心的开发方法论，通过结构化的 User Story 列表、优先级排序、依赖关系和 `passes` 状态追踪，使 Agent 能够自主判断当前任务并逐步完成全部需求。

## 关键内容

1. **核心数据结构**：prd.json 包含 `userStories` 或 `features` 数组，每个 Story 具有 `id`、`description`、`priority`、`dependencies`、`passes`（布尔值）等字段。Agent 通过解析该文件自动筛选未完成且优先级最高的任务。

2. **任务选择逻辑**：
   ```python
   pending = sorted([s for s in stories if not s.get('passes', False)],
                    key=lambda x: x.get('priority', 99))
   → 选择 pending[0] 作为当前工作对象
   ```
   阻塞的 Story 会被设置 priority 为 99，自动降级到最低优先级。

3. **状态更新规则**：仅在验证通过（前端通过 [[Puppeteer MCP]] 截图验证，API 通过 curl 响应验证）后才能设置 `passes: true`。禁止主观判断或跳过验证直接修改状态。

4. **完成度追踪**：通过 `done/total` 比例实时反映进度。外循环检查是否 `done == total` 决定是否终止迭代。

5. **与 [[Agent 迭代循环]] 的关系**：每个迭代周期读取 prd.json → 选择最高优先级未完成 Story → 实现 → 验证 → 更新 passes → 提交 → 进入下一轮。prd.json 是迭代循环的"任务源"。

6. **与 [[Session 交接机制]] 的关系**：prd.json 是跨会话共享的权威进度源，新 Agent 实例启动时通过解析 prd.json 继承进度，无需依赖前一个 Agent 的上下文记忆。

7. **优先级体系**：Priority 1 为核心功能（项目无法运行），Priority 2 为主要功能（用户主要使用），Priority 3 为增强功能（提升体验），Priority 4 为边缘功能（最后做）。阻塞 Story 自动降级为 Priority 99。

8. **前置生成流程**：通过 [[PRD 生成提示词]] 在 [[Ralph Loop]] 启动前生成 prd.json，LLM 先提出 5-10 个澄清问题再生成文档，确保 Story 遵循 [[User Story 粒度原则]]（单个[[上下文窗口]]内可完成）。

9. **生成后验证**：prd.json 需通过 Python 脚本验证——检查基本格式、必填字段（id/description/acceptanceCriteria/passes/priority）、无重复 ID、UI Story 包含 browser 验证步骤。

## 来源
- [[raw/articles/ai-tools/ralph-loop/CLAUDE.md]] — Ralph Coding Agent 提示词模板中的 prd.json 驱动流程
- [[raw/articles/ai-tools/ralph-loop/AGENTS.md]] — AGENTS.md 中的 NEVER DO 规则（禁止未验证设置 passes、禁止修改 prd.json 验收标准）
- [[raw/articles/ai-tools/ralph-loop/coding-agent.md]] — Coding Agent 完整协议中的 prd.json 解析脚本和状态更新流程
- [[raw/articles/ai-tools/ralph-loop/prd-generator-prompt.md]] — PRD 生成提示词模板、验证脚本和专项场景 PRD 模板

## 相关
- [[Ralph Loop]] — implemented_by（PRD 驱动开发的具体实现系统）
- [[Agent 迭代循环]] — enables（为迭代循环提供任务源）
- [[Session 交接机制]] — relates_to（prd.json 作为跨会话权威进度源）
- [[Puppeteer MCP]] — relates_to（验证通过是更新 passes 的前提）
- [[PRD 生成提示词]] — extends（PRD 生成是 PRD 驱动的前置环节）
- [[User Story 粒度原则]] — depends_on（Story 必须遵循粒度约束）
- [[prd.json 格式规范]] — implements（定义了 prd.json 的完整 schema）
