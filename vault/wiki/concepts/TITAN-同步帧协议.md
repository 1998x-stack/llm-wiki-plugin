---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI-Agent, Game-Testing, Protocol, Synchronization, AI工程]
aliases: ["Sync Frame Protocol", "同步帧协议", "TITAN Sync Protocol"]
relates_to: 
  - target: "[[TITAN 框架]]"
    type: part_of
    confidence: 0.9
  - target: "[[TITAN-状态感知层]]"
    type: enables
    confidence: 0.8
supersedes: null
---

# TITAN-同步帧协议

## 概述
[[TITAN 框架|TITAN]]框架中的一种[[同步通信]]协议，通过阻塞式I/O让游戏引擎等待LLM决策，解决LLM推理延迟与游戏实时性之间的矛盾。

## 关键内容

1. **设计动机**：
   - LLM推理耗时1-3秒，而游戏帧率60FPS，异步模式下LLM还在思考时游戏可能已结束
   - 同步协议让游戏"冻结"等待智能体决策，确保LLM有充足时间处理

2. **协议机制**：
   - 时间步长：固定dt = 1/60s，消除真实时间依赖，测试结果可复现
   - I/O模式：阻塞式fgets()，游戏帧率完全由智能体驱动
   - 帧推进：1命令 = 1帧，精确控制，无帧跳过
   - 空推进：{"action":"tick"}允许不按键只观察的帧

3. **消息格式**：
   - Engine → Agent: JSON包含type, frame, dt, fps, game_state, error等字段
   - Agent → Engine: 支持keypressed, tick, screenshot, quit等动作

4. **实现要点**：
   - 游戏引擎在[[C语言]]中实现同步循环：阻塞等待 → 处理 → 推进 → 发射状态
   - 每次发送状态后阻塞等待stdin输入，直到收到智能体指令才继续

## 来源
- [[TITAN-技术框架核心点报告]] — 核心技术点一

## 相关
- [[TITAN 框架]] — part_of
- [[TITAN-状态感知层]] — enables
- [[LangGraph]] — relates_to
- [[Qwen-LLM]] — relates_to