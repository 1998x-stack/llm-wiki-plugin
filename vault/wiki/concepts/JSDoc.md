---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [文档工具, JavaScript, 注释规范, AI工程]
aliases: ["JavaScript Documentation", "JS Documentation", "JSDoc规范"]
relates_to: []
supersedes: null
---

# JSDoc

## 概述
JSDoc是一种用于JavaScript的结构化注释标准，允许开发者在源代码中添加文档注释，这些注释可以被工具提取和解析以生成API文档。

## 关键内容
1. **基本语法**：
   - 使用`/** */`包围多行注释
   - 使用`@`符号标记特定类型的注释标签
   - 支持函数、类、变量等多种元素的文档注释

2. **常用标签**：
   - `@param`：描述函数参数
   - `@returns`：描述函数返回值
   - `@example`：提供使用示例
   - `@since`：[[标注]]版本信息

3. **文档生成**：
   - 可与[[API文档生成器]]等工具集成
   - 通过静态分析提取函数签名和注释
   - 生成结构化的API文档

## 来源
- [[API文档生成器]] — JSDoc作为注释源被API文档生成器提取
- [[]] — 

## 相关
- [[API文档生成器]] — 依赖JSDoc进行文档提取
- [[JavaScript]] — JSDoc的主要应用场景
- [[TypeScript]] — 与TypeScript兼容

## relates_to
relates_to:
  - target: "[[API文档生成器]]"
    type: enables
    confidence: 0.9
  - target: "[[JavaScript]]"
    type: part_of
    confidence: 0.8
  - target: "[[TypeScript]]"
    type: extends
    confidence: 0.7