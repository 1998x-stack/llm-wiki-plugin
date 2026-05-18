---
type: concept
status: active
confidence: 0.95
created: 2026-04-18
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 3
tags: ["superpowers", "multi-agent", "execution", "workflow", "Agent系统"]
aliases: ["subagent-driven-development", "Subagent-Driven Development Skill"]
relates_to:
  - target: "[[Superpowers]]"
    type: part_of
  - target: "[[Multi-Agent Orchestration]]"
    type: implements
  - target: "[[上下文窗口]]"
    type: addresses
  - target: "[[Context Window Pollution]]"
    type: addresses
    confidence: 1.0
  - target: "[[Two-Stage Review]]"
    type: implements
    confidence: 1.0
---

# subagent-driven-development Skill

## 概述
[[Superpowers]] [[Skills|技能]]，通过为每个任务派遣全新[[子 Agent & 多 Agent 系统|子 Agent]] 实现计划，配合[[Two-Stage Review|两阶段评审]]（规格合规性 → 代码质量），是 [[Superpowers]] 在有[[子 Agent & 多 Agent 系统|子 Agent]] 支持平台的首选执行引擎。

## 关键内容

1. **核心公式**：
   > Fresh subagent per task + two-stage review (spec then quality) = high quality, fast iteration

2. **[[Context Window Pollution|上下文窗口污染]]问题**：
   - 主 Agent 在 brainstorming + [[writing-plans Skill|writing-plans]] 后，积累了大量需求讨论、设计方案权衡、被否定方案、用户偏好说明
   - 这些历史会占用宝贵上下文空间，压缩实现任务能看到的代码量
   - 污染推理路径，使实现被"应该用方案B但被否定了"这样的历史干扰
   - 降低执行精度，[[Attention Dilution|注意力分散]]在协调和执行两种认知模式之间

3. **[[子 Agent & 多 Agent 系统|子 Agent]] 解决方案**：
   - **主 Agent（编排者）**：职责是读计划、维护状态、构建[[子 Agent & 多 Agent 系统|子 Agent]] 上下文、协调评审；上下文为完整的计划 + 项目背景
   - **[[子 Agent & 多 Agent 系统|子 Agent]]（执行者，每任务一个）**：职责是只做当前任务；上下文仅为当前任务所需的最小信息；生命周期为任务完成即销毁
   - [[子 Agent & 多 Agent 系统|子 Agent]] 的上下文由主 Agent **精确构造**，不继承主 Agent 的对话历史

4. **[[子 Agent & 多 Agent 系统|子 Agent]] 状态协议**：
   | 状态 | 含义 | 处理 |
   |------|------|------|
   | `DONE` | 任务完成，测试通过，自检通过 | 进入 Phase A 评审 |
   | `DONE_WITH_CONCERNS` | 完成但有值得注意的问题 | 读取关切评估严重性，必要时处理后再评审 |
   | `NEEDS_CONTEXT` | 缺少信息，无法决策 | 提供信息，重新派遣同级模型 |
   | `BLOCKED` | 遇到无法解决的阻碍 | 升级到更强模型 / 拆分任务 / 升级给人类 |

5. **[[Two-Stage Review|两阶段评审]]**：
   - **Phase A：规格合规性评审**（Spec Compliance Review）
     - 评审员角色：怀疑论者（Skeptic），不相信实现[[子 Agent & 多 Agent 系统|子 Agent]] 的自述
     - 确认做了正确的事：检查规格要求的每个功能点是否实现，是否有规格未要求的额外功能
     - 顺序：先确认"做了正确的事"，再审"做得对不对"
   - **Phase B：代码质量评审**（Code Quality Review）
     - 仅在 Phase A 通过后触发
     - 确认做得对不对：代码是否遵循[[项目约定手册|项目约定]]、[[错误处理]]是否完整、类型安全、[[可维护性]]、文件大小是否合理

6. **实现流程**：
   - 主 Agent 宣告使用 Subagent-Driven Development
   - 读取计划文件，提取所有任务的完整文本和上下文
   - 创建 [[TodoWrite-Tool|TodoWrite]] 任务列表
   - 对每个任务：派遣实现[[子 Agent & 多 Agent 系统|子 Agent]] → Phase A 评审 → Phase B 评审 → 标记任务完成

7. **[[模型选择]]策略**：
   - **机械性实现**：独立函数、清晰规格、1-2 个文件 → **Cheap（快速廉价模型）**
   - **集成任务**：多文件协调、模式匹配、调试 → **Standard（标准模型）**
   - **架构/设计/评审**：全局视角、判断调用 → **Capable（最强模型）**

8. **平台要求**：
   - ✅ [[Claude Code]]
   - ✅ [[Codex CLI|Codex]]（需 `multi_agent = true`）
   - ❌ [[Gemini CLI]]（无[[子 Agent & 多 Agent 系统|子 Agent]]，用 [[executing-plans Skill|executing-plans]]）

## 来源
- [[05-subagent-driven-development]] — subagent-driven-development Skill 解析
- [[上下文窗口]] — 上下文管理策略

## 相关
- [[Superpowers]] — part_of
- [[Multi-Agent Orchestration]] — implements
- [[writing-plans Skill]] — precedes
- [[上下文窗口]] — addresses_context_pollution
- [[Context Window Pollution]] — addresses
- [[Two-Stage Review]] — implements
- [[executing-plans Skill]] — alternative_approach
