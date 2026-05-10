---
type: entity
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [gsd-agent, verification, quality-assurance]
aliases: ["gsd-verifier", "GSD Verifier", "GSD验证智能体"]
relates_to: 
  - target: "[[GSD Framework]]"
    type: part_of
    confidence: 0.9
  - target: "[[GSD 多智能体编排架构]]"
    type: implements
    confidence: 0.9
  - target: "[[gsd-executor]]"
    type: verifies
    confidence: 0.9
  - target: "[[GSD核心工作流]]"
    type: part_of_workflow
    confidence: 0.8
supersedes: null
---

# gsd-verifier

## 概述
GSD框架中的验证智能体，负责验证执行阶段生成的代码是否真正实现了预期的功能需求，不仅检查代码是否存在，更重要的是验证功能实现的正确性。

## 关键内容

1. **验证职责**：
   - 检查代码是否真正实现了需求，而不仅仅是存在
   - 读取git diff，验证SUMMARY中声明的工作是否反映在代码中
   - 运行关键测试命令，验证功能是否可用
   - 对比实际实现与需求之间的差距

2. **输入输出**：
   - 输入：PROJECT.md、REQUIREMENTS.md、所有N-M-SUMMARY.md执行存档
   - 输出：VERIFICATION.md文件，包含成功/失败状态及诊断信息

3. **验证价值**：
   - 确保代码实现与需求一致
   - 发现功能实现中的潜在问题
   - 为verify-work阶段提供问题诊断
   - 保证交付质量

## 来源
- [[raw/articles/ai-tools/claude-skills/04-multi-agent-orchestration.md]] — GSD多智能体编排架构详解

## 相关
- [[GSD Framework]] — 整体框架
- [[GSD 多智能体编排架构]] — 所属编排系统
- [[gsd-executor]] — 验证对象
- [[GSD核心工作流]] — 所属工作流程