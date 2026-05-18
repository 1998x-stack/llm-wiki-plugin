---
type: entity
status: active
confidence: 0.85
created: 2026-04-26
updated: 2026-04-26
last_accessed: 2026-04-26
source_count: 1
tags: [计算机历史, 电子工程, 硬件, 数值分析]
aliases: ["Electronic Numerical Integrator and Computer", "电子数值积分计算机"]
entity_type: project
relates_to: 
  - target: "[[J. Presper Eckert]]"
    type: designer
    confidence: 0.95
  - target: "[[John Mauchly]]"
    type: designer
    confidence: 0.95
  - target: "[[约翰·冯·诺依曼]]"
    type: advisor
    confidence: 0.9
  - target: "[[EDVAC]]"
    type: predecessor
    confidence: 0.9
  - target: "[[EDVAC报告]]"
    type: motivator_for
    confidence: 0.9
  - target: "[[存储程序计算机]]"
    type: predecessor_architecture
    confidence: 0.9
  - target: "[[First Draft of a Report on the EDVAC]]"
    type: motivator_for
    confidence: 0.9
    note: 冯·诺依曼在EDVAC报告中描述的架构正是为了解决ENIAC的局限性
supersedes: null
---

# ENIAC

## 概述
Electronic Numerical Integrator and Computer（电子数值积分[[计算]]机），世界上第一台通用电子数字[[计算]]机，于1945年在[[宾夕法尼亚大学]]莫尔电气工程学院完工。

## 关键内容

1. **技术规格**：
   - 1945年完工
   - 使用了17,468根真空管、70,000个电阻、10,000个电容和6,000个开关
   - 占地167平方米，重达27吨
   - 每秒可完成5000次加法运算，比当时任何机电式[[计算]]设备都快上千倍

2. **设计者**：
   - [[J. Presper Eckert]]和[[John Mauchly]]共同设计
   - [[冯·诺依曼]]于1944年夏天以顾问身份加入项目

3. **局限性**：
   - 通过物理接线和开关方式进行"编程"
   - 每次更换[[计算]]任务需要技术人员花费数天甚至数周时间重新[[Configuration|配置]]线路
   - 被视为"专用"而非"通用"[[计算]]机的根源

4. **历史意义**：
   - 证明了电子[[计算]]在速度上可以实现数量级的飞跃
   - 其物理接线式编程的局限性直接促使了[[存储程序计算机]]概念的诞生
   - 为EDVAC等后继[[计算]]机提供了设计经验

## 来源
- [[03-von-neumann-edvac]] — 第1.1、1.3节

## 相关
- [[J. Presper Eckert]] — co-designer
- [[John Mauchly]] — co-designer
- [[约翰·冯·诺依曼]] — advisor to the project
- [[EDVAC]] — successor project
- [[EDVAC报告]] — created to address ENIAC limitations
- [[存储程序计算机]] — created to solve ENIAC's limitations