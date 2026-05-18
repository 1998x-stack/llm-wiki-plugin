---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI-Agent, Game-Testing, Bug-Detection, Diagnostic-System, AI工程]
aliases: ["Diagnosis Oracle System", "诊断预言机系统", "TITAN Oracle System"]
relates_to: 
  - target: "[[TITAN 框架]]"
    type: part_of
    confidence: 0.9
  - target: "[[TITAN-框架]]"
    type: extends
    confidence: 0.8
supersedes: null
---

# TITAN-诊断预言机系统

## 概述
[[TITAN 框架|TITAN]]框架中的Bug检测系统，通过多个独立的检测器监控游戏状态，自动发现各类问题并生成Finding报告。

## 关键内容

1. **系统架构**：
   - 基于多个独立预言机的设计，可分别启用/禁用/扩展
   - 预言机接收帧数据和游戏状态，输出Finding数组
   - 检测类型包括崩溃、卡死、逻辑异常和性能问题

2. **四个核心预言机**：
   - **CrashOracle（崩溃检测）**：检测进程崩溃和Lua运行时错误，严重程度critical
   - **HangOracle（卡死检测）**：检测游戏状态完全冻结，连续N帧hash相同，严重程度important  
   - **LogicOracle（逻辑异常检测）**：检测违反游戏规则的状态转换（如分数减少、生命值异常增加），严重程度important
   - **PerformanceOracle（[[性能审查|性能检测]]）**：检测帧时间异常飙高（dt > 0.1s），严重程度minor

3. **Finding数据结构**：
   - 包含type（crash/lua_error/hang/logic_bug/performance）、severity、step、description和evidence字段
   - 每个发现都带有详细的证据和描述，形成完整的Bug证据链

4. **设计优势**：
   - 解耦设计：每个Bug检测器独立实现，便于维护和扩展
   - 证据链完整：Finding + 截图 + 日志 + 反思，形成完整证据
   - 可[[Configuration|配置]]阈值：可根据需要调整检测敏感度

## 来源
- [[TITAN-技术框架核心点报告]] — 核心技术点四

## 相关
- [[TITAN 框架]] — part_of
- [[TITAN-框架]] — extends
- [[TITAN-报告生成系统]] — relates_to
- [[Bug-Detection]] — relates_to