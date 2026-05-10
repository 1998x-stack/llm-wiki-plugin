---
type: concept
status: active
confidence: 0.7
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [ai-tools, prd, prompt-engineering, ralph-loop]
aliases: ["PRD Generator Prompt", "PRD 生成 Prompt", "prd.json 生成提示词"]
relates_to:
  - target: "[[PRD 驱动开发]]"
    type: extends
  - target: "[[Ralph Loop]]"
    type: part_of
  - target: "[[Agent 角色系统]]"
    type: uses
supersedes: null
---

# PRD 生成提示词

## 概述
PRD 生成提示词是 [[Ralph Loop]] 的前置[[Skills|技能]]，通过让 LLM 扮演产品经理角色，先进行 5-10 轮澄清问答，再生成符合 [[prd.json 格式规范]]的完整产品需求文档。

## 关键内容

1. **触发时机**：在启动 [[Ralph Loop]] 之前必须先生成结构化的 PRD。触发方式为加载 PRD [[Skills|技能]]后发送 `Load the prd skill and create a PRD for [feature description]`，然后回答澄清问题。

2. **交互流程**：
   - 第一步：LLM 作为产品经理和需求分析专家，向用户提出 5-10 个澄清问题
   - 第二步：根据用户回答，生成完整的 prd.json 文件
   - 这种"先问后写"模式确保需求理解准确，避免遗漏关键场景

3. **提示词核心结构**：
   - 角色设定：产品经理和需求分析专家
   - 项目描述占位符：`[在这里描述你的项目]`
   - 两步任务：提问 → 生成 prd.json
   - 格式要求：完整的 JSON schema 定义
   - 数量指导：简单项目 20-50 个 Story，中型 50-100 个，复杂 100-200 个

4. **Story 编写规则**：
   - 以用户视角撰写："用户可以..." 而非 "实现..."
   - 每个 Story 可独立测试，不依赖未完成的 Story（或在 dependencies 中标明）
   - 前端/UI 相关的 Story，acceptanceCriteria 必须包含 "Verify in browser using dev-browser skill"
   - 遵循 [[User Story 粒度原则]]，确保单个 Story 能在一个[[上下文窗口]]内完成

5. **专项场景模板**：
   - **SaaS 应用**：Landing Page、Authentication、Dashboard、Core Feature、[[Settings]]、Billing、Admin、Email 等分类
   - **CLI 工具**：Core Commands、Config Management、Output Formatting、[[错误处理|Error Handling]]、[[Plugins|Plugin System]]、Documentation
   - **API [[服务]]**：Core Endpoints、Authentication、Data Validation、Error Responses、Rate Limiting、Documentation、Testing

6. **生成后验证**：通过 [[Python]] 脚本验证 prd.json 的基本格式、必填字段、重复 ID、前端 Story 的 browser 验证覆盖，以及优先级和分类分布统计。

## 来源
- [[raw/articles/ai-tools/ralph-loop/prd-generator-prompt.md]] — PRD Generator 完整提示词模板、验证脚本和专项场景模板

## 相关
- [[PRD 驱动开发]] — extends（PRD 生成是 PRD 驱动开发的前置环节）
- [[Ralph Loop]] — part_of（PRD 生成是 Ralph Loop 流程的第一步）
- [[User Story 粒度原则]] — relates_to（PRD 生成必须遵循粒度约束）
- [[prd.json 格式规范]] — relates_to（生成的输出格式定义）
