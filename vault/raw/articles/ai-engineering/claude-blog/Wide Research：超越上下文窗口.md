---
title: "Wide Research：超越上下文窗口"
source: "https://manus.im/zh-cn/blog/manus-wide-research-solve-context-problem"
author:
published:
created: 2026-04-16
description: "你是否注意到，当你的AI助手研究一长串项目时，它会开始编造结果？这是一个常见的困扰，被称为\"编造阈值\"，是由AI上下文窗口的固有局限性造成的。本文深入探讨了为什么即使是最大的上下文叉棍口也无法解决这个问题，并介绍了一种新的架构范式：Wide Research。"
tags:
  - "clippings"
---
对于每个子任务,系统启动一个专用的子代理。至关重要的是,这些不是轻量级进程——它们是功能齐全的 Manus 实例,每个都具有:

•