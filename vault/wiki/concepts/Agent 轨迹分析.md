---
type: concept
title: Agent 轨迹分析
status: active
confidence: 0.9
created: 2026-04-16
updated: 2026-04-16
last_accessed: '2026-04-16'
source_count: 2
tags: [AI, 方法论, AI工程]
aliases:
- Trajectory Analysis
- 轨迹分析
- 失败模式分析
relates_to:
- target: '[[ReAct 风格循环]]'
  type: uses
  confidence: 0.95
- target: '[[Agent计算机接口]]'
  type: uses
  confidence: 0.9
- target: '[[恢复机制]]'
  type: uses
  confidence: 0.85
- target: '[[Trajectory Schema]]'
  type: uses
  confidence: 0.95
supersedes: null
---

# Agent 轨迹分析

## 概述

Agent 轨迹分析是对 [[SWE-agent]] 运行过程中产生的 thought/action/observation 序列进行结构化分析的方法论，用于定位失败根因、理解行为模式、优化 ACI 设计。

## 关键内容

### 轨迹格式

**论文中的消息轨迹（Figure 9）：**
```
System prompt
Demonstration（可选）
Issue statement
→ 多轮循环：
    agent 输出 Thought & Action
    environment 返回 Environment Response
    老的 observation 可以被 collapsed
→ 最终 agent Submit
→ 系统产出 Patch File
```

**落盘后的 .traj 文件（JSON 格式）：**
- `trajectory`：逐步 action/observation 记录
- `history`：完整消息历史
- `info`：执行结果、token/cost、submission 等元信息
- `replay_config`：复现配置

单步记录包含：`thought`、`action`、`observation`、`response`、`execution_time`。

### 四层分析法

#### 第一层：看轨迹有没有走对"阶段"

成功轨迹通常经历：定位/搜索 → 打开相关文件 → 编辑 → 运行验证 → 清理并 submit。

| 异常表现 | 可能问题 |
|---------|---------|
| 长时间停留在 find_file/search_dir/open | [[Localization]] 问题 |
| 长时间在 edit/edit/edit 来回打转 | 编辑稳定性/恢复失败 |
| edit 完但没有有效测试 | 验证链路不足 |

#### 第二层：看动作序列有没有异常模式

| 异常模式 | 表现 | 对应失败类型 |
|---------|------|------------|
| 搜索-浏览循环过长 | find_file → open → scroll_down → search_file → ... | Failed to Find Relevant File |
| 编辑循环过长 | edit → error → edit → error → ... | Failed to Recover from Edit（23.4%） |
| 过早 submit | 没建立可靠 reproduction/testing 就 submit | Incorrect Implementation（52.0%） |

#### 第三层：看 observation 是否支持下一步决策

检查：
- action 执行后，observation 有没有明确告诉 agent 状态变了什么
- edit 后有没有看到更新后的窗口
- lint/syntax error 时有没有拿到错误位置和局部 before/after
- 测试命令有没有暴露出真正失败原因

#### 第四层：把轨迹、生成 patch、gold patch 放在一起看

论文的做法：把 agent trajectory + agent patch + gold patch 三者一起交给模型做失败分类。LM 标签和手工标签一致率达 87%。

### 根因链诊断框架

**五步诊断法：**

1. **看终止方式**：submit / cost limit / 连续 format errors
2. **给动作分阶段**：[[Localization]] → Reproduction → Editing → Verification → Submission
3. **找第一个坏拐点**：打开错误文件、无意义搜索循环、第一次 invalid edit 后没恢复
4. **对照最终 patch**：与 gold patch 对比判断是 localization 还是 implementation 问题
5. **给出"根因 + 表现 + 证据"**：不要只说"失败了"，要说明在哪个 turn 开始不可逆地走偏

### 失败模式分类

论文对 [[SWE-bench]] Lite 未解决的 248 条轨迹做分析，主要失败类包括：

| 失败类型 | 占比 | 说明 |
|---------|------|------|
| Incorrect Implementation | ~52%（与 Overly Specific 合计） | 方案本身不够对 |
| Overly Specific Implementation | 同上 | 改法太特例化 |
| Failed to Recover from Edit | ~23.4% | 编辑失败后恢复不了 |
| Failed to Find Edit Location | — | 找到文件但没找到具体位置 |
| Failed to Find Relevant File | — | 文件级定位失败 |
| Failed to Reproduce | — | 没复现成功就盲改 |
| Ran Out of Budget | — | 预算耗尽 |

### 关键洞察

> "最终失败标签回答'死法是什么'，而根因分析回答'是在哪个 turn 开始不可逆地走偏'。"

判断失败原因，最好不要只看轨迹本身，而要把"行为过程 + 最终产物 + 理想产物"三者联合起来。

## 来源

- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/07-SWE-agent 轨迹 格式长什么样，怎么进行分析，怎么判断轨迹中哪些问题导致了后续任务的失败？.md]] — SWE-agent 轨迹分析方法论
- [[raw/ChatGPT-Chat/ChatGPT-SWE-agent 论文核心观点/08-trajectory常见字段 schema包含哪些，分别什么意思，分别如何构造.md]] — Trajectory schema 字段详解

## 相关

- [[ReAct 风格循环]] — uses（轨迹分析基于 thought/action/observation 循环）
- [[Agent计算机接口]] — uses（轨迹反映 ACI 设计的有效性）
- [[恢复机制]] — uses（轨迹分析揭示恢复机制的有效性）
- [[Trajectory Schema]] — uses（轨迹分析基于 trajectory schema 的字段结构）
