---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-agent, proactive-system, timing, AI工程]
aliases: ["Proactive Agent", "主动智能代理", "Proactivity", "主动性"]
relates_to:
  - target: "[[KAIROS]]"
    type: extends
  - target: "[[Claude Code]]"
    type: part_of
  - target: "[[AI Agent Paradigm]]"
    type: part_of
supersedes: null
---
<!-- relates_to 示例:
relates_to:
  - target: "[[相关页面]]"
    type: extends       # uses|depends_on|contradicts|caused|extends|implements|supersedes|part_of|compares_to
-->

# Proactive Agent

## 概述
Proactive Agent是指能够主动监控环境、预测需求并采取行动的AI代理，区别于传统的被动响应式AI系统。

## 关键内容
1. **发展阶段**：
   - 阶段一：被动问答（[[ChatGPT]][[规范化理论|范式]]）- 用户问 → AI答 → 等待
   - 阶段二：主动执行（[[Claude Code]]当前版本）- 用户请求 → AI规划 → AI执行 → 等待
   - 阶段三：自主守护（[[KAIROS]][[规范化理论|范式]]）- AI持续监控 → 在[[KAIROS|合适时机]]主动行动 → 用户回来时已有积累

2. **核心特征**：
   - 常驻守护进程模式：AI持续存在，不需要每次显式召唤
   - 主动感知能力：持续监控环境变化并做出响应
   - 时机选择机制：在[[KAIROS|合适时机]]采取行动，避免干扰用户工作流
   - 状态维护：在后台维持长期状态和上下文

3. **技术实现**：
   - 定时器机制：定期接收信号并分析当前状态
   - 文件监控：监视文件系统变化
   - Webhook集成：订阅外部[[服务]]事件（如[[GitHub]]）
   - 简洁输出模式：克制地向用户报告重要信息

## 来源
- [[Claude Code 源码泄露深度解析（五）：KAIROS——"合适时机"的自主守护进程与 AutoDream]] — 291-300行

## 相关
- [[KAIROS]] — extends
- [[Claude Code]] — part_of
- [[AI Agent Paradigm]] — part_of