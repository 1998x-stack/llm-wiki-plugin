---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [game-engine, c-language, lua, sdl2, Lua编程]
aliases: ["Luna Engine"]
relates_to: 
  - target: "[[TITAN-智能体]]"
    type: connects_to
    confidence: 0.8
  - target: "[[同步帧协议]]"
    type: implements
    confidence: 0.8
  - target: "[[SDL2]]"
    type: uses
    confidence: 0.8
  - target: "[[Lua]]"
    type: uses
    confidence: 0.8
entity_type: project
supersedes: null
---

# Luna-Engine

## 概述
Luna Engine是一个基于[[C语言]]、Lua脚本和SDL2的游戏引擎，采用类似[[Love2D]]的设计风格，用于支持多种游戏的开发和测试。

## 关键内容

1. **技术栈**：
   - 使用C11语言编写引擎核心
   - 集成Lua 5.4作为游戏逻辑脚本语言
   - 采用SDL2进行图形渲染和输入处理
   - 实现同步测试循环，支持与外部智能体的[[同步通信]]

2. **架构特性**：
   - 支持多种游戏类型，包括贪吃蛇、俄罗斯方块、飞扬的小鸟、打砖块、太空射击和2048等
   - 每个游戏实现_getTestState()函数以导出结构化状态信息
   - 提供标准化的JSON接口与外部系统通信

3. **同步协议实现**：
   - 实现阻塞式fgets()等待外部输入
   - 固定时间步长(dt = 1/60s)确保测试可复现性
   - 1命令=1帧的精确控制机制

## 来源
- [[TITAN-技术框架核心点报告]] — 第1节系统总览及第2节同步帧协议实现

## 相关
- [[TITAN-智能体]] — connects_to
- [[同步帧协议]] — implements
- [[SDL2]] — uses
- [[Lua]] — uses