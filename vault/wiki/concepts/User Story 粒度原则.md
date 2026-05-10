---
type: concept
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: ["agent-driven", "context-management", "user-story", "ralph-loop", "Agent系统"]
aliases: ["User Story Granularity", "Story 粒度", "故事粒度标准", "上下文窗口粒度约束"]
relates_to:
  - target: "[[上下文窗口]]"
    type: depends_on
  - target: "[[PRD 驱动开发]]"
    type: part_of
  - target: "[[Ralph Loop]]"
    type: implements
supersedes: null
---

# User Story 粒度原则

## 概述
User Story 粒度原则规定每个 User Story 必须足够小，能在单个[[上下文窗口]]内完成，否则 LLM 会在完成前耗尽上下文导致产出质量急剧下降。

## 关键内容

1. **核心约束**：每个 User Story 的实现工作量必须适配单个 LLM [[上下文窗口]]的容量。这是 [[Ralph Loop]] 和所有基于 Agent 的开发方法的基础约束，直接源于 [[LLM-Statelessness]] 和 [[上下文窗口]] 的物理限制。

2. **粒度判断标准**：
   - ✅ 合适粒度："用户可以通过邮箱注册账户"（30-60 分钟实现）
   - ✅ 合适粒度："用户可以上传头像图片"（30-60 分钟实现）
   - ❌ 过大粒度："实现完整的用户认证系统"（太大！）
   - ❌ 过大粒度："构建聊天功能"（太大！）

3. **时间估算参考**：合适的 Story 应对应 30-60 分钟的人类开发工作量。在 prd.json 中通过 `estimatedMinutes` 字段显式[[标注]]，建议值在 30-90 分钟之间。

4. **过大 Story 的危害**：
   - LLM 在完成前耗尽[[上下文窗口]]
   - 产出质量随上下文占用增加而显著下降
   - 无法在单次迭代中完成，导致状态不一致
   - 增加 [[上下文漂移]] 和 [[Context Rot]] 的风险

5. **Story 拆分策略**：
   - 按用户操作拆分：注册、登录、登出分别独立
   - 按数据模型拆分：CRUD 操作各自成 Story
   - 按 UI 组件拆分：每个页面或组件独立
   - 按 API 端点拆分：每个 endpoint 独立

6. **与 [[PRD 生成提示词]] 的关系**：在生成 prd.json 时，PM Agent 必须遵循此粒度原则，将大功能拆解为足够小的 User Story。数量指导：简单项目 20-50 个 Story，中型 50-100 个，复杂 100-200 个。

## 来源
- [[raw/articles/ai-tools/ralph-loop/prd-generator-prompt.md]] — "每个 User Story 必须足够小，能在单个上下文窗口内完成" 核心原则及粒度示例

## 相关
- [[上下文窗口]] — depends_on（粒度约束的根本原因）
- [[PRD 驱动开发]] — part_of（PRD 编写时必须遵循的约束）
- [[Ralph Loop]] — implements（Ralph Loop 依赖此原则保证单次迭代质量）
- [[上下文漂移]] — relates_to（过大 Story 增加漂移风险）
- [[Context Rot]] — relates_to（上下文腐烂与 Story 粒度直接相关）
