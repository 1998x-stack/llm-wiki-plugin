---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["ai-engineering", "experiment", "case-study"]
aliases: ["OpenAI Codex Agent Experiment", "OpenAI百万行代码实验"]
relates_to:
  - target: "[[Harness-Engineering]]"
    type: relates_to
    confidence: 0.9
  - target: "[[OpenAI]]"
    type: part_of
    confidence: 0.8
  - target: "[[Codex]]"
    type: uses
    confidence: 0.9
  - target: "[[Harness-Engineering与控制论]]"
    type: relates_to
    confidence: 0.7
supersedes: null
---

# OpenAI百万行代码实验

## 概述
[[OpenAI]]进行的一项实验，展示了3名工程师在5个月内使用[[Codex CLI|Codex]] Agent从空[[仓库]]构建了超过100万行代码的产品，所有代码均由AI生成，无一行手写。

## 关键内容

1. **实验[[Settings|设置]]**：
   - 参与人员：3名工程师
   - 时间周期：5个月
   - 提交数量：大约1,500个PR（平均每人每天3.5个）
   - 代码总量：超过100万行代码
   - 生成方式：所有代码由[[Codex CLI|Codex]]生成，无一行手写

2. **早期挑战**：
   - 进展比预期慢，不是因为[[Codex CLI|Codex]]编码能力不足
   - 主要原因是环境未搭建好，Agent不了解项目依赖结构、架构约束
   - 无法验证产出的正确性
   - AI表现出类似新人入职的体验：能力没问题，但不了解组织规矩

3. **解决方案 - 规则编码**：
   - 将项目规则写下来，让机器能读懂
   - 设计严格的依赖方向：Types → Config → Repo → Service → Runtime → UI
   - 将约束编码成自定义Linter规则，CI自动拒绝违规代码
   - 创建约100行的[[项目约定手册|AGENTS.md]]，称为"地图，而不是百科全书"

4. **关键创新**：
   - 本地可观测性系统：每个git worktree启动独立应用实例
   - Agent通过Chrome Dev[[Tool System|Tools]] Protocol直接操控浏览器验证UI
   - Agent可随时查看自己产出的效果，无需人工检查

5. **自动化清理**：
   - 团队最初每周花费20%时间清理Agent产生的"AI slop"（风格不一致、过度抽象、命名奇怪的代码）
   - 后来将清理标准编码为"golden principles"，让[[Codex CLI|Codex]]根据原则自动[[重构]]
   - 实现从人工清理到自动清理的反馈回路闭合

6. **核心哲学**：
   - "[[Humans-steer-Agents-execute|Humans steer. Agents execute.]]"（人负责掌舵，Agent负责执行）
   - 工程师角色从写代码转变为设计让代码被正确写出来的系统

## 来源
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — 关于OpenAI实验的详细描述
- [[Harness Engineering: Leveraging Codex in an Agent-First World]] — OpenAI原始报告

## 相关
- [[Harness-Engineering]] — relates_to
- [[OpenAI]] — relates_to
- [[Codex]] — relates_to
- [[Agent-Native-Architecture]] — relates_to
- [[Harness-Engineering与控制论]] — relates_to