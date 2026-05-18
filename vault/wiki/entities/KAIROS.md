---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, proactive-system, claude-code, AI工程]
aliases: ["KAIROS", "KAIROS守护进程", "合适时机"]
relates_to:
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[AutoDream]]"
    type: extends
  - target: "[[Proactive Agent]]"
    type: implements
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# KAIROS

## 概述
KAIROS是[[Claude Code]]中的自主守护进程系统，源自古希腊语"合适时机"，实现AI在合适时机主动行动而非被动响应的功能。

## 关键内容
1. **常驻守护进程模式**：
   - 将[[Claude Code]]从"被动响应"工具变为"主动运作"的Agent
   - 定时接收tick信号，分析当前状态并决定是否主动行动
   - 在用户闲置超过阈值时启动[[AutoDream]]进行[[Memory Consolidation|记忆整合]]

2. **append-only日志系统**：
   - 维护按天追加的日志文件（~/.claude/kairos/）
   - 记录Observations（观察）、Decisions（决策）、Actions（行动）、Hypotheses（假设）
   - 为[[AutoDream]]系统提供原材料

3. **专属工具集**：
   - FileWatchTool：监控文件系统变化
   - GitWebhookTool：订阅Git[[仓库]]事件
   - DreamTool：触发[[Memory Consolidation|记忆整合]]
   - CronScheduler：[[Cron 调度系统|定时任务调度]]
   - Background[[BashTool]]：后台执行长时间命令

## 来源
- [[Claude Code 源码泄露深度解析（五）：KAIROS——"合适时机"的自主守护进程与 AutoDream]] — 1-150行

## 相关
- [[Claude Code]] — part_of
- [[AutoDream]] — extends
- [[Proactive Agent]] — implements