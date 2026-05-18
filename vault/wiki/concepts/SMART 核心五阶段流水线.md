---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [AI测试, 游戏测试, 代码覆盖率, 强化学习, AI工程]
aliases: ["SMART Five-Stage Pipeline", "SMART Core Five-Stage Pipeline", "SMART五阶段流水线"]
relates_to:
  - target: "[[AST差异解析]]"
    type: part_of
    confidence: 0.8
  - target: "[[语义子目标生成]]"
    type: part_of
    confidence: 0.8
  - target: "[[语义奖励生成]]"
    type: part_of
    confidence: 0.8
  - target: "[[结构锚点映射]]"
    type: part_of
    confidence: 0.8
  - target: "[[自适应混合奖励]]"
    type: part_of
    confidence: 0.8
supersedes: null
---

# SMART 核心五阶段流水线

## 概述
一种用于AI驱动的游戏测试方法，通过五个阶段实现代码覆盖率和游戏意图的协同优化，确保AI既能完成游戏任务又能覆盖尽可能多的代码路径。

## 关键内容

1. **阶段1：[[AST差异解析]]**：
   - 比较游戏更新前后的代码，识别新增/修改的代码行和判断分支
   - 将这些代码点标记为「必须测到的代码点」

2. **阶段2：[[语义子目标生成]]**：
   - 将复杂的任务（如制作洋葱披萨）拆分成玩家可逐步执行的小步骤
   - 确保这些步骤必须按特定顺序执行

3. **阶段3：[[语义奖励生成]]**：
   - 将每一步小目标转化为AI能理解的奖励规则
   - 完成某一步骤给予相应奖励，确保AI按流程操作

4. **阶段4：[[结构锚点映射]]**：
   - 将「小步骤」与「代码锚点」进行一一对应绑定
   - 确保只有在执行相应步骤时才测试相关代码，避免无效测试

5. **阶段5：[[自适应混合奖励]]**：
   - 结合语义奖励（按步骤完成任务）和结构奖励（首次测试到新代码）
   - 既保证功能正常又能实现代码全覆盖

## 来源
- [[Synergizing Code Coverage and Gameplay Intent: Coverage-Aware Game Playtesting with LLM-Guided Reinforcement]] — 论文内容

## 相关
- [[强化学习]] — relates_to
- [[代码覆盖率]] — relates_to
- [[AI测试]] — relates_to
- [[游戏开发]] — relates_to