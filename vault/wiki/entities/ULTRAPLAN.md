---
type: entity
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [cloud-service, ai-computing, remote-execution]
aliases: ["ULTRAPLAN", "云端算力扩展", "Cloud Container Runtime", "CCR"]
relates_to:
  - target: "[[KAIROS]]"
    type: part_of
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[Remote Computing]]"
    type: implements
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# ULTRAPLAN

## 概述
ULTRAPLAN是[[Claude Code]]中的云端算力外包系统，可将复杂规划任务外包给远程强力算力进行处理。

## 关键内容
1. **工作原理**：
   - 将复杂任务发送到云端容器运行时（Cloud Container Runtime）
   - 在云端运行[[Claude_Opus_4.6|Claude Opus 4.6]]（Fennec）模型
   - 云端任务最长可运行30分钟
   - 适用于复杂架构规划、大规模[[重构]]方案等任务

2. **传送机制**：
   - 使用特殊哨兵值__ULTRAPLAN_TELEPORT_LOCAL__进行本地/云端状态同步
   - 云端任务完成后，结果通过浏览器弹窗展示给用户
   - 用户批准后，系统将结果注入本地终端

3. **技术特点**：
   - 实现了优雅的本地-云端-浏览器状态同步
   - 从Agent视角看，这只是一个普通工具调用
   - 实际上触发了跨平台状态同步流程

## 来源
- [[Claude Code 源码泄露深度解析（五）：KAIROS——"合适时机"的自主守护进程与 AutoDream]] — 194-234行

## 相关
- [[KAIROS]] — part_of
- [[Claude Code]] — part_of
- [[Remote Computing]] — implements