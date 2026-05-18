---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 1
tags: [design-principles, oop, software-engineering, 计算理论]
aliases: ["SOLID Principles", "SOLID原则", "单一职责原则", "开闭原则", "里氏替换原则", "接口隔离原则", "依赖倒置原则"]
relates_to:
  - target: "[[代码质量]]"
    type: relates_to
  - target: "[[设计模式]]"
    type: relates_to
  - target: "[[代码审查]]"
    type: relates_to
  - target: "[[面向对象编程]]"
    type: extends
supersedes: null
---

# SOLID原则

## 概述
SOLID是一套面向对象设计的基本原则，用于指导开发者创建更易于维护和扩展的软件系统。

## 关键内容

1. **单一职责原则（SRP - Single Responsibility Principle）**：
   - 一个类应该只有一个引起它变化的原因
   - 每个类或模块应该只负责一项功能领域
   - 有助于提高代码的[[可维护性]]和可读性

2. **开闭原则（OCP - Open/Closed Principle）**：
   - 软件实体应该对扩展开放，对修改关闭
   - 在不修改现有代码的情况下扩展系统功能
   - 通过抽象和多态来实现

3. **里氏替换原则（LSP - Liskov Substitution Principle）**：
   - 子类型必须能够替换其基类型
   - 确保继承关系的正确性
   - 保证程序行为的一致性

4. **接口隔离原则（ISP - Interface Segregation Principle）**：
   - 客户端不应该依赖于它们不需要的接口
   - 将大接口拆分为更小、更具体的接口
   - 减少实现类的负担

5. **依赖倒置原则（DIP - Dependency Inversion Principle）**：
   - 高层模块不应依赖低层模块，两者都应依赖于抽象
   - 抽象不应依赖细节，细节应依赖抽象
   - 有助于解耦和实现松耦合架构

## 来源
- [[代码审查 Skill]] — SOLID原则作为代码质量检查的重要标准

## 相关
- [[代码质量]] — relates_to
- [[设计模式]] — relates_to
- [[代码审查]] — relates_to
- [[面向对象编程]] — extends
- [[依赖注入]] — relates_to
- [[架构设计]] — relates_to