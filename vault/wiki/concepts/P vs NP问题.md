---
type: concept
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 3
tags: [计算复杂度理论, 算法理论, 问题分类]
aliases: ["Polynomial vs NP Problem", "P=NP?", "P与NP问题"]
relates_to:
  - target: "[[NP完全性]]"
    type: central_to
    confidence: 0.9
  - target: "[[Cook定理]]"
    type: foundational_to
    confidence: 0.9
  - target: "[[计算复杂度理论]]"
    type: core_question_in
    confidence: 0.9
  - target: "[[多项式时间算法]]"
    type: question_about
    confidence: 0.8
supersedes: null
---

# P vs NP问题

## 概述
P vs NP问题是计算机科学和数学中最重要的未解决问题之一，询问是否所有能快速验证答案的问题都能快速找到答案。

## 关键内容
1. **定义**：P是能在确定性图灵机上多项式时间内求解的判定问题集合，NP是能在非确定性图灵机上多项式时间内求解的判定问题集合。P vs NP问题询问P是否等于NP。

2. **实际意义**：用自然语言表述："是否所有能快速验证答案的问题都能快速找到答案？"这个问题触及了创造与验证之间的关系——写一首好诗很难，但欣赏一首好诗相对容易。

3. **NP完全性的角色**：NP完全问题的存在使P vs NP问题具有了"全有或全无"的性质。如果任何一个NP完全问题有多项式算法，则P=NP；如果任何一个NP完全问题没有多项式算法，则P≠NP。

4. **现状**：P vs NP问题自1971年由Stephen Cook提出以来，至今仍未解决，被Clay数学研究所列为七大千禧年数学问题之一，悬赏100万美元。

## 来源
- [[08-cook-np-completeness]] — 问题定义与历史背景
- [[NP完全性]] — 核心概念
- [[Cook定理]] — 问题提出的背景

## 相关
- [[NP完全性]] — central to
- [[Cook定理]] — foundational to
- [[计算复杂度理论]] — core question in
- [[多项式时间算法]] — relates to
- [[多项式时间归约]] — proof technique