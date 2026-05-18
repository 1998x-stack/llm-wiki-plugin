---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [clean-code, code-review, software-quality, robert-c-martin, AI工程]
aliases: ["Clean Code Review", "Clean Code Principles", "Robert C. Martin Clean Code"]
relates_to: []
supersedes: null
---

# Clean Code Reviewer

## 概述
Clean [[Code Reviewer Agent|Code Reviewer]] 是一种专门用于执行 Clean Code 原则的[[代码审查]]代理，基于 [[Robert C. Martin]] 的 Clean Code 理论，专注于识别违反最佳实践的问题并提供可执行的修复建议。

## 关键内容

1. **命名原则**：变量、函数和类的命名应体现意图、可发音、可搜索。避免使用编码术语或前缀。类名应使用名词，方法名应使用动词。

2. **函数设计**：函数应少于20行，只做一件事，最多接受3个参数。避免使用flag参数、副作用和返回null值。

3. **注释策略**：代码应尽可能自解释。删除被注释掉的代码，避免编写冗余或误导性的注释。

4. **结构组织**：保持类小而专注，遵循[[SOLID原则|单一职责原则]]，实现高内聚低耦合。避免创建"上帝类"。

5. **[[SOLID原则]]**：严格遵守单一职责、[[SOLID原则|开闭原则]]、里氏替换、接口隔离和依赖倒置等面向对象设计原则。

6. **[[错误处理]]**：使用异常而非错误码进行[[错误处理]]，提供充分的上下文信息，绝不对null值进行操作。

## 来源
- [[clean-code-reviewer]] — Clean Code Reviewer Agent 概念

## 相关
- [[Robert C. Martin]] — author
- [[SOLID原则]] — extends
- [[代码审查]] — relates_to
- [[软件工程]] — relates_to
- [[重构]] — relates_to