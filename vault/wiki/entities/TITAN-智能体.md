---
type: entity
status: active
confidence: 0.9
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [ai-testing, agent, game-testing, langgraph, AI工程]
aliases: ["TITAN", "Testing Intelligent Trigger Agent for Novel bugs"]
relates_to: 
  - target: "[[LangGraph]]"
    type: uses
    confidence: 0.9
  - target: "[[Qwen]]"
    type: uses
    confidence: 0.9
  - target: "[[同步帧协议]]"
    type: implements
    confidence: 0.9
  - target: "[[诊断预言机系统]]"
    type: implements
    confidence: 0.9
entity_type: project
supersedes: null
---

# TITAN-智能体

## 概述
[[TITAN 框架|TITAN]]（Testing Intelligent Trigger Agent for Novel bugs）是一个基于LangGraph和[[Qwen|Qwen LLM]]的自动化游戏测试智能体，采用[[TITAN-同步帧协议|同步帧协议]]与游戏通信，通过多个诊断预言机检测Bug。

## 关键内容

1. **核心功能**：
   - [[LLM]]驱动的黑盒游戏测试智能体，不修改游戏代码
   - 通过标准化JSON协议与游戏进程通信，像人类测试员一样"玩"游戏
   - 运行多个诊断预言机检测Bug，包括崩溃、卡死、逻辑异常等

2. **技术特点**：
   - 实现[[TITAN-同步帧协议|同步帧协议]]，让游戏"冻结"等待智能体决策，解决LLM推理耗时与游戏高帧率的矛盾
   - 使用LangGraph构建[[LangGraph状态机|状态机工作流]]，包含感知、决策、执行、监控、反思等节点
   - 采用[[LLM推理策略|频率控制策略]]，每5步调用一次LLM以节省API调用成本

3. **架构组成**：
   - [[状态感知与抽象|感知层]]：将Lua游戏对象转换为JSON结构化数据再抽象为自然语言描述
   - [[LangGraph状态机]]：7节点状态图（perceive → optimize_actions → decide → execute → monitor → [reflect/report]）
   - [[TITAN-诊断预言机系统|诊断预言机系统]]：包括崩溃检测、卡死检测、逻辑异常检测和[[性能审查|性能检测]]四个模块

## 来源
- [[TITAN-技术框架核心点报告]] — 整个文档

## 相关
- [[LangGraph]] — uses
- [[Qwen]] — uses
- [[同步帧协议]] — implements
- [[诊断预言机系统]] — implements
- [[LLM]] — relates_to