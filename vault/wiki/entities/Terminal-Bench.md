---
type: entity
status: active
confidence: 0.8
created: 2026-04-20
updated: 2026-04-20
last_accessed: 2026-04-20
source_count: 1
tags: [基准测试, 终端, 通用Agent, 评测, AI工程]
aliases: ["Terminal-Bench", "Terminal Bench"]
relates_to:
  - target: "[[评测驱动开发]]"
    type: uses
  - target: "[[SWE-bench]]"
    type: compares_to
supersedes: null
---

# Terminal-Bench

## 概述
Terminal-Bench 是通用终端任务的评测基准，用于评估 AI Agent 在命令行环境中的任务完成能力。

## 关键内容

1. **评测目标**：
   - 评估 Agent 在终端/命令行环境中的操作能力
   - 涵盖文件操作、系统管理、脚本编写等通用任务
   - 提供标准化的终端任务[[Evaluation Harness|评测框架]]

2. **在评测体系中的位置**：
   - 与 [[SWE-bench]]（代码修复）、[[τ-Bench]]（对话）共同构成多维度 [[评测驱动开发|Agent 评测]][[矩阵]]
   - 被 [[Anthropic]] 用于[[基础设施噪声]]量化研究（不同资源[[Configuration|配置]]对成功率的影响达 6 个百分点）

3. **相关研究**：
   - [[Anthropic]] 团队发现 Terminal-Bench 上资源[[Configuration|配置]]差异导致的结果波动
   - 推荐 requests 和 limits 之间保持 3× 带宽以获得稳定结果

## 来源
- [[raw/articles/ai-engineering/anthropic-engineering/claude-engineering/12_demystifying_evals.md]] — 参考与扩展阅读

## 相关
- [[评测驱动开发]] — uses（Terminal-Bench 是通用 Agent 评测的标准工具）
- [[SWE-bench]] — compares_to（不同领域的 Agent 评测基准）
- [[基础设施噪声]] — relates_to（Terminal-Bench 是基础设施噪声研究的主要平台）
