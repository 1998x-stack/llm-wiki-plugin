---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, quality-assurance, validation, Agent系统]
aliases: ["gsd-plan-checker", "GSD Plan Checker", "GSD计划验证智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-planner]]"
    type: validates
    confidence: 0.9
  - target: "[[Nyquist Validation Layer]]"
    type: implements_validation
    confidence: 0.7
supersedes: null
---

# gsd-plan-checker

## 概述
GSD框架中的8维度计划质量验证智能体，负责对[[gsd-planner]]生成的计划进行全面质量检查，确保计划符合GSD框架的各项要求。

## 关键内容

1. **验证维度**：
   - 需求覆盖完整性：确保计划涵盖所有必需功能
   - 技术一致性：与PROJECT.md约定保持一致
   - 计划原子性：确保单个上下文可完成
   - 依赖关系正确性：验证计划间依赖关系
   - 并行安全性：确保同波次无文件冲突
   - 可验证性：<verify>标签包含可执行命令
   - 上下文一致性：与CONTEXT.md决策保持一致
   - Nyquist验证覆盖：测试合约覆盖

2. **验证流程**：
   - 输入：[[gsd-planner]]生成的所有PLAN文件
   - 输出：PASS/FAIL结果及修订意见
   - 循环机制：最多循环3次，超过则上报用户判断
   - 验证循环：
     1. [[gsd-planner]] 生成计划
     2. gsd-plan-checker 验证8维度
     3. 通过则批准，不通过则生成修订意见
     4. [[gsd-planner]] 根据意见修订
     5. 重复验证直至通过或达到最大循环次数

3. **[[质量保障]]作用**：
   - 在执行前确保计划质量
   - 防止执行阶段出现问题
   - 保证计划符合GSD框架约束

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-planner]] — 验证对象
- [[Nyquist Validation Layer]] — 验证理念体现