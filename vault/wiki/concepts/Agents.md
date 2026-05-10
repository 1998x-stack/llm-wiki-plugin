---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-tools, ai-agents, subagents]
aliases: ["Subagents", "Sub intelligent agents"]
relates_to:
  - target: "[[Claude Code]]"
    type: uses
  - target: "[[Agent Skills]]"
    type: collaborates_with
  - target: "[[Multi-Agent Workflows]]"
    type: enables
supersedes: null
---

# Agents

## 概述
[[Claude Code]]中定义的专用[[Subagents-in-Claude-Code|子智能体]]，拥有独立的system prompt，可被[[Skills]]调用，也能调用其他[[Skills]]，参与构建多智能体工作流。

## 关键内容

1. **基本特征**：
   - 拥有独立的system prompt
   - 可被[[Skills]]调用
   - 可以调用其他[[Skills]]
   - 是专用的[[Subagents-in-Claude-Code|子智能体]]

2. **在工作流中的作用**：
   - [[Skills]]与Agents可以相互调用
   - 构成"[[Skills|Skill]] → Agent → [[Skills|Skill]]"的嵌套调用模式
   - 形成完整的多智能体工作流

3. **典型应用示例**：
   ```
   /recipe-implement "Add user auth"          ← Recipe Skill 入口
            ↓
     requirement-analyzer Agent              ← 分析规模，确定工作流
            ↓
     frontend-executor Agent                 ← 使用 React/TypeScript 规则执行
            ↓
     design-sync Agent                       ← 验证前后端接口一致性
   ```

4. **与[[Skills]]的关系**：
   - 与[[Skills]]协作形成复合功能
   - 构成[[Claude Code]]生态中最强大的模式之一

## 来源
- [[raw/articles/ai-tools/claude-skills/01_claude_code_skill_system_overview.md]] — 全文

## 相关
- [[Claude Code]] — uses
- [[Agent Skills]] — collaborates_with
- [[Multi-Agent Workflows]] — enables