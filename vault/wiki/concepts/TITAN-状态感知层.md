---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI-Agent, Game-Testing, Perception, State-Abstraction, AI工程]
aliases: ["TITAN Perception Layer", "TITAN状态感知层", "State Perception and Abstraction"]
relates_to: 
  - target: "[[TITAN 框架]]"
    type: part_of
    confidence: 0.9
  - target: "[[TITAN-同步帧协议]]"
    type: builds_on
    confidence: 0.8
supersedes: null
---

# TITAN-状态感知层

## 概述
[[TITAN 框架|TITAN]]框架中的感知抽象层，负责将游戏内部状态转换为LLM可理解的自然语言描述，同时过滤动态动作空间以提供有效的操作选项。

## 关键内容

1. **三层状态转换**：
   - Lua游戏对象 → JSON结构化数据 → 自然语言描述 → LLM输入
   - 在每一层都进行信息筛选和抽象，降低噪声

2. **游戏状态导出**：
   - 每个游戏实现_getTestState()函数导出关键状态字段
   - 不同游戏导出不同的状态信息（如蛇的位置、俄罗斯方块当前方块、飞翔的小鸟高度等）
   - 提取决策相关的关键信息，省略渲染细节

3. **自然语言抽象**：
   - 将原始JSON数据转换为简洁的自然语言描述
   - 设计原则是只保留决策相关信息，省略渲染细节，降低Token消耗
   - 例如将{"snake": [{"x":12,"y":10}], "food": {"x":15,"y":8}}转换为"Snake game. Score: 30. Head at (12, 10), moving right. Food at (15, 8)."

4. **动态动作空间过滤**：
   - 根据游戏状态动态调整可用动作列表
   - 游戏结束时只返回重启键，开始界面只返回空格键
   - 确保LLM只考虑当前可执行的有效动作

## 来源
- [[TITAN-技术框架核心点报告]] — 核心技术点五

## 相关
- [[TITAN 框架]] — part_of
- [[TITAN-同步帧协议]] — builds_on
- [[Qwen-LLM]] — relates_to
- [[State-Abstraction]] — relates_to