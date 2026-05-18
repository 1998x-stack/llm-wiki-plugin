---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, memory-integration, claude-code, AI工程]
aliases: ["AutoDream", "AI睡眠记忆整合"]
relates_to:
  - target: "[[KAIROS]]"
    type: part_of
  - target: "[[Memory Consolidation]]"
    type: implements
  - target: "[[Claude Code]]"
    type: part_of
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# AutoDream

## 概述
AutoDream是[[Claude Code]]中的AI[[Memory Consolidation|记忆整合]]系统，灵感来自人类睡眠时的[[Memory Consolidation|记忆整合]]机制，用于在后台自动整理和巩固AI的记忆。

## 关键内容
1. **生物学灵感**：
   - 灵感来自人类快速眼动睡眠（REM Sleep）中的[[Memory Consolidation|记忆整合]]机制
   - 模拟大脑回放、整合和巩固白天记忆的过程
   - 去除不重要细节，强化关键知识，解决认知矛盾

2. **工作流程**：
   - 用户闲置超过阈值时自动启动
   - Fork一个独立的子Agent，与主Agent上下文完全隔离
   - 读取当日[[KAIROS]]日志和[[MEMORY.md]] topic files
   - 整合处理：合并相关观察、检测并解决逻辑矛盾、升华临时观察为验证事实、识别新模式、删除过时信息
   - 更新记忆文件和归档日志

3. **技术特点**：
   - 使用独立子Agent避免"思路污染"
   - 提供原子性操作：整合结果要么完全成功要么完全不影响
   - 具备独立失败机制，不影响主会话

## 来源
- [[Claude Code 源码泄露深度解析（五）：KAIROS——"合适时机"的自主守护进程与 AutoDream]] — 88-153行

## 相关
- [[KAIROS]] — part_of
- [[Memory Consolidation]] — implements
- [[Claude Code]] — part_of