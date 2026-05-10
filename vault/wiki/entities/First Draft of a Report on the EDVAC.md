---
type: paper
status: active
confidence: 0.9
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [计算机体系结构, 存储程序, 计算机历史]
aliases: ["First Draft of a Report on the EDVAC", "EDVAC报告"]
entity_type: paper
relates_to: 
  - target: "[[约翰·冯·诺依曼]]"
    type: authored
    confidence: 0.9
  - target: "[[存储程序计算机]]"
    type: defines
    confidence: 0.9
  - target: "[[EDVAC]]"
    type: describes
    confidence: 0.9
  - target: "[[通用图灵机]]"
    type: engineering_realization
    confidence: 0.9
supersedes: null
---

# First Draft of a Report on the EDVAC

## 概述
1945年由[[冯·诺依曼]]撰写的关于EDVAC[[计算]]机设计的技术报告，首次系统阐述了[[存储程序计算机]]的设计原理，定义了现代[[计算]]机的基本架构[[规范化理论|范式]]。

## 关键内容

1. **历史背景**：
   - 1945年2月至6月撰写，1945年6月30日分发
   - 背景是[[ENIAC]][[计算]]机的局限性：需要物理接线才能更改程序
   - 报告最初以[[冯·诺依曼]]一人署名分发，引发署名争议

2. **核心创新**：
   - 存储程序概念：指令和数据存储在同一内存中
   - 五大组件架构：中央算术单元、中央控制单元、内存、输入设备、输出设备
   - 顺序执行模型：[[取指-解码-执行循环]]
   - 二进制表示：推荐使用二进制而非十进制

3. **工程实现**：
   - 内存容量估算：约4096个30位字的存储空间
   - 运算速度分析：加法约1微秒，乘法约1毫秒
   - 控制流机制：条件转移指令实现循环和分支

## 来源
- [[03-von-neumann-edvac]] — 全文

## 相关
- [[约翰·冯·诺依曼]] — authored
- [[存储程序计算机]] — defines fundamental architecture
- [[EDVAC]] — describes the computer design
- [[冯·诺依曼架构]] — defines the architecture