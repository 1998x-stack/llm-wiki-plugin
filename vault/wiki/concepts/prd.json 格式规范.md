---
type: concept
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [agent-driven, prd, json-schema, ralph-loop]
aliases: ["prd.json Schema", "PRD JSON 格式", "Product Requirements Document JSON"]
relates_to:
  - target: "[[PRD 驱动开发]]"
    type: part_of
  - target: "[[Ralph Loop]]"
    type: uses
  - target: "[[JSONL格式]]"
    type: compares_to
supersedes: null
---

# prd.json 格式规范

## 概述
prd.json 是 [[PRD 驱动开发]]的核心数据文件，采用 JSON 格式定义项目的技术栈、User Story 列表、优先级、依赖关系和验收状态，作为 Agent 自主开发的权威任务源。

## 关键内容

1. **顶层结构**：
   ```json
   {
     "project": "项目名称",
     "version": "1.0.0",
     "created": "YYYY-MM-DD",
     "tech_stack": ["Next.js", "Prisma", "PostgreSQL"],
     "userStories": [...]
   }
   ```

2. **User Story 字段定义**：
   - `id`（必填）：唯一标识符，格式如 `auth-001`、`ui-002`，不可重复
   - `category`：故事分类，用于组织和筛选
   - `title`：Story 标题，简短描述
   - `description`（必填）：以用户视角描述功能，"用户可以..." 而非 "实现..."
   - `acceptanceCriteria`（必填）：验收标准数组，每个标准是可测试的具体条件
   - `passes`（必填）：布尔值，仅验证通过后可设为 true
   - `priority`（必填）：1-4 优先级，阻塞时可设为 99
   - `estimatedMinutes`：估算实现时间，建议 30-90 分钟
   - `dependencies`：依赖的 Story ID 数组，空数组表示无依赖

3. **优先级规则**：
   - Priority 1：核心功能，项目无法运行的
   - Priority 2：主要功能，用户主要使用的
   - Priority 3：增强功能，让体验更好的
   - Priority 4：边缘功能，可以最后做的
   - Priority 99：阻塞降级，自动排到最低

4. **Story 分类体系**：
   - Authentication（认证）、User Profile（用户资料）、Core Feature（核心功能）
   - API Integration（API集成）、UI/UX（界面交互）、Data Management（数据管理）
   - Performance（性能优化）、Admin（管理后台）
   - 专项场景：Landing Page、Billing、Email、Core Commands、Config Management、Core Endpoints、Data Validation、Rate Limiting、Testing 等

5. **验收标准特殊要求**：
   - 前端/UI 相关 Story 的 acceptanceCriteria 必须包含 "Verify in browser using dev-browser skill"
   - 每个 Story 可独立测试，不依赖未完成的 Story
   - 如有依赖，必须在 dependencies 字段中明确标注

6. **验证清单**：
   - 基本 JSON 格式合法性
   - 每个 Story 的必填字段（id, description, acceptanceCriteria, passes, priority）
   - 无重复 ID
   - UI Story 包含 browser 验证步骤
   - 优先级分布合理
   - 分类覆盖完整

## 来源
- [[raw/articles/ai-tools/ralph-loop/prd-generator-prompt.md]] — prd.json 完整格式定义、验证脚本和分类示例

## 相关
- [[PRD 驱动开发]] — part_of（prd.json 是 PRD 驱动开发的核心数据结构）
- [[Ralph Loop]] — uses（Ralph Loop 解析 prd.json 选择任务）
- [[User Story 粒度原则]] — relates_to（Story 定义必须遵循粒度约束）
- [[PRD 生成提示词]] — relates_to（prd.json 是 PRD 生成的输出产物）
