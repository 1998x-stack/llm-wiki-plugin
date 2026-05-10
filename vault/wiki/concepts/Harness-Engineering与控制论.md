---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: ["ai-engineering", "agent-systems", "control-theory"]
aliases: ["Harness Engineering Is Cybernetics", "Harness工程与控制论"]
relates_to:
  - target: "[[Harness-Engineering]]"
    type: extends
    confidence: 0.8
  - target: "[[Control-Theory]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Cybernetics]]"
    type: relates_to
    confidence: 0.8
  - target: "[[Kubernetes]]"
    type: compares_to
    confidence: 0.7
supersedes: null
---

# Harness Engineering与控制论

## 概述
[[Harness-Engineering|Harness Engineering]]是[[控制论视角|控制论]]在AI Agent时代的第三次现身，体现了通过反馈回路自动化复杂系统的经典思想。

## 关键内容

1. **[[控制论视角|控制论]]的三次演进**：
   - **第一次（1780年代）**：瓦特的[[调速器稳定性理论|离心调速器]] - 蒸汽机时代的自动化反馈回路
     - 传感器：飞球
     - 执行器：阀门联动装置
     - 工人从手动调节转为设计调速器本身
   - **第二次（2010年代）**：Kubernetes - 云[[计算]]时代的自动化反馈回路
     - 传感器：metrics和health check
     - 执行器：调度器
     - 工程师从手动重启[[服务]]转为编写目标spec
   - **第三次（现在）**：[[Harness-Engineering|Harness Engineering]] - AI Agent时代的自动化反馈回路
     - 传感器：测试、Linter和可观测性
     - 执行器：LLM
     - 工程师从写代码转为设计运行环境

2. **共同模式特征**：
   - 人造出足够好的传感器和执行器，在特定层面闭合反馈回路
   - 人类角色从直接操作转向系统设计
   - 通过自动化验证和约束提高效率

3. **架构层面的反馈闭合**：
   - 底层反馈回路：编译器、测试框架、Linter（检测语法、行为、风格问题）
   - 架构层面反馈：直到LLM出现，才有能力理解和生成代码意图
   - 现代Harness通过[[项目约定手册|AGENTS.md]]、自定义Linter、CI检查实现架构层面的反馈回路

4. **术语渊源**：
   - "[[控制论（Cybernetics）|Cybernetics]]"（[[控制论视角|控制论]]）来自希腊语"kubernetes"（舵手）
   - Kubernetes的词源正是来自[[控制论视角|控制论]]概念
   - 体现了从"划桨"到"掌舵"的角色转变

## 来源
- [[Harness Engineering的本质是什么？ - riba2534 的回答]] — 关于Harness Engineering与控制论关系的分析

## 相关
- [[Harness-Engineering]] — relates_to
- [[Control-Theory]] — relates_to
- [[Cybernetics]] — relates_to
- [[Kubernetes]] — relates_to
- [[OpenAI]] — relates_to