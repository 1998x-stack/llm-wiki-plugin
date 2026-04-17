---
type: entity
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 2
tags: [AI, 工具, Agent系统]
aliases:
- SWE-agent
- Software Engineering Agent
relates_to:
- target: "[[SWE-bench]]"
  type: uses
  confidence: 0.95
- target: "[[ReAct 风格循环]]"
  type: implements
  confidence: 0.9
- target: "[[Agent计算机接口]]"
  type: uses
  confidence: 0.9
- target: "[[Agent 轨迹分析]]"
  type: caused
  confidence: 0.85
  note: SWE-agent 的运行产生了可分析的轨迹数据
- target: "[[Trajectory Schema]]"
  type: implements
  confidence: 0.9
- target: "[[Edit 后验证]]"
  type: uses
  confidence: 0.9
supersedes: null
---

# SWE-agent

## 概述

SWE-agent 是由 Princeton 团队（2024）开发的 AI Agent 系统，能将 LLM 转化为软件工程师，自动修复 GitHub 仓库中的真实 issue 和 bug。通过专门设计的 Agent 计算机接口（ACI）和 [[ReAct 风格循环]]，在 [[SWE-bench]] 上取得显著优于直接输出 patch 的效果。

## 关键内容

### 核心架构

1. **[[ReAct 风格循环]]**：每一步生成 thought（思考）和 action（命令），再接收 observation（[[环境反馈设计|环境反馈]]），形成"想一点、做一点、看反馈、再想一点"的交互循环。
2. **Agent 计算机接口（ACI）**：为 LLM 专门设计的工具集，包括文件浏览、编辑、搜索、lint 检查等，而非简单复用人类 CLI 工具。
3. **Trajectory 落盘**：每次运行产生 `.traj` 文件，记录完整的 thought/action/observation 序列，支持事后分析和调试。

### SWE-bench 表现

- [[SWE-bench]] Full：**12.47%** resolved（GPT-4 Turbo）
- [[SWE-bench]] Lite：**18.00%** resolved（GPT-4 Turbo）
- pass@k 曲线：k=6 时解决率升至 30%+

### Trajectory 格式

SWE-agent 的 `.traj` 文件是 JSON 格式，核心结构包含：
- 顶层：`environment`、`trajectory` 数组
- 每步：`response`（模型原文）、`thought`（解析后的思考）、`action`（执行的命令）、`observation`（[[环境反馈设计|环境反馈]]）、`state`（环境状态）、`query`（发送给模型的输入）
- 版本差异：1.1.0 之前用 `message` 字段表示输入，1.1.0 起改为 `query` 表示精确输入

### Edit 后验证

SWE-agent 在每次 edit 后立即运行轻量级校验：
- `USE_LINTER` 开关控制是否启用 linter
- 默认使用 `flake8 --select=F821,F822,F831,E111,E112,E113,E999,E902` 对 .py 文件做单文件检查
- 引入语法错误的编辑会被拒绝（"Your changes have NOT been applied"）
- 做了 **previous errors filtering**：更新旧错误行号，过滤编辑窗口外的旧问题，只保留本次 edit 新引入的错误
- 官方主线没有内建完整 LSP 验证，更偏向"快速、局部、可恢复"的 lint/syntax 检查

### 工程化建议

自定义实现时建议顶层补充：`instance_id`、`schema_version`、`run_id`、`agent_version`、`model_name`、`config_ref`、`info`。
Step 级建议补充：`step_id`、`timestamp_start`、`timestamp_end`、`parse_error`、`exit_code`、`tool_name`、`tool_args`、`observation_type`、`cost`、`tokens_prompt`、`tokens_completion`。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/08-trajectory常见字段 schema包含哪些，分别什么意思，分别如何构造.md]] — SWE-agent trajectory schema 详解
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/10-swe-agent 每次 edit后，如何设计lintlsp 等validate？.md]] — Edit 后 validate 设计详解

## 相关

- [[SWE-bench]] — uses（基准测试平台）
- [[ReAct 风格循环]] — implements（运行框架）
- [[Agent计算机接口]] — uses（专门设计的工具接口）
- [[Agent 轨迹分析]] — caused（产生可分析的轨迹数据）
- [[Trajectory Schema]] — implements（定义了 trajectory 的数据结构）
- [[Edit 后验证]] — uses（每次 edit 后运行 lint/syntax 检查）
