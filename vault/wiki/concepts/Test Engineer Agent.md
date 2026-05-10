---
type: concept
status: active
confidence: 0.7
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [subagents, testing, automation, quality-assurance]
aliases: ["Test Engineer", "测试工程师", "自动化测试专家"]
relates_to: []
supersedes: null
---

# Test Engineer Agent

## 概述
Test Engineer Agent 是一名专门负责编写全面[[测试覆盖率|测试覆盖]]的测试自动化专家，确保软件质量和功能正确性。

## 关键内容

1. **核心职责**：
   - 分析需要测试的代码
   - 识别关键路径和边界情况
   - 按项目规范编写测试
   - 运行测试验证通过

2. **测试策略**：
   - **[[单元测试]]** - 独立测试单个函数或方法
   - **集成测试** - 测试组件交互
   - **端到端测试** - 测试完整工作流
   - **边界情况** - 边界条件、空值、空集合
   - **错误场景** - 失败处理、非法输入

3. **测试要求与标准**：
   - 使用项目现有测试框架（Jest、pytest 等）
   - 每个测试都要包含 setup/teardown
   - Mock 外部依赖
   - 用清晰描述说明测试目的
   - 在相关场景下加入性能断言
   - 最低 80% 代码覆盖率，关键路径要求 100%

## 来源
- [[test-engineer.md]] — 源文件定义

## 相关
- [[Subagent]] — relates_to
- [[Testing]] — relates_to
- [[Quality Assurance]] — relates_to
- [[Automation]] — relates_to