---
type: concept
status: active
confidence: 0.75
created: 2026-04-18
updated: 2026-04-18
last_accessed: 2026-04-18
source_count: 1
tags: [AI, Agent系统, 设计模式]
aliases: [Agent Role System, 智能体角色系统, Agent 角色配置]
relates_to:
  - target: "[[Codex多Agent调度]]"
    type: implements
    confidence: 0.9
  - target: "[[Orchestrator-Subagent-Pattern]]"
    type: part_of
    confidence: 0.8
  - target: "[[Multi-Agent Orchestration]]"
    type: part_of
    confidence: 0.75
supersedes: null
---

# Agent角色系统

为多 Agent 系统中的每个子 Agent 定义专业化角色，通过注入不同的 guidance（行为指引）和约束，使 Agent 从"通用型"转变为"专业型"，用结构化分工取代"一个 Agent 包揽一切"的脆弱模式。

## 概述
Agent 角色系统通过配置文件定义不同角色的行为边界、关注点和输出格式，让多 Agent 协作模拟人类团队的分工协作——架构师、工程师、审查者各司其职。

## 关键内容

1. **角色定义结构**：每个角色包含 `config_path`（独立配置路径）、`guidance`（行为指引文本）、`display_names`（多实例时的随机昵称）。角色在配置文件中声明，运行时动态加载。
2. **专业分工机制**：不同角色注入不同的 system prompt，限制其行为边界。例如 coder 角色"专注实现，不跨模块边界"；reviewer 角色"只提建议不改代码"；documenter 角色"负责技术文档生成"。
3. **角色与工具的绑定**：不同角色可配备不同的工具集——coder 拥有文件读写和执行权限，reviewer 仅有只读访问和建议输出权限。
4. **降低不确定性的核心机制**：当 Agent 角色不专业、泛化处理时，Role System 通过注入专业 guidance 约束输出范围，减少"万金油"式低质量响应。
5. **工程哲学**：Multi-Agent 的本质是把"人类团队的分工协作"映射到 AI Agent 层面。好的团队有架构师、工程师、Review 者各司其职，Role 系统让不同 subagent 扮演不同角色。

## 典型角色类型

| 角色 | 关注点 | 约束 |
|------|--------|------|
| Coder | 代码质量、测试覆盖、边界情况 | 不修改架构、不跨模块边界 |
| Reviewer | 安全漏洞、性能问题、API 设计 | 不直接改代码，只提建议 |
| Documenter | API 文档、README、架构决策记录 | 专注于文档生成 |

## 来源
- [[raw/articles/ai-tools/codex/07_codex_multi_agent.md]] — Codex CLI 深度解析 Vol.7：Multi-Agent 并行编码的调度与协同

## 相关
- [[Codex多Agent调度]] — 在 Codex 中通过 config.toml 实现角色系统 (implements)
- [[Orchestrator-Subagent-Pattern]] — 角色系统是协调器-子智能体模式的专业化扩展 (part_of)
- [[Multi-Agent Orchestration]] — 多 Agent 编排中的角色分工维度 (part_of)
- [[纵深防御]] — 角色分工是不确定性降低的软层防线 (relates_to)
