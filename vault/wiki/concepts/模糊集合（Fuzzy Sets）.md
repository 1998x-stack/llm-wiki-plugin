---
type: concept
status: active
confidence: 0.85
created: 2026-04-16
updated: 2026-04-16
last_accessed: 2026-04-16
source_count: 1
tags: ["概率论", 控制论]
aliases: ["Fuzzy Sets", "模糊逻辑", "隶属度函数"]
relates_to:
  - target: "[[控制论（Cybernetics）]]"
    type: part_of
    confidence: 0.8
  - target: "[[信息论]]"
    type: relates_to
    confidence: 0.7
  - target: "[[强化学习]]"
    type: relates_to
    confidence: 0.6
supersedes: null
---

# 模糊集合（Fuzzy Sets）

## 概述
Lotfi Zadeh 于 1965 年提出模糊集合理论，用隶属度函数取代经典集合论的非此即彼二值划分，为处理人类语言和认知中固有的模糊性开辟了全新的数学框架。

## 关键内容

1. **历史背景**：经典集合论要求元素要么属于、要么不属于集合，但现实世界中"高个子"、"年轻人"、"温暖的天气"等概念天然不具有清晰边界。[[概率论]]处理事件发生的不确定性，而模糊性处理类别边界的渐变性——这是两种完全不同的不确定性。

2. **核心创新**：隶属度函数 μ(x) ∈ [0,1] 表示元素 x 属于集合的程度，而非经典集合的 {0,1} 二值。"不相容原理"：系统越复杂，精确建模与有意义陈述之间的矛盾越尖锐。

3. **与同时代思想的呼应**：Wittgenstein 的"家族相似性"、Eleanor Rosch 的"原型理论"都与模糊集合精神高度吻合——自然类别围绕典型实例组织，成员资格是程度问题。

4. **应用**：模糊控制（家电、工业自动化）、模糊决策、模糊模式识别、模糊专家系统等。

## 来源
- [[16-zadeh-fuzzy-sets]] — Zadeh 模糊集合

## 相关
- [[控制论（Cybernetics）]] — part_of
- [[信息论]] — relates_to
- [[强化学习]] — relates_to
