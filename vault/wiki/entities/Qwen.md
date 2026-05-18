---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [llm, ai-api, alibaba-cloud, AI工程]
aliases: ["Qwen", "Qwen LLM", "通义千问"]
relates_to: 
  - target: "[[TITAN-智能体]]"
    type: uses
    confidence: 0.9
  - target: "[[LangGraph]]"
    type: integrates_with
    confidence: 0.9
  - target: "[[DashScope]]"
    type: accessed_via
    confidence: 0.9
  - target: "[[决策节点]]"
    type: powers
    confidence: 0.9
entity_type: tool
supersedes: null
---

# Qwen

## 概述
Qwen是阿里巴巴推出的大型[[Language-Model|语言模型]]，通过百炼(DashScope)API提供[[服务]]，在[[TITAN-智能体|TITAN]]智能体中用于决策和反思等任务。

## 关键内容

1. **集成方式**：
   - 通过百炼(DashScope) API访问Qwen模型
   - 使用兼容[[OpenAI]]协议的接口进行HTTP调用
   - 在[[TITAN-智能体|TITAN]]系统中使用qwen-turbo模型，超时时间为60秒

2. **应用场景**：
   - 决策节点：基于当前游戏状态选择下一步动作
   - 反思机制：分析智能体卡住的原因并提出解决方案
   - 知识注入：理解游戏规则和目标

3. **客户端实现**：
   - QwenClient类封装API调用逻辑
   - 自动统计总调用次数和Token消耗
   - 支持温度参数调节以控制输出随机性

## 来源
- [[TITAN-技术框架核心点报告]] — 第4节LLM客户端和第7节知识注入

## 相关
- [[TITAN-智能体]] — uses
- [[LangGraph]] — integrates_with
- [[DashScope]] — accessed_via
- [[决策节点]] — powers