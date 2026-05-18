---
type: entity
status: active
confidence: 0.7
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [可靠性工程, 组织, 实践, AI工程]
aliases: ["Site Reliability Engineering", "站点可靠性工程", "SRE"]
relates_to:
  - name: Postmortem 文化
    type: relates_to
  - name: 彩虹部署
    type: relates_to
  - name: 行为回归测试
    type: relates_to
supersedes: null
---

# SRE

## 概述
SRE（Site Reliability Engineering，站点可靠性工程）是将软件工程方法应用于基础设施和运维问题的学科，旨在构建可扩展、高可靠的软件系统。

## 关键内容

1. **核心定义**：SRE 是 [[Google]] 首创的工程实践学科，将软件工程方法应用于运维问题。SRE 工程师负责构建和维护可靠、可扩展的系统，通过自动化手段减少人工运维负担。SRE 的核心指标包括可用性、延迟、性能和效率。

2. **在 AI 系统中的适应性**：传统软件的 SRE 体系需要适应 AI 系统的特殊性。AI 系统的 [[Postmortem 文化|Postmortem]] 实践仍处于早期阶段，需要新的方法论来处理概率性失败、[[涌现行为]]和不可重现性问题。SRE 在 AI 系统中不仅要监控技术指标，还要监控行为质量指标。

3. **与 [[Postmortem 文化|Postmortem]] 的关系**：[[Postmortem 文化|Postmortem]] 是 SRE 体系的核心实践之一。SRE 强调通过[[Postmortem 文化|事后回顾]]将故障转化为学习机会，推动系统级改进。[[Anthropic]] 的 [[Postmortem 文化|Postmortem]] 实践体现了 SRE 文化在 AI 公司中的应用。

4. **关键实践**：快速止血与根本原因修复的双轨制、[[Configuration|配置]]即代码（[[Configuration]] as Code）、[[金丝雀发布]]和[[彩虹部署|渐进式部署]]、自动化监控和告警、错误预算（Error Budget）管理。在 AI 系统中，还需要模型级回退、Prompt 级回退等特有手段。

## 来源
- [[18_postmortem.md]] — Anthropic Engineering Blog 原文《A postmortem of three recent issues》

## 相关
- [[Postmortem 文化]] — relates_to（Postmortem 是 SRE 的核心实践）
- [[彩虹部署]] — relates_to（金丝雀发布是 SRE 的部署策略）
- [[行为回归测试]] — relates_to（行为回归测试是 AI 系统中 SRE 质量保障的扩展）
