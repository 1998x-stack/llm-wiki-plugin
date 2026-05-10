---
type: concept
status: active
confidence: 0.75
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [AI-Agent, Automated-Testing, Video-Game-Testing, GPT-4o, langgraph, qwen]
aliases: [“TITAN Framework”, “TITAN”, “Testing Intelligent Trigger Agent for Novel bugs”]
relates_to: 
  - target: “[[TITAN-智能体]]”
    type: extends
    confidence: 0.8
  - target: “[[GPT-4o]]”
    type: originally_uses
    confidence: 0.7
  - target: “[[Qwen]]”
    type: implementation_uses
    confidence: 0.8
  - target: “[[LangGraph]]”
    type: implements_similar_pattern_as
    confidence: 0.8
  - target: “[[同步帧协议]]”
    type: core_component
    confidence: 0.8
  - target: “[[诊断预言机系统]]”
    type: core_component
    confidence: 0.8
supersedes: null
---

# TITAN 框架

## 概述
[[TITAN-智能体|TITAN]]框架是一个AI驱动的自动游戏测试框架，最初基于GPT-4o实现，后来有类似实现基于LangGraph和Qwen构建为[[TITAN-智能体|TITAN]]智能体。该框架模仿真人测试员的思路进行自动化测试，包含感知、动作优化、反射推理和问题诊断等模块。

## 关键内容

1. **感知抽象模块（Perception Abstraction Module）**：
   - 帮助AI理解并简化游戏信息
   - 删除无用信息，将复杂数字转换为简单文字（如血量：高/中/低）
   - 提供给AI干净、简短的信息
   - 快速适配不同游戏，帮助AI”读明白”游戏而不负担过重
   - 在[[TITAN-智能体|TITAN]]智能体中实现为[[状态感知与抽象]]层

2. **动作优化模块（Action Optimization Module）**：
   - 帮助AI只执行有用的操作
   - 定义通用动作模板（移动、对话、攻击、使用道具等）
   - 结合游戏经验，仅推荐5个左右当前最应执行的动作
   - 过滤无效操作，确保动作可执行
   - 在[[TITAN-智能体|TITAN]]智能体中集成于[[LangGraph状态机]]的optimize_actions节点

3. **反射推理模块（Reflective Reasoning Module）**：
   - 框架的核心，使AI具备思考能力并能从卡关中自救
   - 进度监控：持续监控任务推进情况，无进展时判定为”卡关”
   - 反思复盘：回顾先前操作，分析错误并调整策略
   - 记忆机制：记录已测试区域，避免重复，完成任务的同时探索未测试区域寻找bug
   - 在[[TITAN-智能体|TITAN]]智能体中通过[[反思节点]]实现

4. **问题诊断模块（Problem Diagnosis Module）**：
   - 自动检测和报告问题
   - 崩溃监控：立即捕捉游戏崩溃
   - 任务卡死监控：标记无法推进的任务并清晰说明原因
   - 执行时间监控：发现动作/任务执行过慢的问题（如无限循环、[[服务]]器卡顿）
   - 整体误报率为30%
   - 在[[TITAN-智能体|TITAN]]智能体中实现为[[诊断预言机系统]]

## 来源
- [[Leveraging LLM Agents for Automated Video Game Testing]] — 框架原始设计
- [[TITAN-技术框架核心点报告]] — TITAN智能体实现

## 相关
- [[TITAN-智能体]] — implements
- [[AI-Agent]] — relates_to
- [[GPT-4o]] — originally_uses
- [[Qwen]] — implementation_uses
- [[Automated-Testing]] — relates_to
- [[Video-Game-Testing]] — relates_to
- [[LangGraph]] — implements_similar_pattern_as