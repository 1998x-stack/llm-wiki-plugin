---
type: entity
entity_type: paper
status: active
confidence: 0.98
created: 2026-04-17
updated: 2026-04-17
last_accessed: 2026-04-17
source_count: 1
tags:
- 技术
- 研究
- 历史
- 计算理论
aliases:
- First Draft of a Report on the EDVAC
- EDVAC Report
- EDVAC 报告
- 关于 EDVAC 的报告初稿
relates_to:
- target: "[[约翰·冯·诺依曼]]"
  type: caused_by
  confidence: 0.99
  note: 署名作者，将工程讨论提炼为逻辑框架
- target: "[[存储程序计算机]]"
  type: caused
  confidence: 0.99
  note: 人类历史上第一份系统描述存储程序计算机设计原理的文献
- target: "[[图灵机]]"
  type: extends
  confidence: 0.9
  note: 将通用图灵机理论转化为可工程实现的方案
- target: "[[On Computable Numbers 论文]]"
  type: extends
  confidence: 0.85
  note: 完成了从 Turing 理论到工程实践的关键转化
- target: "[[J. Presper Eckert]]"
  type: related_to
  confidence: 0.9
  note: EDVAC 硬件概念的重要贡献者，署名争议的核心人物
- target: "[[John Mauchly]]"
  type: related_to
  confidence: 0.9
  note: EDVAC 硬件概念的重要贡献者，署名争议的核心人物
- target: "[[Herman Goldstine]]"
  type: related_to
  confidence: 0.85
  note: 以安全官员身份分发报告至美英多个研究机构
- target: "[[Maurice Wilkes]]"
  type: caused
  confidence: 0.85
  note: Wilkes 读到报告后深受启发，回国建造了 EDSAC
- target: "[[约翰·冯·诺依曼]]"
  type: related_to
  confidence: 0.9
  note: 报告描述了 ENIAC 后继机 EDVAC 的设计，解决了 ENIAC 的物理接线编程缺陷
- target: "[[冯·诺依曼瓶颈]]"
  type: caused
  confidence: 0.9
  note: 报告设计的架构存在 CPU-内存数据传输瓶颈，后来被称为冯·诺依曼瓶颈
supersedes: null
---

# EDVAC 报告

## 概述

[[约翰·冯·诺依曼|Von Neumann]]于1945年撰写的内部技术报告《First Draft of a Report on the EDVAC》，是人类历史上第一份系统、完整地描述[[存储程序计算机]]设计原理的文献，定义了此后八十年所有计算机的基本架构范式。

## 关键内容

### 报告信息

| 项目 | 内容 |
|------|------|
| **标题** | First Draft of a Report on the EDVAC |
| **作者** | John von Neumann（署名）|
| **撰写时间** | 1945年2月至6月 |
| **分发时间** | 1945年6月30日 |
| **发表形式** | 内部技术报告（非正式出版物） |
| **篇幅** | 约101页（未完成的初稿） |

### 五大组件架构

Von Neumann 将计算机分解为五个功能器官：
1. **中央算术单元（CA）** — 对应现代 ALU
2. **中央控制单元（CC）** — 对应现代控制器
3. **内存（M）** — 同时存储数据和指令
4. **输入设备（I）**
5. **输出设备（O）**

### 核心贡献

- **存储程序概念**：指令与数据统一存储，消除物理重新接线
- **取指-解码-执行循环**：定义了处理器工作的基本范式
- **二进制表示**：明确推荐二进制而非十进制
- **条件转移指令**：实现循环、分支、子程序的基础

### 署名争议

报告以 von Neumann 一人署名分发，引发了计算机史上最著名的优先权之争。[[J. Presper Eckert|Eckert]] 和 [[John Mauchly|Mauchly]] 认为存储程序的核心概念源自他们在1944年的讨论，von Neumann 是将工程直觉提炼为逻辑框架的人，而非概念的唯一发明者。更严重的是，由于报告被视为公开披露，直接导致 Eckert 和 Mauchly 后来申请的 EDVAC 专利无法执行。

### 传播效应

报告被 [[Herman Goldstine|Goldstine]] 广泛分发至美英研究机构后，几乎每一个读到它的团队都能够理解其设计思想并据此建造自己的存储程序计算机：
- **EDSAC**（1949，剑桥大学）— [[Maurice Wilkes]] 主持
- **Manchester Baby**（1948，曼彻斯特大学）
- **EDVAC**（1951，宾夕法尼亚大学）
- **IAS 计算机**（1952，普林斯顿高等研究院）

## 来源

- [[raw/books/计算机科学/03-von-neumann-edvac.md]]

## 相关

- [[约翰·冯·诺依曼]] — 署名作者
- [[存储程序计算机]] — 报告定义的核心概念
- ENIAC — 报告描述的后继机（物理接线编程的前代计算机）
- [[图灵机]] — 理论源头
- [[冯·诺依曼瓶颈]] — 报告架构的固有限制
