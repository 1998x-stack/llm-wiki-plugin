---
type: concept
status: active
confidence: 0.8
created: 2026-04-25
updated: 2026-04-25
last_accessed: 2026-04-25
source_count: 2
tags: [文档生成, API, 开发工具, 技能, 文档处理]
aliases: ["API Documentation Generator", "API Doc Generator", "API文档自动生成工具", "api-documentation-generator"]
relates_to: []
supersedes: null
---

# API文档生成器

## 概述
API文档[[生成器]]是一种自动化工具，用于从源代码中的函数签名和注释自动生成完整的API文档。它可以生成[[OpenAPI]]/[[Swagger]]规范、API端点文档、SDK使用示例、集成指南、错误码参考和认证指南。

## 关键内容
1. **核心功能**：
   - 扫描指定目录（如`/src/api/`）下的所有源文件
   - 提取函数签名和[[JSDoc]]注释信息
   - 按端点或模块进行组织分类
   - 生成[[OpenAPI]]/[[Swagger]]规范
   - 生成API端点文档

2. **输出特性**：
   - 生成带示例的Markdown格式文档
   - 包含请求/响应Schema定义
   - 生成curl示例便于测试
   - 支持[[TypeScript]]类型信息
   - 生成SDK使用示例和集成指南

3. **文档结构**：
   - 每个端点包含描述、参数表格、响应格式
   - 错误码参考和认证指南
   - 提供多种语言的代码示例（cURL、JavaScript、[[Python]]等）
   - 包含请求参数的详细说明（名称、类型、是否必需、说明）

## 来源
- [[generate-api-docs]] — API文档生成器的具体实现步骤
- [[raw/assets/claude-howto/03-skills/doc-generator/SKILL.md]] — API文档生成技能的详细描述

## 相关
- [[JSDoc]] — 提取的注释格式标准
- [[文档重构]] — 相关的文档处理方法
- [[Markdown]] — 输出格式
- [[OpenAPI]] — API规范格式
- [[Swagger]] — API文档工具
- [[API]] — 应用程序接口

## relates_to
relates_to:
  - target: "[[JSDoc]]"
    type: depends_on
    confidence: 0.8
  - target: "[[Markdown]]"
    type: uses
    confidence: 0.9
  - target: "[[TypeScript]]"
    type: supports
    confidence: 0.7
  - target: "[[OpenAPI]]"
    type: generates
    confidence: 0.8
  - target: "[[Swagger]]"
    type: generates
    confidence: 0.8
  - target: "[[API]]"
    type: documents
    confidence: 0.9
  - target: "[[Documentation Writer Agent]]"
    type: relates_to
    confidence: 0.7