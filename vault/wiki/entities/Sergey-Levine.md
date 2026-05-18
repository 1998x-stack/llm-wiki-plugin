---
type: entity
title: "Sergey Levine"
status: active
confidence: 0.95
created: 2026-04-15
updated: 2026-04-15
last_accessed: 2026-04-15
source_count: 2
tags: [人物, 机器人学, 深度学习, AI]
aliases:
  - Sergey Levine
  - Levine
relates_to:
  - target: "[[端到端视觉运动学习]]"
    type: caused
    confidence: 0.95
  - target: "[[视觉-语言-动作模型]]"
    type: caused
    confidence: 0.9
supersedes: null
---

# Sergey Levine

## 概述

Sergey Levine 是 UC Berkeley [[计算]]机科学系教授，深度机器人学习领域最具影响力的研究者之一（[[Google]] Scholar 引用超 23 万次）。他与 Chelsea Finn 等人于 2016 年首次实现了从像素到力矩的端到端[[端到端视觉运动学习|视觉运动策略]]学习，此后在 [[Google]] Brain/[[DeepMind]] 推动了大规模机器人学习从单任务到 RT-2 的演进。

## 关键内容

### 核心贡献

**端到端[[端到端视觉运动学习|深度视觉运动策略]]（2016）**：与 Chelsea Finn、Trevor Darrell、Pieter Abbeel 合作，首次在真实 [[PR2 机器人]]上实现从原始摄像头像素到关节力矩的端到端深度学习控制，提出引导策略搜索（GPS）框架解决样本效率问题，提出空间软[[注意力机制|注意力]]层（Spatial [[Softmax]]）解决视觉空间推理问题。

**元学习（MAML）**：与 Chelsea Finn 合作（2017），提出 Model-Agnostic Meta-Learning，用极少量数据快速适应新任务，对机器人学习和通用人工智能均有深远影响。

**大规模机器人学习**：在 [[Google]] Brain（2015–2016）和 [[Google]] [[DeepMind]] 工作期间推动"机器人农场"并行[[遥测系统|数据收集]]，研究从 RT-1（13 万条演示，700+ 任务）到 RT-2（VLA 模型，[[互联网]]知识迁移）的技术路线。

### 学术轨迹

- UC Berkeley EECS 博士后 → [[Google]] Brain（2015–2016）→ UC Berkeley 助理教授（2016–）
- [[Google]] [[DeepMind]] 兼职研究员

### 与 Chelsea Finn 的合作

Chelsea Finn 是 Levine 指导的博士生，两人在端到端机器人学习和元学习上长期合作。Finn 后来成为[[斯坦福大学]]教授，其 MAML 工作和机器人基础模型研究直接继承了这一合作的技术基因。

## 来源

- [[raw/books/机器人学/14-levine-deep-visuomotor-policies.md]]
- [[raw/books/机器人学/16-brohan-rt2-vision-language-action.md]]

## 相关

- [[端到端视觉运动学习]] — 开创性工作
- [[视觉-语言-动作模型]] — RT-2 的核心参与者
